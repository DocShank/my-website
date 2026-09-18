# NeuroAtlas active ticket

Status: IN PROGRESS

Protected base: Precision v6
Precision v6 checkpoint commit: 0ebe853d61e741cc368528f985b1b525186f7677

Current ticket: Precision v7 - dense HD textbook cross-section teacher

User requirements for this ticket:
1. Do not change the main 4-view, axial, coronal, sagittal, 3D, cursor, FIND, viewer behavior, branding, or Anatomy Teacher.
2. Change only the Label This Cross Section feature.
3. Increase label coverage substantially, especially posterior anatomy and cortical structures.
4. Keep labels atlas-supported. Do not invent structures that the registered atlases do not identify.
5. Never truncate an anatomical name. Labels such as Middle cerebellar peduncle must remain complete.
6. Improve spatial balance so posterior and cortical anatomy are not crowded out by deep-structure priority.
7. Make the teaching plate cleaner, with textbook-style names outside the MRI and fine leader lines.
8. Render the teaching plate at higher output resolution so the MRI copy, labels, and leader lines remain sharp.
9. Add a Download Image button that exports the exact labeled cross-section plate as PNG.
10. Put a small NeuroAtlas logo and creator watermark inside the teaching plate so it is present in the exported image.
11. Preserve Filled regions as the main-view default.
12. Preserve 4-VIEW and 3D exclusion for the cross-section teacher.
13. Keep user-facing generated text free of long dash characters.

Implementation plan:
- Replace Precision v6 candidate selection with a denser spatially balanced selector.
- Reserve label capacity for cortical and cerebellar structures instead of allowing white-matter/deep labels to consume the full limit.
- Sample the whole visible slice at a finer grid.
- Allow complete multi-line structure names instead of clipping after two lines.
- Dynamically size the teaching canvas and label columns to reduce collisions.
- Increase export resolution while keeping the displayed plate responsive.
- Add a Download Image button and PNG export.
- Draw a small NeuroAtlas MRI watermark and Created by Dr. Shashank Neupane and Team on the plate itself.
- Validate generated JavaScript with node --check and deploy through GitHub Pages.

If chat streaming is interrupted, read CHECKPOINT.md, ACTIVE_TICKET.md, and the latest GitHub commit before continuing.
