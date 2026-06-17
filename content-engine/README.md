# Content Engine — Setup & Daily Use

A Claude Code skill that turns trending stories into ready-to-record, fully-cited short-form content packages — in your voice, for any topic.

## Install (one time, ~2 minutes)

1. Make sure Claude Code is installed and working (run `claude` in your terminal — if it opens, you're good).
2. Put this folder where skills live:
   ```bash
   mkdir -p ~/.claude/skills
   cp -r content-engine ~/.claude/skills/content-engine
   ```
3. That's it. Claude Code watches the skills folder, so it's live. (If you created `~/.claude/skills` for the first time just now, restart Claude Code once.)

## Daily workflow (~20 min total)

```
you:    claude "run discovery"
engine: → casts a wide net by topic, VETS every catch for credibility,
          then shows a scored digest of verified stories (summary, score + why,
          source tier, ✓ verification verdict, link, suggested angle)
you:    "generate #3"          ← gives you just the SCRIPT (the thing you record)
        "captions for #3"      ← or just the captions
        "hooks for #3"         ← or just hook options
        "full package for #3"  ← or everything, only if you ask
you:    record it, post it
```

You generate only what you want, so you're never burning effort on assets you won't use. Every component still carries its own receipts — a lone script keeps its on-camera source callout, a lone caption keeps its source link.

Other things you can say: "show me today's digest", "new topic pack for eco news", "what have you learned about my voice lately".

## How the pieces fit

```
content-engine/
├── SKILL.md            ← the brain: tells Claude what to do when
├── engine/             ← HOW (topic-agnostic): wide-net discovery, source
│                          vetting, scoring, digest, modular generation, editor
│                          pass. You rarely touch these.
├── packs/
│   ├── _template/      ← clone this to launch a new topic/channel
│   └── wellness-genz/  ← your first pack: sources, scoring weights, VOICE
└── workspace/          ← daily outputs: digests/, drafts/, finals/, learning/
```

**The engine is generic. Packs are swappable.** New channel = copy `_template`, fill in topic + sources + voice, done. The engine never changes.

## ⚠️ Before this sounds like you: the voice workshop

The wellness-genz pack runs today on scaffold defaults (marked `STATUS: SCAFFOLD` / `TODO` in the voice files). It'll be *competent* immediately, but it becomes *yours* when we do the voice workshop:

1. Collect 3–5 samples of your real writing/transcripts + 2–3 creators to emulate (with notes on what you like about each).
2. Rewrite `voice/voice-bible.md`, `lexicon.md`, and `persona.md` from the samples.
3. Generate test scripts until they pass your "would I actually say this?" check.
4. Put 2–3 approved scripts in `voice/examples/` — these gold examples are the strongest voice signal in the system.

After that, the learning loop takes over: every edit you make before recording teaches the system, and it proposes voice-file updates when it spots patterns.

## First-run checklist

- [ ] Run `claude "run discovery"` once — it casts the wide net, vets each catch, and shows you which stories passed (and which it rejected, so you can see the filter working)
- [ ] Review the first digest critically: are scores AND verification verdicts matching your instincts? Say so either way — it calibrates
- [ ] Generate just one component (try `script for #1`) and edit it ruthlessly — feed the edits back ("here's my edited version") to seed the learning loop
- [ ] Schedule the voice workshop (bring samples!)

## Later: full automation

Once output quality is dialed in, add a scheduled job (cron / launchd / Task Scheduler) that runs `claude -p "run discovery"` early each morning, so the digest is waiting when you wake up. Get the voice right first — automating too early just produces mediocre content faster.
