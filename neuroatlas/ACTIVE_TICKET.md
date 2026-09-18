# NeuroAtlas active ticket

Status: DEPLOYED - AWAITING IPHONE VALIDATION

Protected base: Precision v6
Precision v6 checkpoint commit: 0ebe853d61e741cc368528f985b1b525186f7677
Precision v7 ticket commit: 64e2e1dfdd685717ba5909672a1271c3e705492f
Precision v7 patch commit: ff8a27e235eea0bc05ecb4c3fa8c0bd4e03946cd
Precision v7 deployment commit: 5d067faea9c5c1fe146c72265622e66b3f9885f8
Precision v7 hardened deployment commit: 76e31b7ab42b7c52f4e7e562d02e492a96898cbe
Precision v7 Pages run: 35314770598 - completed successfully

Current ticket: Precision v7 - dense HD textbook cross-section teacher

Implemented in Precision v7:
1. Main 4-view, axial, coronal, sagittal, 3D, cursor, FIND, branding, Filled regions default, and Anatomy Teacher remain unchanged.
2. Only the Label This Cross Section feature was upgraded.
3. Cross-section sampling is substantially denser across the full visible slice.
4. Label selection is spatially balanced so posterior anatomy and cortical/cerebellar structures are less likely to be crowded out by deep structures.
5. Mobile label capacity increased to 36 atlas-supported structures and larger screens to 52.
6. A dedicated cortical/cerebellar label quota is reserved before remaining label slots are filled.
7. Anatomical names are no longer clipped after two lines. Full names such as Middle cerebellar peduncle are preserved.
8. Several AAL shorthand labels are expanded into cleaner textbook-style anatomical names.
9. The teaching plate is rendered at substantially higher internal resolution while remaining responsive on screen.
10. Labels remain outside the central MRI when practical and connect to sampled anatomy with fine leader lines and small target dots.
11. The teaching canvas height expands dynamically to reduce label collisions when many structures are present.
12. A Download Image button exports the current labeled teaching plate as a PNG.
13. The exported plate includes a small NeuroAtlas MRI logo watermark and Dr. Shashank Neupane and Team creator credit.
14. 4-VIEW and 3D remain excluded from cross-section labeling. AXIAL, CORONAL, and SAGITTAL remain supported.
15. User-facing generated text remains free of long dash characters.

Build and deployment validation:
- Precision v7 applies after the protected v2, v3, v4, v5, and v6 reconstruction chain.
- Generated page matches pinned SHA-256 7b38676ca501603ccba409e332aa3e61c82d91d316229f8e760669b34eaa54c3.
- Generated module passes node --check.
- Build guards confirm HD TEXTBOOK CROSS SECTION, Download Image, spatial balancing, watermark rendering, and dense label capacity.
- Build guards confirm the old v5 bubble renderer and detached cross-list remain absent.
- Build guards confirm the old two-line truncation code is absent.
- GitHub Pages run 35314770598 completed successfully.
- Deployment workflow now uses download timeouts and cancels stale in-progress Pages runs to reduce future deployment stalls.

Next iPhone validation:
- Open a fresh Precision v7 URL.
- Test one useful AXIAL, CORONAL, and SAGITTAL cross section.
- Check posterior and cortical coverage.
- Check that Middle cerebellar peduncle and other long names display completely.
- Check label-line cleanliness and endpoint accuracy.
- Check HD plate sharpness.
- Press Download Image and confirm the PNG contains the same plate plus the small NeuroAtlas watermark.
- Confirm the main viewer behavior remains unchanged.

If chat streaming is interrupted, resume by reading CHECKPOINT.md, ACTIVE_TICKET.md, and the latest GitHub commit before doing anything else.
