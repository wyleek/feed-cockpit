# Generation: modular, generate only what's asked

One story can produce many assets, but generating all of them every time wastes effort and tokens. So generation is COMPONENT-BASED: produce only the component(s) the user requested. Never dump the full package unless they explicitly ask for "everything" / "the full package".

## Components (each independently requestable)

| Component | Trigger examples | What it is |
|---|---|---|
| `script` | "script for #3", "write #3", bare "generate #3" (default) | The 30–45s spoken script + its receipt beat + a short citation footer |
| `hooks` | "hooks for #3", "give me hook options" | 3 opening-line options, different angles |
| `overlays` | "overlays for #3" | Timestamped on-screen text incl. the citation overlay (needs/uses the script) |
| `captions` | "captions for #3", "IG caption for #3" | Per-platform captions, each carrying the source |
| `citation-block` | "receipts for #3", "sources for #3" | Full claim→source mapping + caveats |
| `package` | "full package for #3", "everything for #3" | All of the above — explicit opt-in only |

### Command parsing
- A bare **"generate #N"** with no component named → produce the **script only** (the keystone asset you record), then offer a one-line menu: *"Want hooks, overlays, captions, or the full receipts block for this too?"* This respects tokens — most days the script is all that's needed.
- If a component is named, produce exactly that. If several are named, produce those.
- If the request is ambiguous, ask one quick question rather than guessing big.

## Before writing ANY component

Read, from the active pack: `voice/persona.md`, `voice/voice-bible.md`, `voice/lexicon.md`, and `voice/examples/` (the gold examples are your strongest voice signal — imitate their rhythm over reasoning from rules). Then read the story's ACTUAL origin source, not just the digest summary — pull the specific stat, finding, and detail. Specificity is the difference between content and filler.

## Citation travels with every factual component
Whatever you generate, the receipts come with it — never strip them to save space:
- **script** → includes the spoken receipt beat (source named out loud, naturally) AND a short citation footer listing origin + the claims it makes.
- **captions** → each carries the source (link, or "source: {journal}, {date}" + "link in bio" where the platform punishes links — per `formats/captions.md`).
- **overlays** → include the citation overlay during the receipt beat.
- **citation-block** → the full version: origin (full citation + URL), accessible write-up, each claim mapped to where the source supports it, and any caveat the script glosses (study size, "in mice", correlation vs causation). If a caveat is significant enough that omitting it misleads, it goes INTO the script, not just here.

## Component specs

### script (30–45s)
Follow the pack's `formats/video-script.md` beat sheet. 75–115 words (~2.5 wps); state estimated read time at the top. Spoken-word rules from the voice bible apply absolutely (contractions, breath-group line breaks, no clause stacking). Delivery markers inline: *(beat)*, *(faster)*, **emphasis**. Receipt beat mandatory.

### hooks
3 options, ≤2 seconds spoken each, each a different angle (the stat / the question / the contrarian take). Log which one the user picks to `workspace/learning/` — picks train the voice.

### captions
One natively-written caption per platform in `pack.md` (never paste across platforms). Per `formats/captions.md`. Each adds something beyond the script; each carries the source.

## After generating

Run `engine/editor-pass.md` — but scoped to ONLY the components you generated (the editor pass knows how to scope). Save the pre-edit draft to `workspace/drafts/YYYY-MM-DD-{slug}.md` and the post-edit version to `workspace/finals/YYYY-MM-DD-{slug}.md`. Present only the final.
