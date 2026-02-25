# Presentation Audit: `Jason_Orender_Dissertation_Proposal_Rev_A.pptx`

## Scope
This audit compares `drafts/Jason_Orender_Dissertation_Proposal_Rev_A.pptx` against the dissertation sources in this repository (`main.tex` + chapter files) for consistency and completeness.

Method used:
- Extracted slide text from the PPTX into `documentation/_presentation_revA_extracted.txt`.
- Cross-checked claims, terminology, workflow order, and timeline with current chapters.

## Findings (Ordered by Severity)

### 1) High: Pipeline step descriptions are internally swapped/inaccurate on the "Proposed Solution" slide
- Evidence (slides): `documentation/_presentation_revA_extracted.txt:63`, `documentation/_presentation_revA_extracted.txt:64`, `documentation/_presentation_revA_extracted.txt:66`
- Evidence (dissertation): `main.tex:80`, `Chapters/07_rq3.tex:33`, `Chapters/07_rq3.tex:37`, `Chapters/07_rq3.tex:41`
- Issue:
  - Slide text under "Fit Sparse Model" describes compression.
  - Slide text under "Compress" describes model fitting via "gradient descent," which is inconsistent with the dissertation framing of sparse fit then post-fit rule compression.
- Impact: Core method flow can be misunderstood in committee review.
- Recommended fix: Rewrite slide to exactly match the 3-stage order: `Rectify -> Fit sparse model -> Compress (anytime logic polishing)`.

### 2) High: Conclusion coverage is incomplete relative to dissertation conclusion chapter
- Evidence (slides): Deck ends with contributions/future work/timeline/thanks (`documentation/_presentation_revA_extracted.txt:376`, `documentation/_presentation_revA_extracted.txt:382`, `documentation/_presentation_revA_extracted.txt:396`, `documentation/_presentation_revA_extracted.txt:422`).
- Evidence (dissertation): `Chapters/89_conclusion.tex:38`, `Chapters/89_conclusion.tex:55`, `Chapters/89_conclusion.tex:71`
- Issue: The deck lacks a dedicated final conclusions slide that reflects:
  - explicit contributions,
  - scope boundaries/limitations,
  - final integrated claim across RQ1/RQ2/RQ3.
- Impact: Presentation is weaker than manuscript on scientific rigor and bounded claims.
- Recommended fix: Add 1-2 closing slides for "Final Conclusions" and "Scope/Limitations" mirroring Chapter 89.

### 3) High: Future-work slide is now underspecified vs the dissertation's pre-defense plan
- Evidence (slides): `documentation/_presentation_revA_extracted.txt:382` onward
- Evidence (dissertation): `Chapters/88_futurework.tex:18`, `Chapters/88_futurework.tex:48`, `Chapters/88_futurework.tex:72`, `Chapters/88_futurework.tex:120`, `Chapters/88_futurework.tex:129`
- Issue: Slide content is still high-level (must-do/high-leverage/stretch) while the dissertation now defines:
  - explicit workstreams,
  - risk/mitigation,
  - decision gates and required outputs.
- Impact: Committee may not see the stronger execution discipline now documented.
- Recommended fix: Replace current future-work slide with a concise workstream+gate summary aligned to Chapter 88.

### 4) Medium: RQ1 wording in slides omits "lag attribution"
- Evidence (slides): `documentation/_presentation_revA_extracted.txt:17`, `documentation/_presentation_revA_extracted.txt:123`, `documentation/_presentation_revA_extracted.txt:132`
- Evidence (dissertation): `Chapters/04_resquestions.tex:9`
- Issue: Slides currently say "feature attribution" while dissertation question is "feature and lag attribution."
- Impact: Reduces alignment with the dissertation's longitudinal emphasis.
- Recommended fix: Update all RQ1 instances to "feature and lag attribution."

### 5) Medium: RQ3 statistical framing in slides leads with p-values, but dissertation framing is equivalence-first
- Evidence (slides): `documentation/_presentation_revA_extracted.txt:331`, `documentation/_presentation_revA_extracted.txt:360`
- Evidence (dissertation): `Chapters/07_rq3.tex:76`, `Chapters/88_futurework.tex:80`
- Issue: The slide emphasizes paired t-test p-values first, whereas the dissertation explicitly states equivalence framing is the right basis for "no material degradation" claims.
- Impact: Can invite methodological criticism during questioning.
- Recommended fix: Reframe slide title and narrative to lead with equivalence margin/TOST and treat p-values as secondary context.

### 6) Medium: Administrative metadata inconsistencies (names/title/date context)
- Evidence (slides): `documentation/_presentation_revA_extracted.txt:6`, `documentation/_presentation_revA_extracted.txt:7`
- Evidence (dissertation): `main.tex:43`, `main.tex:65`, `main.tex:66`
- Issues:
  - Committee name appears as "Yoahang Li" on slide (manuscript uses "Yaohang Li").
  - Slide uses "Dr. Nguyen Yet" while manuscript lists "Yet Nguyen."
  - Deck title includes "Anytime Rule Compression" while manuscript title currently ends with "ANYTIME RULE" (possible manuscript truncation or intentional abbreviation).
  - Slide date is `2/28/2026`; verify this is the intended presentation date given other dated milestones.
- Impact: Avoidable credibility and formatting issues.
- Recommended fix: Normalize names/title/date across deck and manuscript front matter.

### 7) Medium: Related-work representation in slides is thin relative to manuscript depth
- Evidence (slides): mostly one high-level slide (`documentation/_presentation_revA_extracted.txt:44`)
- Evidence (dissertation): `Chapters/03_relatedwork.tex` (multiple method families + positioning)
- Issue: Deck does not visibly show the expanded baseline taxonomy now present in the dissertation (lasso/elastic-net, grouped/ordered, rule-learning, dependence-aware alternatives).
- Impact: Can make novelty/positioning look weaker than documented.
- Recommended fix: Add one compact "Related Work Positioning" slide with 4 method-family columns and where your pipeline differs.

### 8) Low: Source attribution in slides is sparse for quantitative claims
- Evidence (slides): result-heavy sections lack explicit source tags (e.g., RQ1/RQ3 metrics).
- Evidence (dissertation): chapters include detailed `\autocite` support.
- Issue: Claims are generally consistent, but slide-level provenance is not obvious.
- Impact: Reviewers may request on-the-spot source tracing.
- Recommended fix: Add small footer citations per result slide (e.g., prior paper key + dataset source).

## Consistency Checks That Passed
- RQ1 synthetic and real-world numeric tables in slides are consistent with `Chapters/05_rq1.tex` (including the 100--200x comparator runtime statement).
- Core milestone dates for prospectus/defense/graduation are aligned with Chapter 88 targets (`23 Feb 2026`, `17 Jul 2026`, `28 Aug 2026`).
- RQ2 PoC scope language (zero-threshold arcsin tractability) is directionally consistent with the manuscript.

## Recommended Slide Update Plan (Minimal)
1. Fix the end-to-end pipeline slide semantics/order.
2. Add one "Final Conclusions + Scope Boundaries" slide from Chapter 89.
3. Replace current future-work slide with Chapter 88 workstreams + decision gates.
4. Normalize RQ1 wording to "feature and lag attribution."
5. Reframe RQ3 stats slide to equivalence-first messaging.
6. Correct committee names/title/date metadata and add source footers on quantitative slides.

## Notes
- This audit used extracted slide text. Office equation objects are only partially recoverable via raw XML text extraction, so formula rendering should still be visually spot-checked in PowerPoint.
