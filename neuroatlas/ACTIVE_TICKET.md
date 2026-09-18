# NeuroAtlas active ticket

Status: IN PROGRESS

Protected base: Precision v5
Precision v4 implementation commit: 59d862e1d6511c258d446f8f3f815f4d97e0c84a
Precision v5 patch commit: 5ef9cef559672605fb9b6fb31b66125c892e453a
Precision v5 checkpoint commit: 6d536017aab70e43d1849e11674b33ed2ecef130

Current ticket: Precision v6 - textbook cross-section teacher

User-validated problem:
- Branding and filled-region default are acceptable.
- FIND and the main MRI viewer should remain unchanged.
- The Precision v5 cross-section teacher is rejected.
- Its black panel, floating numbered circles, and detached legend do not resemble a useful anatomy teaching plate.
- Axial, coronal, and sagittal cross-section outputs must be rebuilt.

Acceptance criteria for Precision v6:
1. Preserve the exact main MRI viewer, navigation, FIND behavior, 3D behavior, branding, anatomy teacher, and Filled regions default.
2. Replace the v5 bubble-marker/legend renderer rather than tuning it.
3. Use the exact currently displayed axial, coronal, or sagittal MRI slice as the teaching image.
4. Render structure names around the image in a conventional anatomy-textbook style.
5. Draw thin leader lines from each label to a point inside the identified structure.
6. Keep label text outside the central anatomy whenever practical.
7. Use deterministic collision avoidance so labels do not stack on top of each other.
8. Prefer the most educational visible structures: ventricles/CSF, internal capsule and major white matter, basal ganglia, thalamus, hippocampal/mesial temporal structures, brainstem/cerebellum, then major cortical regions.
9. Label only structures supported by the registered AAL, Harvard-Oxford, or JHU atlases. Do not invent anatomy.
10. Keep color subtle. Color may distinguish label classes and leader lines, but it must not obscure the MRI.
11. Disable the cross-section teacher in 4-VIEW and 3D. Enable it only in AXIAL, CORONAL, and SAGITTAL.
12. The generated teaching plate must be readable on iPhone without requiring a long detached legend.
13. No long dash characters in user-facing generated text.
14. Build must pass node --check and GitHub Pages deployment.

Implementation plan:
- Add a Precision v6 runtime patch after v5.
- Remove/hide the v5 marker bubble and legend behavior.
- Generate the teaching plate on a dedicated canvas wider than the MRI so there is room for labels on both sides.
- Copy the exact live MRI slice into the center of that canvas.
- Sample visible atlas structures from the live slice.
- Choose representative target points from actual sampled pixels inside each atlas structure.
- Split labels into left and right columns based on target position.
- Sort and vertically distribute each side to avoid collisions.
- Draw fine leader lines from the label columns to the structure targets.
- Keep a small optional class key only if useful, not as the primary labeling method.

If chat streaming is interrupted again, resume by reading CHECKPOINT.md, ACTIVE_TICKET.md, and the latest GitHub commit before doing anything else.
