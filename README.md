# Feed Cockpit — the no-AI feed + review dashboard

A frugal front-end for the content engine. A plain Python script pulls your RSS/alert feeds, filters and ranks them with **zero AI / zero tokens**, and writes `feed.json`. The cockpit (a single HTML page) shows that feed so you can scan, judge the angle, and pick what to generate. Generation still happens in Claude Code — the cockpit copies the command for you.

This is **separate from your `content-engine` skill**, which is untouched. This folder feeds *into* it.

## What's in here
- `sources.yaml` — your feeds, tiers, and keyword filters. **The only file you edit regularly.**
- `fetch_feed.py` — the no-AI pipeline: fetch → filter → score → dedup → write `feed.json`.
- `feed.json` — the ranked output (a sample is included; the script overwrites it).
- `cockpit.html` — the dashboard. Reads `feed.json`.
- `requirements.txt` — Python deps (feedparser, PyYAML).
- `.github/workflows/feed.yml` — optional: free 24/7 scheduling in the cloud (see below).

## One-time setup
```bash
cd feed-cockpit
pip install -r requirements.txt
```

## Run it
```bash
python3 fetch_feed.py        # pulls feeds, writes feed.json
```
You'll see how many items were fetched, kept, and whether any feeds were dead.

## Open the cockpit
Because browsers block local file reads, **serve the folder** (one command):
```bash
python3 -m http.server 8000
```
Then open **http://localhost:8000/cockpit.html**. Click "↻ reload feed.json" after a fresh run to see new stories. (When you host it later, this serving step is automatic.)

## Daily flow
1. `python3 fetch_feed.py` (or let the scheduler do it — below)
2. Open the cockpit, scan the ranked feed
3. Judge the angle yourself, click **Pick & copy command** on a winner
4. Paste `generate #<id>` into Claude Code → it builds the content in your voice
5. Record, ship

## The division of labor (why this saves tokens)
The script honestly does only what code can do well:
- **fetches** feeds, **filters** by keyword + recency, **blocks** noise, **dedupes**, and **scores by relevance** (source tier + keyword density). No AI.

It deliberately leaves `angle_tag` as `"unscored"` because deciding whether a story has a real wellness angle (native / bridge / stretch) is judgment, not pattern-matching. That judgment — and the actual script writing — is the only part that touches Claude. Code ranks 80+ raw items down to a clean ~20; you (or a cheap Claude pass) only judge those.

## Tuning relevance (no code)
Everything lives in `sources.yaml`:
- Add/remove **feeds** (verify URLs resolve; dead ones are skipped and flagged in the cockpit).
- Add **Google Alert** RSS feeds under `alert_feeds` — this is how AP/Reuters/CNN/breaking news get in. Create at google.com/alerts, set delivery to RSS, paste the URL.
- Widen/narrow **keywords**, raise `min_keyword_hits` to be stricter, add `block_keywords` to kill noise, add `boost_keywords` to float quality studies up.

## Running it 24/7

A scheduled job runs the script automatically — you do NOT keep a process running. Two options:

### Option 1 — Your Mac (free, simple, but only while awake)
Runs only when your laptop is on and not asleep. Good for getting started.

`launchd` is the Mac-native way. Create `~/Library/LaunchAgents/com.wylee.feedcockpit.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.wylee.feedcockpit</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>/Users/wylee/path/to/feed-cockpit/fetch_feed.py</string>
  </array>
  <key>StartInterval</key><integer>3600</integer>   <!-- every 3600s = 1 hour -->
  <key>RunAtLoad</key><true/>
</dict></plist>
```
Then: `launchctl load ~/Library/LaunchAgents/com.wylee.feedcockpit.plist`
(Simpler alternative: a `cron` entry `0 * * * * cd /path/to/feed-cockpit && /usr/bin/python3 fetch_feed.py`.)

### Option 2 — GitHub Actions (free, TRUE 24/7, independent of your computer)
This is the real "always on" answer. The included `.github/workflows/feed.yml` runs the script hourly on GitHub's servers and commits the updated `feed.json` back. Your laptop can be off.
1. Put this folder in a GitHub repo (`git init`, push).
2. The workflow runs automatically on the hourly schedule (or hit "Run workflow" in the Actions tab).
3. Optional: enable **GitHub Pages** on the repo to serve `cockpit.html` at a public URL your partner can bookmark — now the feed updates itself and they just visit the page.

Recommendation: start with Option 1 to confirm the pipeline behaves, then move to Option 2 for hands-off 24/7. Same script, same `feed.json` — only *where* it runs changes.

## Where this is headed (not built yet)
- The cockpit currently copies a command to paste into Claude Code. Generating *in-place* (a real button) needs a small backend holding an API key — the hosted Supabase/Netlify version on the roadmap. The `feed.json` format is identical all the way up, so nothing here gets rebuilt when you graduate.
