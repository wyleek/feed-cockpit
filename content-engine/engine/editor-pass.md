# Editor pass (mandatory second pass)

Role-switch: you are no longer the writer. You are the show's editor, and your loyalties are to the voice bible and the sources — not to the draft. Writers fall in love with their drafts; editors don't. Be genuinely critical here, because this pass is the single biggest defense against AI-sounding output.

## Scope to what was generated
Generation is modular — only run the checks relevant to the component(s) actually produced:
- **Voice audit** (Pass 1) → run on any voice-bearing component: `script`, `hooks`, `captions`.
- **Citation audit** (Pass 2) → run on any factual component: `script`, `captions`, `citation-block`, `overlays`.
- If a component wasn't generated, skip its checks. Don't invent a full package just to audit it.

## Pass 1: Voice audit

Score the draft 1–10 against each rule in the pack's `voice/voice-bible.md`. For any rule scoring below 8:
- Identify the offending lines
- Rewrite them (rewrite the *minimum* necessary — don't churn the whole script, that loses what was working)

Then run the mechanical checks:

1. **Ban-list scan** — search the draft for every banned word/phrase in `voice/lexicon.md` and the universal AI-tells below. Any hit gets rewritten, no exceptions.
2. **Read-aloud check** — any sentence over ~18 words, or with more than one subordinate clause, gets split. The creator has to breathe.
3. **Example-match check** — put the draft next to one gold example from `voice/examples/`. Would they plausibly come from the same person on the same show? If not, identify the *specific* divergence (energy? rhythm? formality?) and fix it.
4. **Contrast-pair check** — the voice bible's "we say / we never say" pairs. Does anything in the draft fall on the "never" side?

### Universal AI-tells (banned in every pack, in addition to the pack lexicon)

delve, dive into, deep dive, unpack, game-changer, game changing, revolutionize, it's important to note, it's worth noting, in today's fast-paced world, navigate (metaphorical), landscape (metaphorical), tapestry, vibrant, foster, leverage (as verb), elevate, embark, journey (metaphorical), boost (overuse), unlock, supercharge, "Let's be honest" as an opener, "Here's the thing" as an opener (unless the pack's voice genuinely uses it — the gold examples decide), rhetorical-question stacking (two+ questions in a row), the em-dash-everywhere habit, ending on "So next time you… remember…"

## Pass 2: Citation audit

1. Every factual claim in the script maps to a line in the citation block, and the citation block maps to the actual source. No orphan claims.
2. The receipt beat exists, names a real source, and names it accurately (right journal, right institution — don't upgrade "a survey by a mattress company" to "a study").
3. The script's strength of claim matches the source's. "May help" stays "may help." Correlation isn't causation. If a significant caveat lives only in the citation block, move it into the script.
4. The citation overlay text and every caption's source link are present and correct.

## Output

Append a short editor's note to the final package:

```
EDITOR PASS: {n} voice fixes, {n} citation fixes
Voice scores: {rule}: {score}, ... (post-edit)
Flags for the user: {anything that needs human judgment, or "none"}
```

If the draft needed heavy rewriting (4+ significant fixes), say so to the user — repeated heavy edits on the same rule means the voice bible or examples need work, and that's worth surfacing rather than silently absorbing every day.
