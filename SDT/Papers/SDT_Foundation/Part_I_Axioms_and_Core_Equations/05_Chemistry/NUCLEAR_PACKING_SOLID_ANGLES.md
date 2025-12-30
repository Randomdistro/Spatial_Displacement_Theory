# Nuclear Packing Solid Angle Calculations
## Actual Calculations from Packing Structure

**Date:** December 2025  
**Status:** Direct calculations, no word salad

---

## Packing Structure (Corrected)

### First Shell (nuc_primordial)
- 12 spheres around center (icosahedral)
- **2 octahedral spaces** remain

### First Shell Filling
- **FIRST octahedral space:** Proton + neutron = **Deuteron** (2nuc_H)
- **SECOND octahedral space:** Proton + neutron = **Helium Deuteron** (2nuc_He)
- **Alpha particle:** Deuteron + Helium Deuteron = both spaces filled

---

## Second Layer: Octahedral Defects

**First shell:** 12 icosahedral spheres + 2 octahedral spaces = 14 positions

**Second layer geometry:**
- Icosahedron: 12 vertices, 20 triangular faces
- Dodecahedron (dual): 20 vertices, 12 pentagonal faces
- They interpenetrate creating interstitial positions

**Octahedral defects in second layer:**

**From geometric structure:**
- Central sphere: radius $r$
- 12 outer spheres: each radius $r$, centers at distance $2r$ from center
- Each outer sphere center is exactly $2r$ from every other outer sphere center
- Total width: $6r$ (central + 2 layers of radius $r$ spheres)

**First shell octahedral spaces:**
- 12 dots on surface of $2r$ sphere, each $2r$ apart (triangular arrangement)
- This leaves **2 zones** on opposite sides where 2 dots are slightly more than $2r$ apart
- Each zone forms an **octahedral space** with:
  - 5 surrounding positions (from 5 nearest outer spheres)
  - 1 reference position (the "fourth wall")
  - **Total: 6 positions per octahedral space**

**First shell:** 2 octahedral spaces = 12 octahedral positions (but only 2 are used: one for deuteron, one for helium deuteron)

**Second layer calculation (CORRECTED):**
- **Second layer total width: 10r** (from center to outer edge)
- Second layer positions are in the **triangular interstices** between first-shell spheres
- These positions **do not touch each other** - they are isolated
- An icosahedron has 20 triangular faces, so **20 triangular interstices**

**Structure:**
- First shell: 12 spheres at radius $2r$, each $2r$ apart
- Triangular interstices: 20 positions in the triangular gaps
- Each interstice is surrounded by 3 first-shell spheres
- Second layer positions are at these interstices, at radius $R_2$ where total width is $10r$

**Octahedral defects in second layer:**
- The second layer has its own structure with octahedral spaces
- But the building blocks (alphas) are placed in the triangular interstices
- **20 triangular interstice positions** are available
- The number of **octahedral defects** depends on how many of these positions can form octahedral coordination

**Question:** How many octahedral defects are in the second layer structure itself (not counting the triangular interstices)?

**From the pattern:**
- First shell: 2 octahedral spaces (where 2 dots are > 2r apart)
- Second layer: Similar structure might also have 2 octahedral spaces
- But the triangular interstices (20 positions) are where building blocks are placed

**Need to calculate:** The exact number of octahedral defects in the second layer structure, accounting for the fact that second-layer positions are in triangular interstices and don't touch each other.

---

## Overloaded Neutron Counts

**Definition:** Overloaded neutrons = T = N - Z (excess neutrons beyond deuterons)

From D-T decomposition:
- D = 2Z - N (deuteron count)
- T = N - Z (overloaded neutron count = triton count)

**For each element:**

| Element | Z | N | A | D | T | Overloaded Neutrons |
|---------|---|----|---|----|----|-------------------|
| H-1 | 1 | 0 | 1 | 2 | -1 | -1 (deficit) |
| H-2 (D) | 1 | 1 | 2 | 1 | 0 | 0 |
| He-4 | 2 | 2 | 4 | 2 | 0 | 0 |
| Li-6 | 3 | 3 | 6 | 3 | 0 | 0 |
| Li-7 | 3 | 4 | 7 | 2 | 1 | 1 |
| Be-9 | 4 | 5 | 9 | 3 | 1 | 1 |
| B-10 | 5 | 5 | 10 | 5 | 0 | 0 |
| B-11 | 5 | 6 | 11 | 4 | 1 | 1 |
| C-12 | 6 | 6 | 12 | 6 | 0 | 0 |
| C-13 | 6 | 7 | 13 | 5 | 1 | 1 |
| N-14 | 7 | 7 | 14 | 7 | 0 | 0 |
| N-15 | 7 | 8 | 15 | 6 | 1 | 1 |
| O-16 | 8 | 8 | 16 | 8 | 0 | 0 |
| O-17 | 8 | 9 | 17 | 7 | 1 | 1 |
| O-18 | 8 | 10 | 18 | 6 | 2 | 2 |
| F-19 | 9 | 10 | 19 | 8 | 1 | 1 |
| Ne-20 | 10 | 10 | 20 | 10 | 0 | 0 |
| Ne-21 | 10 | 11 | 21 | 9 | 1 | 1 |
| Ne-22 | 10 | 12 | 22 | 8 | 2 | 2 |
| Na-23 | 11 | 12 | 23 | 10 | 1 | 1 |
| Mg-24 | 12 | 12 | 24 | 12 | 0 | 0 |
| Al-27 | 13 | 14 | 27 | 12 | 1 | 1 |
| Si-28 | 14 | 14 | 28 | 14 | 0 | 0 |
| P-31 | 15 | 16 | 31 | 14 | 1 | 1 |
| S-32 | 16 | 16 | 32 | 16 | 0 | 0 |
| Cl-35 | 17 | 18 | 35 | 16 | 1 | 1 |
| Ar-40 | 18 | 22 | 40 | 14 | 4 | 4 |
| K-39 | 19 | 20 | 39 | 18 | 1 | 1 |
| Ca-40 | 20 | 20 | 40 | 20 | 0 | 0 |
| Fe-56 | 26 | 30 | 56 | 22 | 4 | 4 |
| Ni-58 | 28 | 30 | 58 | 26 | 2 | 2 |
| Cu-63 | 29 | 34 | 63 | 24 | 5 | 5 |
| Zn-64 | 30 | 34 | 64 | 26 | 4 | 4 |
| Au-197 | 79 | 118 | 197 | 40 | 39 | 39 |

**Pattern:**
- Most stable isotopes have T = 0 or T = 1 (minimal overload)
- Heavier elements have more overloaded neutrons (T increases)
- Gold (Z=79) is the boundary where D = T

---

## How Next Blocks Stack In

**After first shell (alpha particle complete):**

**Second layer stacking:**
1. Next building blocks occupy icosahedral/dodecahedral interstitial positions
2. These positions are offset from first shell
3. As each shell engages, structure condenses

**Process:**
- First shell: 12 icosahedral + 2 octahedral = 14 positions → Alpha (4 nucleons)
- Second shell: Interstitial positions in icosahedral/dodecahedral geometry
- Each additional alpha or building block stacks in available interstitial positions
- The arrangement (triangular, tetrahedral, octahedral) depends on how many alphas and their geometry

**For C-12 (3 alphas):**
- 3 alphas stack in triangular arrangement
- Each alpha = complete first shell
- They occupy specific interstitial positions in second layer

**For O-16 (4 alphas):**
- 4 alphas stack in tetrahedral arrangement
- Each alpha = complete first shell
- They occupy tetrahedral interstitial positions

---

## Solid Angle Occlusion Calculation

**For each element, calculate actual occlusion from packing:**

1. Identify building block arrangement
2. Calculate solid angle from each building block
3. Account for overlaps
4. Determine total occlusion
5. Use to calculate $Z_{\text{eff,ion}}$ and exact ionization energy

## Overloaded Neutron Counts (T = N - Z)

**Formula:** T = N - Z

**Key elements for solid angle calculations:**

| Element | Z | N | T | Building Blocks |
|---------|---|---|---|-----------------|
| H-1 | 1 | 0 | -1 | Single proton |
| H-2 | 1 | 1 | 0 | Deuteron |
| He-4 | 2 | 2 | 0 | Alpha (D + He-D) |
| C-12 | 6 | 6 | 0 | 3α triangle |
| N-14 | 7 | 7 | 0 | 3α + 1p |
| O-16 | 8 | 8 | 0 | 4α tetrahedron |
| Ne-20 | 10 | 10 | 0 | 5α |
| Mg-24 | 12 | 12 | 0 | 6α octahedron |
| Si-28 | 14 | 14 | 0 | 7α |
| Ar-40 | 18 | 22 | 4 | Multiple alphas + overloaded neutrons |
| Fe-56 | 26 | 30 | 4 | 13α + overloaded neutrons |
| Cu-63 | 29 | 34 | 5 | Multiple blocks + overloaded neutrons |
| Au-197 | 79 | 118 | 39 | Many blocks + overloaded neutrons |

**Note:** Elements with T = 0 have no overloaded neutrons (all neutrons in deuterons). Elements with T > 0 have excess neutrons (in tri-alpha or triple structures).

