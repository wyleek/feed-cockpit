# Scoring config: {TOPIC NAME}

The engine's five dimensions (see `engine/scoring.md`) with this pack's weights. Weights must sum to 1.0.

| Dimension | Weight | This pack's interpretation |
|---|---|---|
| Audience fit | 0.30 | {What specifically makes YOUR audience stop scrolling} |
| Source strength | 0.25 | {Anything topic-specific about tiers} |
| Freshness | 0.15 | {How fast does this topic decay?} |
| Hook potential | 0.20 | {What kinds of hooks work for this audience} |
| Mission fit | 0.10 | {Restate the mission test in one line} |

## Topic-specific boosts/penalties

- {e.g., +1 if the story has a direct "do this differently today" takeaway}
- {e.g., −2 if it's fear-bait, even if accurate}

> Starting weights are a guess. The learning loop (`workspace/learning/`) will propose adjustments based on which stories the user actually picks.
