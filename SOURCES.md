# Sources

## The paper

| Field | Value |
|---|---|
| Title | The Effect of Offset Correction and Cursor on Mid-Air Pointing in Real and Virtual Environments |
| Authors | Sven Mayer, Valentin Schwind, Robin Schweigert, Niels Henze (University of Stuttgart) |
| Venue | CHI '18 — Proceedings of the 2018 CHI Conference on Human Factors in Computing Systems, Montreal, 21–26 April 2018, paper 653, 13 pages |
| DOI | [10.1145/3173574.3174227](https://doi.org/10.1145/3173574.3174227) |
| ISBN | 978-1-4503-5620-6/18/04 (from the paper's copyright block, p. 1) |
| Copyright | "© 2018 Copyright held by the owner/author(s). Publication rights licensed to ACM." (p. 1) |
| Funding | German Research Foundation (DFG), Cluster of Excellence in Simulation Technology (EXC 310/2) and SFB/Transregio 161 project C04 (Acknowledgements, p. 9) |
| Full text used | Author copy, `https://nhenze.net/uploads/The-Effect-of-Offset-Correction-and-Cursor-on-Mid-Air-Pointing-in-Real-and-Virtual-Environments.pdf` — HTTP 200, 13 pages, PDF metadata title matches, downloaded to `/tmp` (never committed) |

Page numbers used throughout this repository refer to that 13-page author PDF.
An identical copy is linked from the first author's own publication list as
`http://sven-mayer.com/wp-content/uploads/2018/01/mayer2018vrpointing.pdf`.

### Second paper read in full (needed for the cross-paper claims on p. 6)

Sven Mayer, Katrin Wolf, Stefan Schneegass, Niels Henze. "Modeling Distant
Pointing for Compensating Systematic Displacements." CHI '15 LBW,
DOI 10.1145/2702123.2702319. Author copy at
`http://sven-mayer.com/wp-content/uploads/2017/03/mayer2015.pdf` — HTTP 200,
4 pages. Its Tables 1 and 2 are the ground truth for the ratios the CHI '18
paper quotes; both are reproduced in `src/paper_values.py` and checked in
`src/check_paper.py`.

## Artifact hunt

Everything below was executed on 2026-08-16. "Result" is what actually came
back, not what a link promised.

| # | Where I looked | What I looked for | Result |
|---|---|---|---|
| 1 | `https://doi.org/10.1145/3173574.3174227` | canonical landing page | **Blocked.** Fetch tool returns `url_not_accessible`; the redirect target `dl.acm.org` answers HTTP 403 to every non-browser client from this environment |
| 2 | `https://dl.acm.org/doi/10.1145/3173574.3174227` (supplementary / artifacts tab) | ACM supplementary material, badges | **Blocked, HTTP 403.** Could not be inspected; recorded in `UNVERIFIED.md`. Search-engine snapshots of the page show only the abstract and reference list, no artifact section |
| 3 | `https://dl.acm.org/action/downloadSupplement?doi=10.1145%2F3173574.3174227…` | supplement archive | HTTP 403 |
| 4 | The paper itself: data-availability statement | data/code statement | **None.** The paper has no data-availability, code-availability or ethics/preregistration statement. The only two artifact pointers in the whole paper are footnotes 1 and 2 (rows 5–6) |
| 5 | Footnote 1, p. 4: `github.com/interactionlab/htc-vive-marker-mount` | 3D models of the custom OptiTrack marker mounts | **Found, HTTP 200.** Live, MIT-licensed, contains the mount models and a bill of materials |
| 6 | Footnote 2, p. 5: `github.com/valentin-schwind/selfpresence` | the androgynous virtual hand models used in VR | **Found, HTTP 200.** Live |
| 7 | `https://sven-mayer.com/publications/` (first author) | data/code link for this paper | **None.** The entry for this paper links exactly three things: the PDF, a YouTube video, and the DOI. No repository, no dataset |
| 8 | `https://sven-mayer.com/?s=offset+correction` | any project page for the paper | No project page for this paper |
| 9 | `https://nhenze.net/` and `https://nhenze.net/data/` (last author's data page) | released datasets | **None for this paper.** The data page hosts one unrelated dataset ("Hit It!" touch events on mobile phones) |
| 10 | GitHub org `interactionlab` (full repository listing, 22 repositories) | a repository for this paper | **None.** The listing contains `htc-vive-marker-mount` (row 5), `pointing-in-vr-hands` (the CHI PLAY '18 avatar paper — Unity project only, no data), `Deictic-Pointing-in-VR` (the CHI '20 paper — has a dataset, different study), `hand-marker-labeling`, and 18 unrelated repositories |
| 11 | GitHub user `sven-mayer` (21 public repositories) | data/analysis code for this paper | **None** |
| 12 | GitHub user `valentin-schwind` (28 public repositories) | data/analysis code for this paper | **None** except `selfpresence` (row 6) |
| 13 | GitHub code/repository search, "mid-air pointing offset correction" | third-party or author reimplementation | No matching repository |
| 14 | Zenodo API, `"mid-air pointing" offset correction` | deposited dataset | **None** by these authors |
| 15 | OSF API (`/v2/nodes`, `/v2/search`), "mid-air pointing", "pointing" | project, dataset or preregistration | **None** by these authors |
| 16 | figshare API, "mid-air pointing offset correction" | dataset | **None** |
| 17 | DaRUS, the University of Stuttgart data repository | institutional deposit | **None.** 0 hits for `"mid-air pointing"` (the repository post-dates the paper) |
| 18 | arXiv API, exact title | preprint with ancillary files | **None.** 0 entries |
| 19 | Semantic Scholar API (paper `6a870821…`) | open-access PDF, linked artifacts | `isOpenAccess: false`, `openAccessPdf.status: CLOSED`, no artifact links |
| 20 | Papers-with-Code search | linked code | No result page (HTTP 302) |
| 21 | ResearchGate entry for the paper (`publication/324663429_…`) | supplementary files | **Blocked, HTTP 403** to non-browser clients. Search-engine snapshots of the page show the paper text and figures only; no data or code file is listed |
| 22 | YouTube video linked from the author page (`watch?v=Mu_8iJer2BM`) | the CHI video figure | Referenced by the authors' own page; from this environment the request returned HTTP 429 (rate limited), so its availability is **not verified** here |

### What that adds up to

Both artifacts the paper points at are alive eight years later, which is more
than most CHI 2018 papers manage — but neither is the study. **No pointing
data, no analysis code, no fitted model coefficients, and no questionnaire or
Unity material for either study has ever been published, at any of the 22
locations above.** The two live links are hardware mounts and hand meshes.

That matters more than usual here, because the paper's stated contribution is
a *model*: "we developed models to compensate systematic offsets" (Abstract).
The models are 8 fits of a 15-parameter polynomial per angle (4 ray casts × 2
environments × pitch and yaw). Not one of those 240 coefficients appears in the
paper or anywhere else, so the contribution cannot be applied by a reader even
in principle. The predecessor paper (Mayer et al. 2015) did print its
coefficients, in its Table 3 — 15 numbers per angle, "in 10⁻⁵", verified in the
PDF and re-implemented here in `src/mayer2015_model.py`.
