#!/usr/bin/env python3
"""
fetch_feed.py  —  the no-AI stage of the content engine.

Pulls RSS/Atom feeds + Google Alert feeds listed in sources.yaml, filters by
keyword and recency, scores each item deterministically (no AI, no tokens),
deduplicates, ranks, and writes feed.json in the format the cockpit reads.

No cap on story count — everything that passes freshness + keyword filters is included.
Pinned stories (from pins.json) are always kept in the feed even if they've aged out.
Stories dropped from a refresh are appended to history/dismissed.json.

Usage:  python3 fetch_feed.py
Output: feed.json (next to this script)
"""

import json, re, sys, html, hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path
import io

try:
    import feedparser, yaml
except ImportError:
    sys.exit("Missing deps. Run:  pip install -r requirements.txt")

HERE = Path(__file__).parent
CONFIG = HERE / "sources.yaml"
OUTPUT = HERE / "feed.json"
HISTORY_DIR = HERE / "history"
PINS_PATH = HERE / "pins.json"
DISMISSED_PATH = HISTORY_DIR / "dismissed.json"

DISMISSED_MAX = 500  # cap the dismissed history file


def load_config():
    with open(CONFIG) as f:
        return yaml.safe_load(f)


def load_pins():
    if not PINS_PATH.exists():
        return {"pinned_ids": [], "stories": {}}
    try:
        data = json.loads(PINS_PATH.read_text())
        if 'stories' not in data:
            data['stories'] = {}
        return data
    except Exception:
        return {"pinned_ids": [], "stories": {}}


def load_previous_feed():
    """Return list of stories from current feed.json before overwriting."""
    if not OUTPUT.exists():
        return []
    try:
        with open(OUTPUT) as f:
            return json.load(f).get("stories", [])
    except Exception:
        return []


def save_dismissed(dropped_stories):
    """Append stories dropped from this refresh to dismissed.json (capped at DISMISSED_MAX)."""
    if not dropped_stories:
        return
    HISTORY_DIR.mkdir(exist_ok=True)
    existing = []
    if DISMISSED_PATH.exists():
        try:
            existing = json.loads(DISMISSED_PATH.read_text())
        except Exception:
            existing = []

    now = datetime.now(timezone.utc).isoformat()
    new_entries = [{"dismissed_at": now, **s} for s in dropped_stories]
    combined = new_entries + existing
    combined = combined[:DISMISSED_MAX]
    DISMISSED_PATH.write_text(json.dumps(combined, indent=2, ensure_ascii=False))


def clean_text(raw, limit=320):
    """Strip HTML tags/entities from feed summaries; trim to a sane length."""
    if not raw:
        return ""
    txt = re.sub(r"<[^>]+>", "", raw)
    txt = html.unescape(txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return (txt[:limit].rsplit(" ", 1)[0] + "…") if len(txt) > limit else txt


def get_published(entry):
    """Return a timezone-aware datetime for the entry, or None."""
    for key in ("published_parsed", "updated_parsed"):
        t = entry.get(key)
        if t:
            return datetime(*t[:6], tzinfo=timezone.utc)
    return None


def norm_title(title):
    """Normalized key for dedup: lowercased, alphanumerics only."""
    return re.sub(r"[^a-z0-9]+", "", title.lower())


def make_id(title, when):
    date = (when or datetime.now(timezone.utc)).strftime("%Y-%m-%d")
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:48].rstrip("-")
    return f"{date}-{slug}" if slug else f"{date}-{hashlib.md5(title.encode()).hexdigest()[:8]}"


def score_item(title, summary, tier, cfg):
    """
    Deterministic relevance score 0-10. NO AI.
    Combines: source tier + keyword density + boost terms.
    """
    text = f"{title} {summary}".lower()
    kw_hits = [k for k in cfg["keywords"] if k.lower() in text]
    boost_hits = [k for k in cfg.get("boost_keywords", []) if k.lower() in text]

    # source strength from tier (1->10, 2->7, 3->4)
    source_strength = {1: 10, 2: 7, 3: 4}.get(tier, 5)
    # keyword relevance: scales with hits, capped
    keyword_relevance = min(10, 3 + len(kw_hits) * 2)
    # boost: research-quality signal words
    boost = min(2, len(boost_hits))

    raw = source_strength * 0.45 + keyword_relevance * 0.55 + boost
    return round(min(10, raw), 1), kw_hits, source_strength, keyword_relevance


def passes_filters(title, summary, when, cfg, cutoff):
    text = f"{title} {summary}".lower()
    if when and when < cutoff:
        return False, "stale"
    if any(b.lower() in text for b in cfg.get("block_keywords", [])):
        return False, "blocked"
    hits = sum(1 for k in cfg["keywords"] if k.lower() in text)
    if hits < cfg.get("min_keyword_hits", 1):
        return False, "off-topic"
    return True, "ok"


def archive_if_new_day():
    """If feed.json exists and was generated on a previous calendar day, save it to history/."""
    if not OUTPUT.exists():
        return
    try:
        with open(OUTPUT) as f:
            existing = json.load(f)
        gen_at = existing.get("meta", {}).get("generated_at", "")
        gen_date = datetime.fromisoformat(gen_at).date()
        today = datetime.now(timezone.utc).date()
        if gen_date < today:
            HISTORY_DIR.mkdir(exist_ok=True)
            dest = HISTORY_DIR / f"{gen_date}.json"
            dest.write_text(json.dumps(existing, indent=2, ensure_ascii=False))
            print(f"  archived {gen_date} -> history/{gen_date}.json")
    except Exception:
        pass


def load_seen_ids():
    """Collect all story IDs already saved to history files."""
    seen = set()
    if not HISTORY_DIR.exists():
        return seen
    for path in HISTORY_DIR.glob("*.json"):
        if path.name == "dismissed.json":
            continue
        try:
            with open(path) as f:
                data = json.load(f)
            for story in data.get("stories", []):
                if story.get("id"):
                    seen.add(story["id"])
        except Exception:
            pass
    return seen


def pub_sort_key(r):
    """Sort key: dated items newest-first, then by score; undated items fall to the bottom."""
    pub = r["score_breakdown"].get("published")
    if pub:
        try:
            return (1, datetime.fromisoformat(pub).timestamp(), r["score"])
        except Exception:
            pass
    return (0, 0, r["score"])


LOG_PATH = HERE / "fetch.log"

def _log(lines):
    """Append lines to fetch.log and print to stdout."""
    text = "\n".join(lines) + "\n"
    print(text, end="")
    with open(LOG_PATH, "a") as f:
        f.write(text)


def main():
    archive_if_new_day()
    prev_stories = load_previous_feed()
    prev_ids = {s["id"] for s in prev_stories if s.get("id")}

    pins = load_pins()
    pinned_ids = set(pins.get("pinned_ids", []))

    seen_ids = load_seen_ids()

    cfg = load_config()
    cutoff = datetime.now(timezone.utc) - timedelta(hours=cfg.get("freshness_hours", 72))
    all_feeds = (cfg.get("feeds") or []) + (cfg.get("alert_feeds") or [])

    candidates = {}
    dead_feeds = []
    stats = {"fetched": 0, "kept": 0, "feeds_ok": 0, "feeds_dead": 0}

    for feed in all_feeds:
        try:
            parsed = feedparser.parse(feed["url"])
            if parsed.bozo and not parsed.entries:
                raise ValueError(parsed.get("bozo_exception", "no entries"))
            stats["feeds_ok"] += 1
        except Exception as e:
            dead_feeds.append(feed["name"])
            stats["feeds_dead"] += 1
            print(f"  ! dead/empty feed: {feed['name']} ({e})")
            continue

        for entry in parsed.entries:
            stats["fetched"] += 1
            title = clean_text(entry.get("title", ""), 200)
            summary = clean_text(entry.get("summary", entry.get("description", "")))
            link = entry.get("link", "")
            when = get_published(entry)
            if not title or not link:
                continue

            ok, _reason = passes_filters(title, summary, when, cfg, cutoff)
            if not ok:
                continue

            key = norm_title(title)
            score, kw_hits, src_str, kw_rel = score_item(title, summary, feed["tier"], cfg)

            if key in candidates:
                rec = candidates[key]
                rec["sources"].append({"url": link, "outlet": feed["name"],
                                       "tier": feed["tier"], "role": "corroboration"})
                if score > rec["score"]:
                    rec["score"] = score
                continue

            story_id = make_id(title, when)
            # skip if already in history archives (not just current feed)
            if story_id in seen_ids and story_id not in prev_ids:
                continue

            stats["kept"] += 1
            candidates[key] = {
                "id": story_id,
                "status": "new",
                "pinned": story_id in pinned_ids,
                "first_seen": datetime.now(timezone.utc).isoformat(),
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "headline": title,
                "summary": summary,
                "category": None,
                "topic_tags": kw_hits[:6],
                "angle_tag": "unscored",
                "angle_line": None,
                "angle_authenticity": None,
                "sources": [{"url": link, "outlet": feed["name"],
                             "tier": feed["tier"], "role": "origin"}],
                "verification": f"Source pre-vetted (Tier {feed['tier']} feed: {feed['name']})",
                "caveats": None,
                "score": score,
                "score_breakdown": {
                    "source_strength": src_str,
                    "keyword_relevance": kw_rel,
                    "published": when.isoformat() if when else None,
                },
                "keyword_hits": kw_hits,
                "generated": [],
            }

    # inject pinned stories that didn't make it through the filter (aged out, etc.)
    new_ids = {r["id"] for r in candidates.values()}
    for pid in pinned_ids:
        if pid not in new_ids and pid in pins.get("stories", {}):
            s = pins["stories"][pid]
            s["pinned"] = True
            key = norm_title(s.get("headline", pid))
            if key not in candidates:
                candidates[key] = s

    # sort by published date newest-first, undated items fall to the bottom
    live = sorted(candidates.values(), key=pub_sort_key, reverse=True)
    live_ids = {s["id"] for s in live}

    # track dismissed: stories that were in the previous feed and aren't in the new one
    pinned_or_new = live_ids | pinned_ids
    dismissed = [s for s in prev_stories if s.get("id") and s["id"] not in pinned_or_new]
    if dismissed:
        save_dismissed(dismissed)
        print(f"  dismissed {len(dismissed)} stories -> history/dismissed.json")

    added_ids = live_ids - prev_ids if prev_ids else set()
    dropped_ids = prev_ids - live_ids

    for s in live:
        s["is_new"] = s["id"] in added_ids

    feed_obj = {
        "meta": {
            "pack": "wellness-genz",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "live_count": len(live),
            "schema_version": 1,
            "pipeline": "fetch_feed.py (no-AI)",
            "dead_feeds": dead_feeds,
            "stats": stats,
        },
        "stories": live,
    }

    with open(OUTPUT, "w") as f:
        json.dump(feed_obj, f, indent=2, ensure_ascii=False)
    log_lines = [
        f"",
        f"  feeds: {stats['feeds_ok']} ok, {stats['feeds_dead']} dead",
        f"  items: {stats['fetched']} fetched -> {stats['kept']} kept -> {len(live)} in feed",
        f"  delta: +{len(added_ids)} new, -{len(dropped_ids)} dropped (prev: {len(prev_ids)})",
    ]
    if dead_feeds:
        log_lines.append(f"  check these dead feeds in sources.yaml: {', '.join(dead_feeds)}")
    log_lines.append(f"  wrote {OUTPUT}")
    _log(log_lines)


if __name__ == "__main__":
    main()
