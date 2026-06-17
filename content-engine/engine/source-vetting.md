# Source vetting (runs before the user sees anything)

This is the layer that makes wide-net discovery safe. Every candidate the net catches passes through here BEFORE it can reach the digest. The job: decide "is this a real, trustworthy source?" and attach a verdict the user can trust at a glance, so they never have to open a junk article to find out it's junk.

Be strict. A wide net catches a lot of garbage — content farms, AI-generated SEO pages, predatory journals, brand surveys cosplaying as studies. When in doubt, reject. A smaller digest of verified stories beats a bigger one you can't trust; the entire premise of this pack is "wellness with receipts."

## Vet each candidate in this order

### 1. Trace to origin
Find the actual primary source behind the claim: the study, the dataset, the official announcement. If you can't find a real origin — only outlets citing each other or citing nothing — that's a major red flag. A claim with no traceable origin cannot be Tier 1 or 2.

### 2. Judge the publisher
Is the outlet credible?
- **Recognized journalism** with editorial standards and bylined authors who link sources → can be Tier 2.
- **Primary/authoritative origin** (peer-reviewed journal, government health/science agency, major university research office) → Tier 1, IF the journal is legitimate. Check predatory-journal signals: pay-to-publish with no real peer review, fake/odd impact metrics, journal name mimicking a famous one, publisher on known predatory lists.
- **Trend/culture outlet** (culture mags, social platforms, influencer posts) → Tier 3 at most. Can support "this is trending" framing only.

### 3. Smell test for slop (auto-reject signals)
A wide net WILL surface these — reject on sight:
- **Topic-salad articles** — content that wanders off-topic into unrelated filler (e.g., a "mental health" page that splices in sports-betting or crypto copy). Classic AI-content-farm tell.
- **No author, no date, no sources**, or a generic/throwaway domain with programmatic phrasing.
- **"Study" that's actually a brand's customer survey** or a single influencer's claim with nothing under it.
- **SEO-bait** stuffed with the same keyword phrase repeated unnaturally.
- **Re-skinned press release** with zero independent reporting AND no accessible underlying study.

### 4. Corroboration check
Do independent, credible outlets cover the same underlying finding? Multiple independent confirmations raise confidence and tier; a lone Tier-3 source with no corroboration cannot carry a factual health claim (cap per scoring's tier gate).

### 5. Claim-support check
Does the origin actually support the headline? Health journalism routinely overstates — "linked to" becomes "causes," a mouse study becomes a human finding. If the origin doesn't support the claim the story is selling, reject (or, if the GAP itself is the story, reframe it as a debunk and note that).

### 6. Conflict-of-interest check
Who funded it? Supplement/app/brand-funded work without independent replication gets flagged and, for this pack's purposes, usually rejected (see pack red flags). Disclose any COI in the verdict if the story survives.

## Output per surviving candidate

Attach a compact verdict (shown on the digest card so the user trusts the filter):

```
✓ Verified — Tier {1/2/3} · Origin: {journal/agency} · {N} independent outlets · {COI note or "no COI flags"}
```

Or, for rejects, log a one-line reason in the digest's "Cut but close" / rejection notes so the user has visibility into what the filter is doing (and can overrule it):

```
✗ {headline} — rejected: {content farm / no traceable origin / brand-funded survey / claim unsupported}
```

The user should be able to scan the digest and see not just the story, but that the engine already checked the receipts.
EOF