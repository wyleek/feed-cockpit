# Scoring

Goal: rank candidates so the user can pick in seconds. Scores must be *explainable* — every score comes with a one-line "why" because the user reviews these daily and needs to trust (and calibrate) the system's judgment.

## The five dimensions

Score each candidate 1–10 on each dimension. The pack's `scoring.md` defines the weights and any topic-specific interpretation of each dimension.

1. **Audience fit** — Would the pack's target audience stop scrolling for this? Judge against the audience profile in `pack.md`, not your own taste.
2. **Source strength** — Tier of the *origin* source (per the pack's `sources.md` tier definitions), plus corroboration. A Tier 1 origin with multiple independent write-ups scores top marks. A single Tier 3 source caps this at 4.
3. **Freshness** — Published in the last 24h scores high; over a week old needs a reason (e.g., a study that's only now getting attention). News content decays fast.
4. **Hook potential** — Is there a surprising stat, a counterintuitive finding, a "wait, what?" angle, or a direct stake for the viewer? Stories without a hookable angle make weak short-form video regardless of importance.
5. **Mission fit** — Does it serve the pack's stated mission and tone (e.g., constructive/positive framing)? A perfectly accurate story that's pure doom may not fit a feel-good mission; the pack defines this.

## Computing the score

Weighted average per the pack's weights, displayed as a single score out of 10 with one decimal (e.g., **8.3**). Alongside the number, always include:

- The one-line **why** ("Strong RCT + cortisol hook, but story is 5 days old")
- The dimension that's dragging it down, if any — this is what the user most wants to know

## Hard gates (apply before weighting)

- **Tier gate:** factual health/science claims with only Tier-3 sourcing → cap total score at 4.0 and label "trend-only framing required".
- **Claim-support gate:** if the origin source doesn't support the headline claim, cut the story entirely (it will have been screened in discovery, but verify when scoring borderline candidates).
- **Dupe gate:** previously covered without new development → cut.

## Calibration

When the user consistently picks lower-scored stories over higher-scored ones, that's signal, not noise. Note which dimension mispredicted their choice in `workspace/learning/` and propose a weight adjustment to the pack's `scoring.md` after 3+ occurrences.
