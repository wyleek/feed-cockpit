# Feed format (the keystone)

Everything reads from this. Discovery WRITES records in this shape; the HTML feed and (later) Supabase READ this shape. Same data, different home — that's the portability guarantee. Do not change field names casually; downstream renderers depend on them.

## Files

- **`workspace/feed.json`** — the live feed. Up to **20** ranked records, plus any pinned records riding above the cap. This is what the HTML page renders.
- **`workspace/archive.json`** — bumped, dismissed, and shipped stories. Append-only. **Never delete a record** — move it here.

Both files are a JSON object with a top-level `meta` block and a `stories[]` array (schema below).

## File envelope

```json
{
  "meta": {
    "pack": "wellness-genz",
    "generated_at": "2026-06-12T12:00:00Z",
    "feed_cap": 20,
    "live_count": 18,
    "pinned_count": 2,
    "schema_version": 1
  },
  "stories": [ /* record objects, sorted by score desc; pinned float to top of their status group */ ]
}
```

`schema_version` exists so future field changes are detectable. Bump it if the record shape changes; renderers should check it.

## The record (one story)

```json
{
  "id": "2026-06-12-cannabis-sleep",

  "status": "new",
  "pinned": false,
  "first_seen": "2026-06-12T07:00:00Z",
  "last_updated": "2026-06-12T12:00:00Z",

  "headline": "1 in 5 young adults use weed or booze to fall asleep — and it backfires",
  "summary": "A national study found 22% of young adults use cannabis or alcohol as a sleep aid, but it degrades sleep quality over time. Among past-year cannabis users, 41% used it specifically for sleep.",
  "category": "sleep",
  "topic_tags": ["sleep", "substances", "young-adults"],

  "angle_tag": "native",
  "angle_line": "Not a lecture — a plot twist about why the thing helping you fall asleep is why you wake up tired.",
  "angle_authenticity": 9,

  "sources": [
    {
      "url": "https://news.umich.edu/...",
      "outlet": "University of Michigan / JAMA Pediatrics",
      "tier": 1,
      "role": "origin"
    },
    {
      "url": "https://www.sciencedaily.com/...",
      "outlet": "ScienceDaily",
      "tier": 2,
      "role": "corroboration"
    }
  ],
  "verification": "Tier 1 origin (JAMA Pediatrics) · 2 independent outlets · no COI flags",
  "caveats": "Self-reported survey data; correlation not causation.",

  "score": 8.4,
  "score_breakdown": {
    "audience_fit": 9,
    "source_strength": 9,
    "freshness": 7,
    "hook_potential": 8,
    "mission_fit": 8,
    "angle_authenticity": 9
  },

  "generated": []
}
```

### Field reference

**Identity & status**
- `id` — stable unique key, `YYYY-MM-DD-slug`. Everything (picks, generated assets, journal entries) points at this.
- `status` — pipeline state: `new` → `reviewed` → `picked` → `generated` → `shipped`, or `dismissed`. Drives the feed's "already dealt with" states.
- `pinned` — `true` once picked/generated; pinned records are EXEMPT from bumping until `shipped` or `dismissed`.
- `first_seen` / `last_updated` — ISO 8601 UTC. A story seen at 7am may rise by noon as coverage grows; update `last_updated`, keep `first_seen`.

**The story**
- `headline` — working title for the USER (punchy), not the outlet's SEO headline.
- `summary` — exactly 1–2 sentences. Written fresh in plain language. NEVER copied or lightly reworded from the source.
- `category` — single primary bucket (sleep, stress, gut, fitness, mind, food, social, ...).
- `topic_tags[]` — for filtering the feed later.

**Angle layer** (the wellness twist as data)
- `angle_tag` — `native` | `bridge` | `stretch`.
- `angle_line` — one-sentence pitch: the actual wellness read to lead or close with.
- `angle_authenticity` — 1–10, "is this bridge honest or forced." Low + `stretch` ⇒ usually cut (see scoring gate).

**Sourcing & verification**
- `sources[]` — list. Each: `url`, `outlet`, `tier` (1/2/3 per the pack rubric), `role` (`origin` | `corroboration` | `lead`). Social/influencer entries are `lead` and never carry a factual claim alone; the cited `origin` does.
- `verification` — the vetting verdict line, shown on the card.
- `caveats` — study limits ("in mice", small n, correlation≠causation). Lives at record level so generation can't lose it.

**Scoring**
- `score` — 0–10, one decimal. The feed's sort key.
- `score_breakdown` — per-dimension (the pack's scoring dimensions + `angle_authenticity`). Powers the dropdown "why this scored this" and learning-loop calibration.

**Generation tracking**
- `generated[]` — what's been produced from this story. Each: `{ "component": "script", "path": "workspace/finals/2026-06-12-cannabis-sleep.md", "created": "..." }`. Lets the feed show "script ✓ · captions ✗" and prevents accidental regeneration.

## Rules the writer (discovery) must follow

1. Sort `stories[]` by `score` descending. Within equal status, pinned first.
2. Enforce the cap: if a new story's score beats the lowest UNPINNED live story and the live count is at `feed_cap`, move the loser to `archive.json` (set its `status` if not already terminal) and add the newcomer.
3. Never delete — bump to archive.
4. Pinned (`picked`/`generated`, not yet `shipped`/`dismissed`) never get bumped, even above the cap.
5. Dedup by underlying story across runs (and against archive): same study/event ⇒ one record, best source as `origin`, others as `corroboration`; update `last_updated` rather than creating a duplicate.
6. Keep `meta` counts accurate.

## Rules the reader (HTML / Supabase) must follow

- **Lean card** by default: `headline`, `summary`, `angle_tag` + `angle_line`, `score`, `sources` (as links), and a pick action.
- **Dropdown arrow** per card expands to: `score_breakdown`, `verification`, `caveats`, full `sources[]` with tiers/roles. Collapsed by default — clean to scan, full reasoning for training.
- Render from data only; never invent fields not present.
- Treat the file as read-only state (the HTML renderer displays; it doesn't rewrite `feed.json`). Status changes come from the engine, not the static page — until/unless a hosted UI (deferred) adds write-back.
