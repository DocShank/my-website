# NeuroAtlas MRI

NeuroAtlas MRI is a non-commercial browser-based educational prototype for
learning cross-sectional neuroanatomy. It combines a standardized MNI152 T1
template with AAL regional labels, JHU ICBM-DTI-81 white-matter labels, and
selected Harvard-Oxford subcortical labels.

- Live application: https://docshank.github.io/my-website/neuroatlas/
- Manuscript release: NeuroAtlas MRI Precision v7.1
- Current feature generation: Precision v7
- Rendering library: NiiVue 0.62.1

The application is intended for education only. It does not contain patient
data, process clinical scans, or provide diagnostic output.

## Reproducible deployment

GitHub Actions reconstructs the protected viewer from the repository's patch
sequence, verifies the generated page hash, downloads the atlas resources from
pinned upstream revisions, verifies every data-file checksum, builds validated
atlas landing points, and deploys the resulting static site to GitHub Pages.

Precision v7 changed only the Cross-Section Teacher relative to the version 6
checkpoint. It increased label density, preserved full structure names,
improved label placement, increased export resolution, added a small watermark,
and added direct image download. The core multiplanar viewer, search, crosshair,
atlas selection, and teaching-panel behavior remained in place. Precision v7.1
adds provenance, licensing, and wording corrections without changing anatomical
logic or figure-generating behavior.

## Licences and attribution

Original NeuroAtlas MRI application code is released under the BSD 2-Clause
License in [LICENSE](LICENSE). Third-party software and neuroimaging resources
retain their own terms. Exact sources, commit identifiers, checksums, citations,
and license notices are recorded in
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

The JHU atlas is included for non-commercial educational use under the terms
described in the FSL license. The Harvard-Oxford atlas is redistributed under
CC BY-SA 4.0. The project code licence does not relicense any atlas or imaging
resource.
