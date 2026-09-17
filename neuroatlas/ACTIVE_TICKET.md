# NeuroAtlas active ticket

Status: DEPLOYED - AWAITING IPHONE VALIDATION

Base release: Precision v3
Base code commit: 52f2124407f1bba9a44165286f93563650c65bec
Checkpoint commit: 318b8569c8c1ce72f15c2bef4b6d92b8ad641728
Precision v4 implementation commit: 59d862e1d6511c258d446f8f3f815f4d97e0c84a
Precision v4 Pages run: 35269053894 - completed successfully

Current ticket: Precision v4 - search, ventricles, fallback, outline precision

Implemented in this ticket:
1. Protected viewer layout and interaction remain unchanged.
2. FIND landing points are generated from real voxels inside atlas labels rather than mathematical centroids.
3. Third and fourth ventricle recognition takes priority over adjacent atlas labels at the cursor.
4. Lateral ventricle segmentation remains Harvard-Oxford based, with ventricular teaching text preserved.
5. Fallback labels are chosen by physical distance across AAL, Harvard-Oxford, and JHU rather than atlas-by-atlas priority.
6. Fallback labels display distance so nearby labels are not presented as exact voxel matches.
7. Searched structures use 45 percent teaching opacity by default.
8. Sharp color boundaries use NiiVue opaque-boundary mode while structure fill remains translucent.
9. Finer rostral/caudal midbrain, pons, and medulla teaching remains intact, with upper/lower and open/closed search aliases.
10. User-facing generated page contains no long dash characters.

Server-side validation completed:
- JHU internal-capsule representative points for labels 17, 18, 19, 20, 21, and 22 sample back to the correct labels.
- Harvard-Oxford left and right lateral-ventricle representative points sample back to labels 3 and 14 respectively.
- Generated Precision v4 JavaScript passes node --check.
- Generated page contains bestNearbyLabel, Sharp color boundaries, ventricle-priority logic, and brainstem aliases.

Next validation on iPhone Safari:
- internal capsule
- anterior limb of internal capsule
- posterior limb of internal capsule
- left lateral ventricle
- right lateral ventricle
- third ventricle
- fourth ventricle
- sagittal cortical points that previously returned no valid atlas boundary
- rostral midbrain / caudal midbrain
- rostral pons / caudal pons
- open medulla / closed medulla
- 45 percent opacity and Sharp color boundaries

If chat streaming is interrupted, read CHECKPOINT.md, ACTIVE_TICKET.md, and the latest GitHub commit before continuing.
