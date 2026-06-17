# Discovery: cast a wide net

Goal: surface as many genuinely relevant candidate stories as possible from across the open media landscape — NOT from a fixed list of feeds. We search by topic, catch everything that mentions it, and let the vetting layer (`engine/source-vetting.md`) decide what's trustworthy before anything reaches the user.

Why wide-net over a fixed feed list: a hardcoded source list goes stale, misses anything outside it, and bakes in yesterday's idea of who's worth reading. Searching by topic catches the story wherever it broke — including outlets we've never seen. The cost is that a wide net also catches slop (content farms, AI-generated SEO pages, brand surveys dressed as studies). That's expected and fine, because nothing skips vetting.

## Inputs
- The active pack's `sources.md` — now primarily a list of SEARCH TOPICS + the tier rubric + red flags (not an allowlist)
- The active pack's `pack.md` — topic boundaries and audience (keeps the net on-mission)
- Last 7 days of `workspace/digests/` (for deduplication)

## Procedure

1. **Run the net.** Execute the pack's standing search queries with web search, past-week restricted. Cast wide — variant phrasings, "new study X", trend terms, plus a few fresh angles based on what's clearly current. Aim to pull 20–40 raw hits; over-collecting here is good, because vetting will cut hard.
2. **Optional anchor sweep.** If the pack lists a few trusted "anchor" sources, check them too — they're a reliable floor on a thin day, NOT a ceiling. The net is primary.
3. **Trace each hit to origin.** A blog post about a Stanford study is not the source — the study is. Find the actual study / primary report / official announcement. Record both (origin + accessible write-up). This feeds vetting.
4. **Hand EVERY surviving hit to vetting.** Run `engine/source-vetting.md` on each candidate. Vetting rejects junk, assigns a dynamic tier, and attaches a one-line credibility verdict. Only vetted-pass candidates continue.
5. **Deduplicate** (after vetting, so the highest-quality version of a story wins):
   - Same underlying story/study from multiple outlets → ONE candidate, highest-tier source as primary, the rest logged as corroboration (corroboration is a positive signal).
   - Against the last 7 days of digests → drop repeats unless there's a genuinely new development.

## Output
Pass vetted, deduped candidates (with origin link, publisher, assigned tier, corroboration count, and the vetting verdict) to scoring (`engine/scoring.md`), then format per `engine/digest.md`.

Target: 20–40 raw hits → vetting → 8–15 survivors entering scoring → top 5–7 in the digest. If the net comes up thin after vetting, present what passed and say the pool was thin — never lower the vetting bar to fill space, and never invent.
