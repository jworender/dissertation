# Dean's Office Formatting Corrections, Manual Crosswalk, and Recommendations

This document records formatting directions received from the College of Sciences Dean's Office, compares them with the [*Old Dominion University Thesis and Dissertation Manual* (Fall 2025)](./odu-thesis-and-dissertation-manual-fall25.pdf), and identifies changes that would help future students using the College of Sciences LaTeX template.

The classifications used below are:

- **Manual requirement:** the requested change directly implements an explicit rule in the manual.
- **Stricter Dean's Office interpretation:** the request is compatible with the manual but is more restrictive than the options stated there.
- **Undocumented exception or conflict:** the request appears inconsistent with, or creates an exception to, the published manual.
- **Template implementation gap:** the template appears intended to satisfy the manual, but its LaTeX implementation does not cover the relevant layout case.

The Dean's Office has responsibility for final compliance review, so its case-specific directions must be followed even where the written manual permits other options or is ambiguous (manual, p. 7).

## Correction crosswalk

| Dean's Office direction | Manual basis | Classification | Dissertation implementation | Recommendation |
|---|---|---|---|---|
| Order numbered references by first citation rather than alphabetically. | The manual permits an approved journal or style-guide model to determine ordering and explicitly lists alphabetized, alphabetized-and-numbered, and non-alphabetized-and-numbered arrangements (p. 12, *Citations and References*, item 3). | **Undocumented exception or conflict.** The College required one of several arrangements that the university manual presents as permissible alternatives. | The IEEE bibliography configuration uses `sorting=none`, so references are numbered in order of first citation. | Make `sorting=none` the College of Sciences template default if citation order is always required. Alternatively, publish a College addendum stating that numbered College submissions must use citation order. The university manual should not present alphabetization as an unrestricted alternative if the colleges will reject it. |
| Remove Appendix B.1 through B.4 from the Table of Contents. | The appendix section says only that section headings within appendices should be bold when appendix headings are bold (p. 14). It does not create a TOC exception. The Dean's Office checklist says that major headings and first-level subheadings appear in the TOC (p. 22). | **Undocumented exception or conflict.** B.1--B.4 are the first internal heading level under Appendix B, so removing them is contrary to the checklist unless appendix subheadings are intended to be exempt. | A dedicated `\appendixsectionnotoc` command preserves B.1--B.4 as numbered headings in the appendix while suppressing only their TOC entries. Appendix B itself remains in the TOC. | Clarify in the manual and template whether internal appendix headings belong in the TOC. If they are excluded, provide a supported appendix-heading command that prints and numbers a heading without writing a TOC entry. Students should not suppress TOC entries globally because later appendices still need to appear. |
| Insert two double-line spaces between adjacent tables and figures. | A table or figure placed with text or other material must have at least two double spaces (four single spaces) above and below it (p. 13, *Tables and Figures: Placement*). | **Manual requirement** and **template implementation gap.** | The dissertation applies the template's `1.69cm` clearance to ordinary float separation and to LaTeX's separate float-page spacing registers. Large adjacent floats move to separate pages when both cannot fit with the required clearance. | Define one named float-clearance length in the template and apply it to `\intextsep`, `\textfloatsep`, `\floatsep`, `\@fpsep`, and `\@dblfpsep`. The last two are essential on pages containing only floats. Do not add manual `\vspace` commands between individual figure/table environments because LaTeX may move those floats away from their source locations. |
| Make every table's font size consistent with Table 5 (`tab:d001_stability`). | The manual allows tables, figures, and appendix material to vary in point size, but establishes a 10 point minimum (p. 11). The tables-and-figures section repeats the 10 point minimum (p. 13). It also says that a reduced table or figure must retain a normal-size title (p. 13). | **Stricter Dean's Office interpretation**, with an underlying **manual-compliance issue** caused by automatic scaling. | The original `\resizebox` produced different effective sizes: approximately 9.68 pt in Table 5 and 13.87 pt in Table 6. All 16 table bodies now use an explicit 10 pt font with 12 pt leading; captions remain at the normal document size. Width-dependent `\resizebox` scaling was removed. Wide tables were reflowed or divided into continued parts instead of being reduced below 10 pt. | Provide a template-level table-body style at 10 pt and discourage `\resizebox` for text-bearing tables. Use narrower column padding, wrapped `p{}`/`X` columns, landscape placement, or continued tables when necessary. Validate the effective font in the compiled PDF because a nominal LaTeX font declaration made before `\resizebox` does not guarantee the rendered size. |
| Reformat the RQ3 real-data frontier figure from a 2-by-3 matrix to a 3-by-2 matrix because its subfigures were too small and difficult to read. | Figures must be clearly legible and professionally presented, and text within a figure has a 10 point minimum (p. 13, *Tables and Figures*). The final checklist also requires general legibility and compliance with the figure-formatting rules (p. 22). | **Manual requirement** applied through a **case-specific Dean's Office legibility determination.** | `rq3_real_data_frontiers` now places two data panels per row in a 3-by-2 matrix; the five domain panels occupy the first five positions and the shared legend remains in the sixth. The square 12-by-12-inch source canvas and 180 dpi export make each data panel wider at the dissertation's final `\textwidth` placement, and the smallest explicit annotation font was raised from 9 to 10 point. | Design multi-panel figures for their final printed width, not only for notebook display. Prefer fewer columns when annotations, axis labels, or tick labels become compressed; export at adequate resolution; and inspect the figure on the compiled dissertation page with its caption before submission. |
| Leave a full double-space before and after every section heading, including headings that wrap to multiple lines. | The manual requires multi-line titles and subheadings themselves to be double-spaced and requires spacing before and after headings to be consistent (p. 10, *Structure: Chapters, Sections, and Headings*, items 3 and 6). It does not state an exact pre- or post-heading distance. | **Stricter Dean's Office interpretation** and **template implementation gap.** | Section headings are now typeset as normal multiline paragraphs with prohibited internal page breaks, preserving the template's original 5.5 inch title width and hanging indentation. This makes the explicit `0.42cm` skips begin before the first rendered heading line and after the final line. In the rebuilt PDF, the one-line Section 3.3 and two-line Section 3.4 examples both measure 40.8 pt above and below the heading; the wrapped heading's lines remain double-spaced. | Do not use a bottom-referenced `\vbox`, which causes extra heading lines to grow upward into the preceding space, or a top-aligned inline `\parbox`, which distorts the following space. Use a normal paragraph with a prohibitive interline page-break penalty, and test the measured space on both sides of wrapped headings. |
| Do not leave a section or subsection heading at the end of a page; move it to the next page only when fewer than two lines of following material would fit. | The manual says that a subheading at the bottom of a page must be followed by at least one line of text (p. 10, *Structure: Chapters, Sections, and Headings*, item 9). | **Stricter Dean's Office interpretation** of the manual's one-line minimum and **template implementation gap.** | The section and subsection macros use an exact remaining-page-height test and reserve 3.25 body baselines before placing a heading. This keeps the complete heading, its required following space, and at least two lines of subsequent material together without moving headings unnecessarily. After the final rebuild, all 91 numbered section/subsection headings, including Appendix B.1--B.4, have at least two rendered lines beneath them. Section 3.1 remains on the Chapter 3 opening page with ten following lines, and the earlier six-page expansion is avoided. | Use an exact page-space calculation that accounts for the preceding vertical skip. Avoid an approximate stretch-based test or source-specific `\newpage` commands: the former can create large blank areas, while the latter become stale after reflow. Audit the rebuilt PDF from the first heading to the last after any global spacing or float change. |
| Do not allow a single carried-over paragraph line to occupy a page by itself. | The manual does not explicitly state widow and orphan limits. Its heading rule addresses only a subheading at the bottom of a page (p. 10, item 9), not isolated paragraph lines. | **Stricter Dean's Office interpretation** and **template implementation gap.** | The template now assigns prohibitive widow, club, and display-widow penalties globally. The former single-line continuations after `ANSWER TO RQ3` and `FINAL STATEMENT` now contain five and four rendered baselines, respectively. A whole-document PDF audit found no body page with only one rendered text baseline. | Set widow and club controls in the template rather than repairing individual paragraphs with manual page breaks. Re-audit after any pagination change because preventing one widow can shift later chapters, floats, and appendix pages. |

## Requirements triggered by the table-font correction

Increasing tables that formerly used `\scriptsize` (normally 8 pt) to the required 10 pt can make them too tall for one page. The manual provides a specific continuation format for oversized tables (p. 13):

1. Give the complete table number and title only on the first page.
2. On later pages, show the table number and the word "Continued."
3. Repeat the necessary column headings.
4. Place the table's closing line only on its final page.

Future template versions should provide a documented continued-table environment that implements these rules automatically. Students should not solve an oversized table by scaling it below 10 pt.

## Why corrected floats may move

The manual permits tables and figures either on text pages or on separate pages (p. 13). LaTeX placement options such as `[tbh]` and `[p]` are preferences, not fixed coordinates. Changing any of the following can cause LaTeX to reconsider the remaining float queue:

- the height or width of a table after fixing its font size;
- the required gap between adjacent floats;
- whether an oversized table must continue on another page; or
- whether two figures still fit together on a float-only page.

Movement after a formatting correction is therefore expected and may cascade to later floats. Avoid forcing every float with `[H]`; use it only when exact placement is required and the resulting page still satisfies margins and spacing. After reflow, verify the manual's proximity rule: when possible, the first textual mention should be within 1.5 pages before the table or figure, or on the immediately following page (p. 13).

## Recommendations for future students

1. **Start with the current manual and any college-specific addendum.** The committee approves content and disciplinary style, but the Dean's Office performs the final compliance review.
2. **Treat 10 pt as a rendered minimum.** Do not assume that text entered at 10 or 12 pt remains that size after scaling.
3. **Keep captions at the normal document size.** Reduce or reflow table bodies without shrinking their titles.
4. **Use one table-font macro throughout the project.** Local `\small`, `\footnotesize`, `\scriptsize`, and `\resizebox` commands make consistency difficult to audit.
5. **Use structural table fixes before scaling.** Adjust column padding, allow wrapping, use landscape orientation when appropriate, or continue the table across pages.
6. **Configure both text-page and float-page separation.** Standard `\floatsep` alone does not control the space between floats on a float-only page.
7. **Expect pagination changes after global formatting corrections.** Rebuild enough times for the TOC, lists, citations, and cross-references to stabilize, then visually inspect the PDF.
8. **Record case-specific Dean's Office directions.** When a request narrows or contradicts the published options, preserve the direction and the manual citation so later students and template maintainers can distinguish policy from implementation.
9. **Test wrapped headings.** Confirm that the heading stays on one page and that the required post-heading space begins after its final line, not after the first line's baseline.
10. **Keep headings with following material.** Use a template-level space reservation rather than page-number-specific breaks, then repeat the heading audit after pagination changes.
11. **Prevent paragraph widows and orphans globally.** Do not use manual page breaks to repair isolated final lines; they become stale when earlier content changes.
12. **Design multi-panel figures at their final dissertation width.** A layout that looks clear in a full-size notebook may become unreadable when reduced to `\textwidth`; reduce the number of columns, retain at least 10 point figure text, and inspect the compiled page before submission.

## Suggested College of Sciences template changes

- Default numbered IEEE references to `sorting=none`, or document the permitted alternatives explicitly.
- Add `\appendixsectionnotoc{...}` (or an equivalent supported command) if appendix subheadings are not supposed to appear in the TOC.
- Define and document a single 10 pt table-body command applied automatically to `tabular`, `tabularx`, and any supported multipage table environment.
- Remove examples that use `\resizebox{\textwidth}{!}` around text-bearing tables.
- Apply the prescribed float clearance to float-only pages as well as ordinary text pages.
- Provide a compliant continued-table example with repeated headings and the closing rule only on the final page.
- Replace the numbered-section heading's inline `\parbox` with a normal multiline paragraph that cannot break internally, so pre- and post-heading skips are measured from the correct rendered lines.
- Add a common keep-with-next-space test to numbered and unnumbered section and subsection commands so headings cannot be stranded at page bottoms.
- Set template-level widow, club, and display-widow penalties to prevent isolated paragraph lines.

## Manual sections consulted

- *Review by Dean's Office*, p. 7.
- *Structure: Chapters, Sections, and Headings*, p. 10.
- *General Document Formatting Requirements*, pp. 10--12.
- *Citations and References*, p. 12.
- *Tables and Figures*, pp. 13--14.
- *Appendices*, pp. 14--15.
- *Dean's Office Checklist*, p. 22.
