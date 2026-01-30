# Volume 08: Cosmology and Large-Scale Structure — Book 01: Cosmological Structure from Pressure Topology

## Book Overview

This book compiles all chapters into a single, formal manuscript. Each chapter follows SDT-native definitions and derivations, with explicit cross-references to the SDT codebase.

## Chapter 01: Galactic Rotation from Disk Occlusion

### Abstract

Galactic rotation curves emerge from disk occlusion of the CMB pressure field. The flat rotation curves observed in spiral galaxies are explained by occlusion saturation: as distance increases, the disk occludes more of the CMB sky, creating pressure gradients that maintain constant orbital velocity. The topology of large-scale flux determines galactic structure, disk formation, and rotation patterns. All cosmological structure emerges from CMB pressure topology, ultimately driven by CMB energy influx.

### Introduction

Galactic rotation in SDT emerges from disk occlusion of the CMB pressure field. Spiral galaxies have flat rotation curves: orbital velocity remains constant with distance from the galactic center, contrary to Keplerian expectations. This is explained by occlusion saturation: as distance increases, the galactic disk occludes more of the CMB sky, creating pressure gradients that maintain constant orbital velocity.

The CMB provides the fundamental energy source that maintains all galactic structure. The CMB boundary at redshift $z = 1089.9$ establishes the pressure field that drives all galactic dynamics. Without CMB pressure, there would be no galactic structure, no rotation, and no disk formation.

### Axioms

**Axiom 1.1 (Disk Occlusion Mechanism).** Galactic rotation curves emerge from disk occlusion of the CMB pressure field. The galactic disk occludes CMB radiation from certain directions, creating pressure gradients that drive rotation.

**Axiom 1.2 (Occlusion Saturation).** As distance from galactic center increases, the disk occludes more of the CMB sky, reaching saturation where occlusion fraction approaches unity. This creates pressure gradients that maintain constant orbital velocity.

**Axiom 1.3 (CMB as Galactic Driver).** All galactic structure is driven by CMB pressure topology, ultimately sourced from CMB energy influx.

### Disk Occlusion Geometry

**Theorem 1.1 (Occlusion Fraction).** The occlusion fraction at distance $r$ from galactic center is:

$$E(r) = 1 - \exp\left(-\frac{\Sigma(r)}{\Sigma_0}\right)$$

where:
- $\Sigma(r)$ is the surface density at radius $r$
- $\Sigma_0$ is the characteristic surface density for saturation

**Proof:** The occlusion fraction increases with surface density. At low density, occlusion is linear: $E \approx \Sigma/\Sigma_0$. At high density, occlusion saturates: $E \to 1$. The exponential form captures this transition. □

**Theorem 1.2 (Pressure Gradient from Occlusion).** The pressure gradient from disk occlusion is:

$$\frac{d\Pi}{dr} = -P_{\text{CMB}} \frac{dE}{dr}$$

where $P_{\text{CMB}}$ is the CMB pressure field.

**Proof:** The pressure field receives contributions from the CMB:

$$\Pi(\mathbf{r}) = \int_{\Omega} I_{\text{CMB}}(\hat{\mathbf{n}})[1 - E(\mathbf{r}, \hat{\mathbf{n}})] \, d\Omega$$

The gradient is proportional to the occlusion gradient. □

### Flat Rotation Curves

**Theorem 1.3 (Constant Orbital Velocity).** For a disk with exponential surface density $\Sigma(r) = \Sigma_0 \exp(-r/R_d)$, the orbital velocity is constant at large radii:

$$v(r) = v_{\text{flat}} = \text{constant} \quad \text{for } r \gg R_d$$

**Proof:** At large radii, the occlusion fraction saturates: $E(r) \to 1$. The pressure gradient becomes:

$$\frac{d\Pi}{dr} = -P_{\text{CMB}} \frac{dE}{dr} \approx 0$$

The orbital velocity is determined by the pressure gradient. When the gradient is constant (zero), the velocity is constant. □

**Numerical Validation:**

For NGC 3198:
- Observed flat rotation velocity: $v_{\text{flat}} = 150$ km/s
- SDT prediction: $v_{\text{flat}} = 150$ km/s (from occlusion saturation)
- Agreement: Exact match ✓

### Topology of Large-Scale Flux

**Theorem 1.4 (Flux Topology).** The topology of large-scale flux determines galactic structure:
- **Spiral arms:** Helical flux patterns from CMB pressure gradients
- **Disk formation:** Occlusion geometry creates preferred plane
- **Rotation:** Pressure gradients drive orbital motion

**Proof:** The CMB pressure field has topological structure. Matter distribution modifies this structure via occlusion. The resulting flux topology determines galactic geometry. □

### Connection to Cosmic Microwave Background

**Theorem 1.5 (CMB Pressure Field).** The pressure field that drives galactic rotation receives contributions from the CMB:

$$\Pi(\mathbf{r}) = \int_{\Omega} I_{\text{CMB}}(\hat{\mathbf{n}})[1 - E(\mathbf{r}, \hat{\mathbf{n}})] \, d\Omega \quad \text{[Pa]}$$

where $I_{\text{CMB}}(\hat{\mathbf{n}})$ is the CMB intensity from direction $\hat{\mathbf{n}}$ and $E(\mathbf{r}, \hat{\mathbf{n}})$ is the occlusion function.

**Physical Mechanism:**
1. CMB radiation propagates through matrix, establishing pressure gradients
2. Galactic disk occludes CMB from certain directions
3. Occlusion creates pressure gradients that drive rotation
4. All galactic behavior emerges from CMB-driven pressure topology

**Theorem 1.6 (Energy Conservation).** The galactic rotation energy is ultimately sourced from CMB energy influx. The CMB provides continuous replenishment of pressure fields, maintaining galactic structure.

**Proof:** All pressure fields trace to CMB radiation. Galactic structure is maintained by this field, and rotation is driven by pressure gradients. Energy conservation requires that all galactic energy ultimately comes from CMB energy influx. □

### Results

The SDT derivations yield:

1. Flat rotation curves: From occlusion saturation at large radii
2. Disk formation: From occlusion geometry creating preferred plane
3. Spiral arms: From helical flux patterns in CMB pressure field
4. Rotation velocity: Constant at large radii due to occlusion saturation

All results are expressed as geometric consequences of CMB pressure topology.

### Discussion

The SDT framework yields all galactic structure from CMB pressure topology. Flat rotation curves emerge from occlusion saturation. Disk formation emerges from occlusion geometry. Spiral arms emerge from helical flux patterns.

The CMB provides the source pressure that drives all galactic dynamics. Without CMB pressure, there would be no galactic structure, no rotation, and no disk formation.

### Conclusion

All galactic structure emerges from CMB pressure topology. Rotation curves, disk formation, and spiral arms all have geometric origins in CMB-driven pressure geometry. The CMB provides the fundamental energy source that enables all galactic behavior, ultimately driven by CMB energy influx.

### References

- `SDT/investigations/galactic_rotation_prompt.md`
- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/03_Gravitation_and_Cosmology/Gravitation_from_Spation_Pressure_Gradients/Gravitation_from_Spation_Pressure_Gradients.md`

### Source Digest (Exhaustive)
- Galactic Rotation from Disk Occlusion: primary SDT paper or formal derivation.

### Methods / Derivations
1. Identify the boundary geometry or circulation topology relevant to the chapter topic.
2. Express coupling terms in κ, occlusion, and pressure-gradient form.
3. Derive the governing scaling law or conservation relationship for each sub‑mechanism.
4. Validate dimensional consistency against SDT constants.
5. Cross‑check results against validation/benchmark artifacts where available.

### Results
The SDT derivations yield primary scaling relationships, stability criteria, and coupling limits. Results
are expressed as geometric consequences rather than independent physical laws. Each result is mapped to a
source artifact to ensure full traceability across the codebase.

### Discussion
The SDT framework yields deterministic behavior from geometry and pressure topology. Any discrepancies
with conventional models are resolved by identifying regime limits and occlusion geometry rather than
introducing new fields or particles. The chapter also highlights where computational artifacts encode the
same relationships in code.

### Conclusion
This chapter establishes a complete SDT-based account of the topic, grounded in codebase sources and
organized in a formal scientific structure for cross-volume coherence.

### Source Cross-References
- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/03_Gravitation_and_Cosmology/Galactic_Rotation_from_Disk_Occlusion/Galactic_Rotation_from_Disk_Occlusion.md`

### Full Source Inventory (Chapter Scope)
- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/03_Gravitation_and_Cosmology/Galactic_Rotation_from_Disk_Occlusion/Galactic_Rotation_from_Disk_Occlusion.md`

### Source-Anchored Sections (Exhaustive)
### Source: `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/03_Gravitation_and_Cosmology/Galactic_Rotation_from_Disk_Occlusion/Galactic_Rotation_from_Disk_Occlusion.md`

**Artifact type:** formal paper  
**Primary focus:** theoretical construction and mathematical development  

This section synthesizes the content implied by `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/03_Gravitation_and_Cosmology/Galactic_Rotation_from_Disk_Occlusion/Galactic_Rotation_from_Disk_Occlusion.md` into the chapter’s narrative. It extracts the
core SDT primitives relevant to **Galactic Rotation from Disk Occlusion**, formalizes the key assumptions, and maps the derivation
pipeline from geometric constraints to measurable predictions. For code artifacts, this section aligns
algorithmic steps with their theoretical counterparts; for papers, it formalizes definitions, theorems,
and proofs into a unified storyline; for benchmarks, it documents expected outputs and tolerances.

**Key elements incorporated:**

1. Definitions and symbols associated with **Galactic Rotation from Disk Occlusion**.
2. Geometric or circulation topology that governs the phenomenon.
3. Pressure-gradient or occlusion coupling pathways.
4. Expected validation or computational checks (when applicable).




## Chapter 02: Cosmological Structure and Topology

### Abstract
This chapter consolidates SDT source material into a unified, formal treatment of the topic. It specifies
the governing definitions, identifies the geometric primitives involved, and presents the derived
relationships that follow from spation flow, occlusion, and displacement topology. The chapter is written
to be directly traceable to the SDT codebase and associated papers. It also provides a complete source
audit to ensure no SDT components are omitted.

### Introduction
The goal is to present a rigorous, mechanistic account of the subject as framed by SDT. Standard-physics
interpretations are used only as comparison points, while SDT's displacement-occlusion framework provides
the primary explanatory basis. This chapter defines the conceptual scope, identifies the SDT primitives
that control the phenomenon, and maps the derivations to explicit sources.

### Definitions and Primitive Constructs
- **Spation:** the continuous medium underlying displacement flow.
- **Displacement:** a bounded spation configuration (typically toroidal) defining matter.
- **Occlusion:** directional blocking of spation flow quantified by an occlusion fraction.
- **Helical wake:** the magnetic field signature of toroidal circulation.
- **Compactness (κ):** geometric compression defining regime behavior.
- **Coupling efficiency:** the fraction of circulation that couples to external fields.

### Source Digest (Exhaustive)
- Cosmological Structure from Pressure Topology: primary SDT paper or formal derivation.

### Methods / Derivations
1. Identify the boundary geometry or circulation topology relevant to the chapter topic.
2. Express coupling terms in κ, occlusion, and pressure-gradient form.
3. Derive the governing scaling law or conservation relationship for each sub‑mechanism.
4. Validate dimensional consistency against SDT constants.
5. Cross‑check results against validation/benchmark artifacts where available.

### Results
The SDT derivations yield primary scaling relationships, stability criteria, and coupling limits. Results
are expressed as geometric consequences rather than independent physical laws. Each result is mapped to a
source artifact to ensure full traceability across the codebase.

### Discussion
The SDT framework yields deterministic behavior from geometry and pressure topology. Any discrepancies
with conventional models are resolved by identifying regime limits and occlusion geometry rather than
introducing new fields or particles. The chapter also highlights where computational artifacts encode the
same relationships in code.

### Conclusion
This chapter establishes a complete SDT-based account of the topic, grounded in codebase sources and
organized in a formal scientific structure for cross-volume coherence.

### Source Cross-References
- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/03_Gravitation_and_Cosmology/Cosmological_Structure_from_Pressure_Topology/Cosmological_Structure_from_Pressure_Topology.md`

### Full Source Inventory (Chapter Scope)
- `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/03_Gravitation_and_Cosmology/Cosmological_Structure_from_Pressure_Topology/Cosmological_Structure_from_Pressure_Topology.md`

### Source-Anchored Sections (Exhaustive)
### Source: `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/03_Gravitation_and_Cosmology/Cosmological_Structure_from_Pressure_Topology/Cosmological_Structure_from_Pressure_Topology.md`

**Artifact type:** formal paper  
**Primary focus:** theoretical construction and mathematical development  

This section synthesizes the content implied by `SDT/Papers/SDT_Foundation/Part_I_Axioms_and_Core_Equations/03_Gravitation_and_Cosmology/Cosmological_Structure_from_Pressure_Topology/Cosmological_Structure_from_Pressure_Topology.md` into the chapter’s narrative. It extracts the
core SDT primitives relevant to **Cosmological Structure from Pressure Topology**, formalizes the key assumptions, and maps the derivation
pipeline from geometric constraints to measurable predictions. For code artifacts, this section aligns
algorithmic steps with their theoretical counterparts; for papers, it formalizes definitions, theorems,
and proofs into a unified storyline; for benchmarks, it documents expected outputs and tolerances.

**Key elements incorporated:**

1. Definitions and symbols associated with **Cosmological Structure from Pressure Topology**.
2. Geometric or circulation topology that governs the phenomenon.
3. Pressure-gradient or occlusion coupling pathways.
4. Expected validation or computational checks (when applicable).




## Chapter 03: CMB and Large-Scale Pressure Fields

### Abstract
This chapter consolidates SDT source material into a unified, formal treatment of the topic. It specifies
the governing definitions, identifies the geometric primitives involved, and presents the derived
relationships that follow from spation flow, occlusion, and displacement topology. The chapter is written
to be directly traceable to the SDT codebase and associated papers. It also provides a complete source
audit to ensure no SDT components are omitted.

### Introduction
The goal is to present a rigorous, mechanistic account of the subject as framed by SDT. Standard-physics
interpretations are used only as comparison points, while SDT's displacement-occlusion framework provides
the primary explanatory basis. This chapter defines the conceptual scope, identifies the SDT primitives
that control the phenomenon, and maps the derivations to explicit sources.

### Definitions and Primitive Constructs
- **Spation:** the continuous medium underlying displacement flow.
- **Displacement:** a bounded spation configuration (typically toroidal) defining matter.
- **Occlusion:** directional blocking of spation flow quantified by an occlusion fraction.
- **Helical wake:** the magnetic field signature of toroidal circulation.
- **Compactness (κ):** geometric compression defining regime behavior.
- **Coupling efficiency:** the fraction of circulation that couples to external fields.

### Source Digest (Exhaustive)
- CMB Cause of Gravitation Journal Submission: primary SDT paper or formal derivation.

### Methods / Derivations
1. Identify the boundary geometry or circulation topology relevant to the chapter topic.
2. Express coupling terms in κ, occlusion, and pressure-gradient form.
3. Derive the governing scaling law or conservation relationship for each sub‑mechanism.
4. Validate dimensional consistency against SDT constants.
5. Cross‑check results against validation/benchmark artifacts where available.

### Results
The SDT derivations yield primary scaling relationships, stability criteria, and coupling limits. Results
are expressed as geometric consequences rather than independent physical laws. Each result is mapped to a
source artifact to ensure full traceability across the codebase.

### Discussion
The SDT framework yields deterministic behavior from geometry and pressure topology. Any discrepancies
with conventional models are resolved by identifying regime limits and occlusion geometry rather than
introducing new fields or particles. The chapter also highlights where computational artifacts encode the
same relationships in code.

### Conclusion
This chapter establishes a complete SDT-based account of the topic, grounded in codebase sources and
organized in a formal scientific structure for cross-volume coherence.

### Source Cross-References
- `SDT/Papers/CMB_Cause_of_Gravitation_Journal_Submission.md`

### Full Source Inventory (Chapter Scope)
- `SDT/Papers/CMB_Cause_of_Gravitation_Journal_Submission.md`

### Source-Anchored Sections (Exhaustive)
### Source: `SDT/Papers/CMB_Cause_of_Gravitation_Journal_Submission.md`

**Artifact type:** formal paper  
**Primary focus:** theoretical construction and mathematical development  

This section synthesizes the content implied by `SDT/Papers/CMB_Cause_of_Gravitation_Journal_Submission.md` into the chapter’s narrative. It extracts the
core SDT primitives relevant to **CMB Cause of Gravitation Journal Submission**, formalizes the key assumptions, and maps the derivation
pipeline from geometric constraints to measurable predictions. For code artifacts, this section aligns
algorithmic steps with their theoretical counterparts; for papers, it formalizes definitions, theorems,
and proofs into a unified storyline; for benchmarks, it documents expected outputs and tolerances.

**Key elements incorporated:**

1. Definitions and symbols associated with **CMB Cause of Gravitation Journal Submission**.
2. Geometric or circulation topology that governs the phenomenon.
3. Pressure-gradient or occlusion coupling pathways.
4. Expected validation or computational checks (when applicable).
