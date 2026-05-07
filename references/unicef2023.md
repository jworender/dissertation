# UNICEF Data Warehouse (UNICEF, 2023)

## Dissertation Alignment Context
The dissertation uses a three-stage longitudinal pipeline: critical-range rectification of lagged signals into {-1,+1} indicators, L1-regularized logistic feature-and-lag selection, and anytime rule compression that converts sparse coefficients into compact m-of-K rules.

## Outline Summary of the Dataset
1. **Dataset identity:** The UNICEF Data Warehouse is a public data-query and country-profile resource for indicators related to children and women.
2. **Primary access point:** The `dv_index` page is titled `Query Data - UNICEF DATA` and is part of UNICEF Data's monitoring site.
3. **Topical scope:** The site organizes data by topics such as adolescents, child and adolescent health, children with disabilities, climate and environment, early childhood development, education, gender equality, HIV/AIDS, maternal and newborn health, migration, mortality, child nutrition, child poverty, protection, and WASH.
4. **Country scope:** The page also organizes data by country and links country overviews, SDG progress data, civil registration and vital statistics data where available, and topic-specific country profile PDFs.
5. **Data structure relevance:** The warehouse provides cross-national indicator data with heterogeneous coverage across countries, topics, years, and measures.
6. **Dissertation use case:** In the dissertation, UNICEF functions as a cross-domain real-world dataset rather than as the central target domain.
7. **Boundary-condition role:** The dissertation uses the UNICEF case to show that rectification is not universally superior on raw discrimination; untransformed models can perform better when the target structure is less threshold-and-lag aligned.
8. **Interpretability role:** Even when raw discrimination is stronger, the transformed UNICEF model remains useful as an example of a sparser and more interpretable representation.
9. **Methodological caution:** The dataset motivates careful branch logic: if rectification loses held-out discrimination without enough attribution or compactness benefit, raw or hybrid representations may be the better default.
10. **External-validity role:** UNICEF broadens the empirical scope beyond synthetic, industrial-control, and radar datasets, helping define where the dissertation method weakens outside its target regime.

## Relevance to the Dissertation
UNICEF Data Warehouse (UNICEF, 2023) is relevant as a cross-domain real-world dataset used to test the dissertation's scope boundaries. It supports the claim that rectification benefits are conditional: transformed models may be sparser and easier to interpret, while raw models can retain stronger discrimination when the data-generating process is less compatible with critical-range assumptions.

## Dataset and Acquisition Notes

- Public data page: <https://data.unicef.org/dv_index/>
- Site title observed during this summary: `Query Data - UNICEF DATA`
- Site framing: UNICEF Data monitors the situation of children and women.
- Relevant access modes visible on the public page: data by topic, data by country, country overviews, SDG progress data, selected CVRS data links, and topic-specific country profile PDFs.
- Dissertation role: cross-domain real-world boundary case for transformed vs. untransformed sparse modeling.

## Elements from This Dataset to Use in the Dissertation
1. Use UNICEF as a boundary-condition example rather than as primary evidence of rectification dominance.
2. Report both discrimination and interpretability outcomes, since raw and transformed models can trade places depending on the metric.
3. Use the case to justify the dissertation's diagnostic branch rules for staying raw, rectifying, or using hybrid features.
4. Use the dataset's cross-domain character to strengthen the scope statement that threshold-and-lag alignment matters.

## Competitive Method Assessment
This is not a competing method. It is a dataset used to stress-test the dissertation pipeline outside the strongest threshold-mediated regime. Its main value is showing where raw sparse modeling can outperform rectified modeling on discrimination while rectification can still offer sparsity and interpretability benefits.

## Dissertation Citation Traceability

- Chapter: `Rectification Improves Sparse Longitudinal Selection (RQ1)`; Section: `Real-world evidence and interpretability tradeoffs`; Line: `Chapters/05_rq1.tex:377`; Relevance: Cited to support the statement that In the UNICEF case, untransformed models can achieve stronger raw discrimination metrics while transformed models remain substantially sparser and easier to interpret.
