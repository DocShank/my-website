# NeuroAtlas active ticket

Status: DEPLOYED - AWAITING IPHONE VALIDATION

Protected base: Precision v5
Precision v4 implementation commit: 59d862e1d6511c258d446f8f3f815f4d97e0c84a
Precision v5 patch commit: 5ef9cef559672605fb9b6fb31b66125c892e453a
Precision v5 checkpoint commit: 6d536017aab70e43d1849e11674b33ed2ecef130
Precision v6 patch commit: fb5c63747cb7c2af50545b301ed3c714648faffa
Precision v6 deployment commit: 6db81dd4a9e0e2db0e9444dbb2c6357846115d02
Precision v6 Pages run: 35309183050 - deploy job completed successfully

Current ticket: Precision v6 - textbook cross-section teacher

User-validated problem addressed:
- The v5 black teaching panel, floating numbered circles, and detached legend were rejected.
- The main MRI viewer, FIND, navigation, 3D behavior, branding, anatomy teacher, and Filled regions default were preserved.

Implemented in Precision v6:
1. Replaced the v5 marker-bubble/legend renderer.
2. The teaching plate captures the live NiiVue canvas only after an explicit nv.drawScene() call and converts the exact current MRI slice to an image before composing the teaching plate.
3. The exact axial, coronal, or sagittal slice is placed in the center of a wider teaching canvas.
4. Structure labels are drawn in left and right textbook-style columns outside the MRI.
5. Thin colored leader lines connect each label to a representative sampled point inside the atlas-supported structure.
6. Representative target points are chosen from real sampled pixels inside each structure, not geometric centers that may fall outside irregular anatomy.
7. Labels are sorted by target position and vertically redistributed to reduce collisions.
8. Label priority favors CSF/ventricles, major white matter, deep gray/brainstem, cerebellum, then cortical regions.
9. Up to 18 atlas-supported labels are shown on iPhone and up to 24 on larger screens.
10. Long left/right names are shortened to compact textbook-style names with (L) or (R).
11. The detached numbered legend and floating circle UI were removed from the generated build.
12. Color is limited mainly to thin leader lines and tiny target dots, preserving the MRI itself.
13. 4-VIEW and 3D remain excluded. AXIAL, CORONAL, and SAGITTAL remain supported.
14. User-facing generated page remains free of long dash characters.

Build validation completed:
- Precision v6 patch applies after the protected v2, v3, v4, and v5 reconstruction chain.
- Generated HTML matches pinned SHA-256 638652bb9965853873fa85da1f721df8827272e580c4484fd4cfc68b4886e382.
- Generated module passes node --check.
- Build guards confirm TEXTBOOK CROSS SECTION and renderTextbookPlate are present.
- Build guards confirm renderCrossPins and cross-list are absent.
- GitHub Pages deploy job for run 35309183050 completed successfully.

Next iPhone validation:
- Open a fresh Precision v6 URL.
- In CORONAL, AXIAL, and SAGITTAL, press LABEL THIS CROSS SECTION.
- Confirm the same MRI slice is reproduced rather than a black panel.
- Confirm labels appear around the MRI with thin leader lines.
- Confirm labels are readable and do not pile up badly.
- Confirm leader-line endpoints land inside the intended anatomy.
- Confirm 4-VIEW and 3D keep the button disabled.

If chat streaming is interrupted again, resume by reading CHECKPOINT.md, ACTIVE_TICKET.md, and the latest GitHub commit before doing anything else.
