# NeuroAtlas active ticket

Status: IN PROGRESS

Base release: Precision v3
Base code commit: 52f2124407f1bba9a44165286f93563650c65bec
Checkpoint commit: 318b8569c8c1ce72f15c2bef4b6d92b8ad641728

Current ticket: Precision v4 - search, ventricles, fallback, outline precision

Work in this ticket:
1. Keep the protected viewer layout and interaction unchanged.
2. Make FIND land only on validated in-label atlas voxels and report failure honestly if a landing point is unavailable.
3. Give third and fourth ventricle recognition priority over adjacent atlas labels at the cursor.
4. Keep lateral ventricle segmentation from Harvard-Oxford and improve CSF teaching text.
5. Choose fallback labels by physical distance across AAL, Harvard-Oxford, and JHU rather than atlas-by-atlas priority.
6. Show fallback distance so a nearby label is never presented as an exact voxel match.
7. Use 45 percent teaching opacity by default for searched structures.
8. Use NiiVue opaque colored boundaries for sharper delineation while keeping translucent fill.
9. Preserve finer rostral/caudal midbrain, pons, and medulla teaching.
10. Do not use long dash characters in user-facing text.

After each completed code stage, update this file with the resulting commit SHA. If chat streaming is interrupted, read CHECKPOINT.md, ACTIVE_TICKET.md, and the latest GitHub commit before continuing.
