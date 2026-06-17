---
name: content-engine
description: Run the daily short-form content pipeline — discover trending stories, score and summarize them into a review digest, then generate fully-cited video scripts, overlays, and platform captions in the creator's voice. Use this skill whenever the user asks to find stories, run discovery, build or show the digest, generate content from a story (e.g. "generate #3"), write a script, make today's content, create captions, or anything related to their content pipeline, topic packs, or voice — even if they don't say "content engine" explicitly.
---

# Content Engine

A topic-agnostic pipeline that turns trending stories into ready-to-record short-form content packages. The engine is generic; everything topic-specific (voice, sources, scoring weights, audience) lives in a swappable **topic pack** under `packs/`.

> **Read `ROADMAP.md` first.** It records locked design decisions and what's deferred. The current focus is generating the HTML feed; many planned features (all-day cron, visual assets, hosted UI, journal) are DEFERRED — do not build them unless the user reopens them.

## Core principle: nothing ships without a receipt

Every story must trace to a credible source, every script includes a citation beat, and every caption links the source. If a claim can't be sourced at Tier 1 or Tier 2 (defined in the pack's `sources.md`), it gets cut or explicitly framed as a trend/opinion. This is non-negotiable because the content makes health and science claims to a real audience.

## The pipeline

```
DISCOVER ──> SCORE ──> DIGEST ──> [user picks] ──> GENERATE ──> EDITOR PASS ──> PACKAGE
```

The user is the editorial gate between digest and generation. Never auto-publish; the human picks the story and records the video themselves.

## Which pack to use

1. If the user names a pack ("use the eco pack"), use that one.
2. If only one pack exists in `packs/` (ignoring `_template`), use it.
3. Otherwise ask.

Always read the pack's `pack.md` first — it defines topic, audience, and mission, and everything downstream depends on it.

## Commands and what to do

### "Run discovery" / "find stories" / "what's trending"
Read `engine/discovery.md` and the active pack's `sources.md`, then cast a wide net by topic. Run EVERY catch through `engine/source-vetting.md` to verify credibility BEFORE it can reach the digest — this is what makes wide-net discovery safe. Output is a scored digest (see below) of vetted stories, saved to `workspace/digests/YYYY-MM-DD.md` and shown to the user.

### "Show me the digest" / "what have we got today"
If today's digest exists in `workspace/digests/`, present it. If not, run discovery first.

### "Generate #N" / "script for #N" / "captions for #N" etc.
Read `engine/generation.md`, the pack's full `voice/` folder, and the relevant `formats/` files. Generate ONLY the component(s) the user asked for — never the full package unless they say "everything"/"full package". A bare "generate #N" defaults to the script alone (plus its receipts) and offers a menu for the rest. Then **always** run the editor pass (`engine/editor-pass.md`), scoped to just what you generated, before showing anything. Save draft to `workspace/drafts/` and final to `workspace/finals/`.

### "New topic pack" / "set this up for [topic]"
Copy `packs/_template/` to `packs/<topic-name>/` and walk the user through filling it in, starting with `pack.md`, then `sources.md`, then voice files. Don't invent the user's voice — ask for samples or run a voice workshop.

### "Update the voice" / feedback on a script
Apply the user's edits, then check `workspace/learning/README.md` — every user edit is a signal. Log the diff and, if a pattern has appeared 3+ times, propose a specific addition to the pack's voice files. The voice bible is a living document that should converge on the user over time.

## Reference files — read before acting

- `engine/discovery.md` — how to cast a wide net by topic and dedupe candidate stories
- `engine/source-vetting.md` — how to verify each catch's credibility before it reaches the user
- `engine/scoring.md` — how to score stories using the pack's rubric
- `engine/digest.md` — the exact digest card format (the user reviews this daily; format consistency matters)
- `engine/generation.md` — the content package spec (script, overlays, captions, citation block)
- `engine/editor-pass.md` — the mandatory voice + citation QA pass
- `packs/<active>/...` — all topic-specific config

## Hard rules

1. **Never fabricate a story, statistic, study, or source.** If discovery comes up dry, say so and suggest widening the search — a thin digest is fine, an invented one is a betrayal of the whole premise.
2. **Never skip the editor pass.** A draft that hasn't been scored against the voice bible is not done.
3. **Citation beat is mandatory** in every script, and every caption carries the source link.
4. **Scripts are spoken-word.** They will be read aloud on camera by a human. Read `voice/voice-bible.md` spoken-word constraints every time.
5. **Tier-3-only sourcing cannot support a factual health/science claim.** It can only support "this is trending" framing.
