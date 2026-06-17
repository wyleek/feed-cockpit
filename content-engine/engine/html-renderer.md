# HTML feed renderer

Turns `workspace/feed.json` into a shareable, self-contained `workspace/feed.html` — a review console for picking stories. This is the NOW deliverable (see ROADMAP.md); the hosted Supabase/Netlify version is deferred.

## What it is
A single HTML file, no build step, no dependencies (fonts from Google Fonts CDN). Opens by double-click (file://) or can be sent to a partner/trainee as-is. Renders the feed exactly per `engine/feed-format.md`:
- **Lean cards** ranked by score (pinned first): rank, score, headline, summary, the angle tag + line, source chips, verification line, and a "Pick & copy command" button.
- **Angle-spine signature:** left edge of each card is colored by `angle_tag` (native = sage, bridge = amber, stretch = stone), so the day's angle texture is scannable at a glance.
- **Dropdown arrow** per card expands to the score breakdown (animated bars), caveats, and full sources with tiers/roles. Collapsed by default — clean to scan, full reasoning for training someone.
- **Pick** copies `generate #<id>` to the clipboard to run back in Claude Code (the static page doesn't write state — see feed-format reader rules).

## How to (re)generate it
The data is EMBEDDED in the HTML (inline `const FEED`) so the file works offline and when shared. To refresh after a discovery run:
1. Read `workspace/feed.json`.
2. Open `workspace/feed.html`, find the `const FEED = /* feed.json */ {...};` block, and replace the object with the current feed.json contents verbatim.
3. Nothing else changes — the renderer reads whatever is in FEED.

Keep the embedded snapshot and feed.json in sync. (When the hosted version lands, the page will fetch from Supabase instead of embedding, and this sync step goes away.)

## Why embedded, not fetch()
Opening an HTML file from disk and `fetch()`-ing a sibling `feed.json` is blocked by browser file:// security (CORS). Embedding the data is what makes the file truly portable and shareable. The hosted version (deferred) will serve both over HTTP and can fetch normally.

## Design tokens (so refreshes stay on-brand)
Porcelain bg `#F4F5F2`, ink `#1A211D`, sage `#5C7D6A` (native/primary), amber `#C2912F` (bridge), stone `#A2A8A1` (stretch), clay `#BD6B3E` (score). Display: Newsreader; body: Inter; data/mono: IBM Plex Mono. The spine + mono score figures are the signature — keep them.
