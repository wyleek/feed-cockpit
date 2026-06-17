# Roadmap & Decisions Log

This file records design decisions made in planning so future sessions don't re-litigate them or drift. It is NOT a build instruction — it's the agreed plan. Build items are marked with status.

---

## NOW — current focus

**Generate the HTML feed version in its current state.** Render the existing engine's output as a clean, self-contained HTML feed page. Everything below this line is DEFERRED — do not build unless the user reopens it.

---

## DECIDED (locked — do not re-litigate)

### The pivot: trending-first, wellness-angled
- The show is a **news page with a wellness twist**, NOT a wellness page chasing news.
- Discovery is two-stage: (1) find top/trending stories generally, (2) an **angle pass** that finds the honest wellness read.
- Wellness "dosage" is LIGHT and variable — sometimes the twist is the whole video, sometimes a one-line closer. Lean lighter than a pure wellness frame.

### Angle spectrum (replaces a hard wellness gate)
Every story tagged one of:
- `native` — already wellness; lead with it straight.
- `bridge` — one honest step to a wellness read (heat wave → sleep/mood).
- `stretch` — forced/contorted ("election → cortisol"); scores low, usually cut.
- Rule: **strict on authenticity, loose on dosage.** Bar is "is the angle real," not "is it big." `angle_authenticity` sub-score enforces this; it's the main defense against becoming the "everything is secretly cortisol" parody account.

### Sources (US-centric to start; user adds personal taste later)
Curated set, sorted by ROLE:
- **Breaking-news spine (trend detection):** AP, Reuters, BBC, NPR, Guardian, CNN
- **Receipts engine (citable origins):** STAT, The Conversation, Scientific American, New Scientist, NIH/NIMH/CDC, EurekAlert/ScienceDaily, Harvard Health/Johns Hopkins/Cleveland Clinic
- **Angle radar:** Vox (+ health desks above)
- **Detection layer (signal only, never cited):** Google News, Google Alerts, Google Trends
- Pull mechanism varies: clean RSS where it exists (NPR, Guardian, BBC, STAT, The Conversation, SciAm, New Scientist, NIH/CDC, EurekAlert/ScienceDaily); AP/Reuters/CNN via Google News queries (flaky RSS); Google News/Alerts/Trends + institutional health sites via standing searches.
- Known risk: receipts engine is science-heavy; if feed under-surfaces "big story → wellness twist," ADD a culture/general source — don't rework anything.

### Social / influencers — citation-clean rule
- Social is a **lead source, never a source of record.** A viral post = a tip. Engine traces to the verifiable origin and cites THAT.
- No citable origin → story may run only as "this is a trend/conversation," never as fact. (Same Tier-3 logic already in source-vetting.md.)

### Feed format (THE KEYSTONE — write `engine/feed-format.md` first when building the feed)
- **One `feed.json`** = the live feed, up to 20 ranked records (+ pinned ones above cap).
- **`archive.json`** (or archive folder) = bumped/dismissed/shipped stories. **Never delete.**
- At #21 boundary: new story out-scores #20 → bumped story → archive.
- **Picked/generated stories are pinned** — exempt from bumping until shipped or dismissed.
- `status` walks: `new → reviewed → picked → generated → shipped` (or `dismissed`).
- Record = one story (JSON). HTML renders records today; Supabase stores same records later. Same shape, different home = portability.

#### Record fields (agreed)
- Identity/status: `id` (slug+date), `status`, `first_seen`, `last_updated`
- Story: `headline` (for the user, punchy), `summary` (2 sentences, fresh, never copied), `category`, `topic_tags[]`
- Angle: `angle_tag` (native/bridge/stretch), `angle_line`, `angle_authenticity`
- Sourcing: `sources[]` each = `{url, outlet, tier (1/2/3), role (origin/corroboration/lead)}`; `verification` (verdict line); `caveats`
- Scoring: `score` (sort key), `score_breakdown` (per-dimension)
- Generation: `generated[]` each = `{component, path, created}`

#### HTML view (agreed)
- **Lean card** by default: headline, summary, angle, score, sources, pick action.
- **Dropdown arrow** per card → expands to score breakdown, vetting notes, caveats, full source list. Clean to scan; educational for training someone.

---

## DEFERRED (planned, NOT building yet — reopen explicitly)

### Discovery automation / all-day feed
- Google Alerts as free 24/7 listeners (BYO keywords — user must seed; NOT yet done).
- Scheduled headless cron runs (e.g. 7am/noon/5pm) — wake, ingest, vet, angle, score, append to feed, sleep. No standing agents/polling (token cost).
- Feed appends + dedupes across runs throughout the day.

### Angle-authenticity scoring detail
- How the engine mechanically decides native/bridge/stretch and where the cut line sits. (Conceptually agreed; mechanics unspecified.)

### Google Alerts keyword list
- The BYO trigger terms ("new study" + sleep/anxiety/burnout/gut, "breaking news" triggers). User to seed.

### Visual assets (3 rungs, talk before building each)
1. **Shot list** — engine suggests b-roll/image per script beat + search terms. Cheap, no new infra. (Best first rung.)
2. **Curated image directory** — user's tagged folder (sleep/stress/gym/phone/food); license-clean ONLY (own shots or Pexels/Unsplash-style). Engine matches shot list to it.
3. **Motion / advanced** — HyperFrames by HeyGen connector (already connected) for reel motion; carousel-builder skills. Each is a new modular component ("carousel for #3", "motion for #3").
- Image MCP (Pexels/Unsplash-style) as FILL-IN for what the directory lacks. Directory first, MCP second — affordable + consistent look.

### UI for partner/trainee (ladder)
- Rung 0 (NOW-ish): self-contained HTML feed file. ← current focus
- Rung 1: Supabase (connected) stores stories → Netlify-hosted page reads them → live URL, updates all day, ❤️ to flag picks.
- Rung 2: generate buttons in UI trigger the engine (real engineering + per-click cost; earned, not assumed).

### Journal / diary
- Append-only dated log: stories pulled, scores, picks, what Claude generated, edits made, voice learnings. Expansion of existing `workspace/learning/`. Triple duty: audit trail (trainee can see how decisions get made) + voice feedback memory + content history.
- Organized `assets/` folder tree (by date + by story).

### The "three-button" dream (north star)
1. Get sources → (feed.json + cron makes this a button)
2. Choose source → (ranked feed + hosted page makes this a click)
3. Generate → (already modular; basically exists)
- Past the buttons: auto-edit voice recording, sync audio to cuts, assemble finished video. **Different class of tool (video automation), hard + expensive — separate module, spec only once front of pipeline hums.** Named so architecture leaves room; not near-term.

### Voice (unchanged, still waiting on user)
- Voice files are SCAFFOLD. Workshop needs: 3–5 of user's real samples/transcripts + 2–3 creators to emulate (with what they like about each). Then rewrite voice-bible/lexicon/persona, add gold examples, let learning loop converge.

---

## Guiding principles (from the user, hold these)
- **Walk before run.** Ship current state; add features as bolt-on sections onto existing scaffolding.
- **Affordable + intentional.** No unnecessary parts, no standing/polling agents. Free listeners + scheduled processing + on-demand generation.
- **Everything cited.** Extends to visuals (license-clean) too.
- **Keep the human part human:** user records the script. Automate everything around that.
- **Nothing built so far needs tearing down** — every future feature is a new modular component or a new output format for the same structured story data. That's why engine/packs are split and generation is modular.
