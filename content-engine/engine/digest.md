# Digest format

The digest is the user's daily review queue — the centerpiece of their workflow. They scan it in under two minutes, pick a story, and say "generate #N". Format consistency matters: same structure every day so their eyes know where to land.

Save to `workspace/digests/YYYY-MM-DD.md` AND present it in full in the conversation.

## Template

```markdown
# Content Digest — {Weekday, Month D, YYYY}
Pack: {pack name} · {N} candidates surfaced from {M} screened

## 1. {Punchy working headline — written for the user, not the audience} — ⭐ 8.7
**Summary:** {Two sentences max. What happened + why the audience would care.}
**Why this score:** {One line, including weakest dimension if relevant.}
**Source:** {Origin: outlet/journal, Tier N} → [link] {· Corroboration: Outlet A, Outlet B}
**✓ Verified:** {vetting verdict — e.g., "Tier 1 origin (JAMA) · 3 independent outlets · no COI flags"}
**Angle:** {One line: the hook you'd lead with on camera.}

## 2. ...
```

Order by score, highest first, 5–7 cards. After the cards:

```markdown
---
**Cut but close:** {1-2 stories that just missed on SCORE, one line each — gives the user veto insight into the filter}
**Rejected by vetting:** {anything the net caught but the vetter killed — "✗ {headline}: content farm / no traceable origin / brand-funded survey". Gives the user visibility into the credibility filter so they can overrule it.}
**Feed health:** {only if an anchor source appears dead}

Reply "generate #N" for the script, or name a component ("captions for #N", "hooks for #N").
```

## Rules

- Summaries are written fresh in plain language — never copied or lightly reworded from the source. Two sentences, hard limit.
- The **Angle** line is the most valuable thing on the card. It should make the user able to *see the video*. Write it in the spirit of the pack's voice (it's a pitch, not a script).
- Scores always come with the why. A bare number teaches the user nothing.
- Every card must have a working link. No link, no card.
- If the day is thin (<5 strong candidates), say so plainly at the top and show what's there. Don't pad.
