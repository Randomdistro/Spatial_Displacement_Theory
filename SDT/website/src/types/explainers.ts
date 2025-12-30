/**
 * Visual Explainer System - Type Definitions
 * Comprehensive type system for explainers, cross-references, and visualizations
 */

export type ExplainerCategory = 'paper' | 'phase' | 'benchmark' | 'formula' | 'rule' | 'element';
export type Domain = 
  | 'foundational' 
  | 'atomic' 
  | 'electromagnetic' 
  | 'gravitational' 
  | 'cosmological'
  | 'thermodynamic'
  | 'chemistry'
  | 'nuclear'
  | 'condensed-matter'
  | 'fluid-dynamics'
  | 'universal';

export type VisualizationType = '3d' | '2d' | 'animation' | 'formula' | 'chart';
export type VisualizationPosition = 'inline' | 'sidebar' | 'fullscreen';
export type ParameterType = 'slider' | 'input' | 'dropdown' | 'checkbox';
export type ReferenceType = 
  | 'DERIVES'           // Paper derives formula
  | 'VALIDATES'         // Benchmark validates paper
  | 'USES'              // Paper uses concept
  | 'EXTENDS'           // Paper extends previous work
  | 'SPECIAL_CASE'      // Formula is special case
  | 'DEPENDS_ON'        // Concept depends on another
  | 'RELATED_TO'        // General relationship
  | 'PART_OF'           // Concept is part of larger concept
  | 'VALIDATED_BY';     // Concept validated by benchmark

export type ExplainerStatus = 'draft' | 'review' | 'published' | 'deprecated';

/**
 * Cross-reference between concepts
 */
export interface CrossReference {
  sourceId: string;           // ID of source concept
  targetId: string;           // ID of target concept
  referenceType: ReferenceType; // Type of relationship
  context?: string;            // Optional context description
  section?: string;            // Specific section/page
  strength?: number;           // 0-1, strength of relationship
}

/**
 * Parameter configuration for interactive visualizations
 */
export interface ParameterConfig {
  name: string;
  type: ParameterType;
  min?: number;
  max?: number;
  step?: number;
  defaultValue: any;
  label: string;
  description: string;
  unit?: string;              // Unit for display
  options?: Array<{ value: any; label: string }>; // For dropdown
}

/**
 * Visualization configuration
 */
export interface VisualizationConfig {
  id: string;
  type: VisualizationType;
  component: string;              // React component name
  props: Record<string, any>;    // Component props
  position: VisualizationPosition;
  interactive: boolean;
  parameters?: ParameterConfig[]; // For interactive visualizations
  caption?: string;               // Caption text
  alt?: string;                   // Accessibility alt text
}

/**
 * Formula reference with metadata
 */
export interface FormulaReference {
  id: string;                    // Unique formula ID
  latex: string;                 // LaTeX representation
  displayMode: 'inline' | 'block';
  label?: string;                // Equation label (e.g., "Eq. 1")
  description: string;           // What the formula represents
  dimensionalAnalysis: string;   // Dimensional analysis result
  numericalExample?: {
    values: Record<string, number>;
    result: number;
    units: string;
  };
  derivation?: {
    steps: DerivationStep[];
    sourcePaper: string;
    sourcePhase?: string;
  };
  variables?: VariableDefinition[]; // Variable definitions
}

/**
 * Single step in formula derivation
 */
export interface DerivationStep {
  step: number;
  latex: string;                 // Formula at this step
  description: string;           // What transformation was applied
  justification?: string;         // Why this step is valid
}

/**
 * Variable definition for formulas
 */
export interface VariableDefinition {
  symbol: string;
  name: string;
  description: string;
  units: string;
  value?: number;                // Typical or example value
}

/**
 * Content structure for explainers
 */
export interface ExplainerContent {
  markdown: string;              // Main content (markdown)
  formulas: FormulaReference[];  // Formulas in content
  visualizations: VisualizationConfig[]; // Visual components
  sections?: ContentSection[];    // Structured sections
}

/**
 * Content section for structured display
 */
export interface ContentSection {
  id: string;
  title: string;
  content: string;               // Markdown content
  order: number;
  visualizations?: string[];     // IDs of visualizations in this section
  formulas?: string[];            // IDs of formulas in this section
}

/**
 * Cross-reference collections
 */
export interface ExplainerReferences {
  papers: string[];              // Related paper IDs
  phases: string[];              // Related phase IDs
  benchmarks: string[];          // Related benchmark IDs
  formulas: string[];            // Related formula IDs
  rules: string[];               // Related rule IDs
  elements?: string[];            // Related element IDs (for chemistry)
}

/**
 * Validation metadata
 */
export interface ValidationMetadata {
  validatedBy?: string[];         // Benchmark IDs that validate
  errorRate?: number;             // Validation error percentage
  tolerance?: number;             // Acceptable error tolerance
  experimentalValue?: number;     // Experimental measurement
  predictedValue?: number;        // SDT prediction
  units?: string;                 // Units for values
  source?: string;                // Source of experimental data
}

/**
 * Complete explainer metadata
 */
export interface ExplainerMetadata {
  id: string;                     // Unique identifier (e.g., "paper-core-engine")
  title: string;                  // Display title
  description: string;            // Short description (1-2 sentences)
  category: ExplainerCategory;
  domain: Domain;
  
  // Content
  content: ExplainerContent;
  
  // Cross-references
  references: ExplainerReferences;
  
  // Metadata
  authors?: string[];
  dateCreated: string;           // ISO 8601 date
  dateUpdated: string;           // ISO 8601 date
  version: string;                // Semantic version
  status: ExplainerStatus;
  
  // Validation (for benchmarks and validated concepts)
  validation?: ValidationMetadata;
  
  // Additional metadata
  tags?: string[];                // Searchable tags
  difficulty?: 'beginner' | 'intermediate' | 'advanced';
  estimatedReadTime?: number;      // Minutes
  prerequisites?: string[];       // IDs of prerequisite explainers
}

/**
 * Explainer registry entry
 */
export interface ExplainerRegistryEntry {
  id: string;
  metadata: ExplainerMetadata;
  componentPath?: string;         // Path to React component (if custom)
  dataPath: string;               // Path to JSON metadata file
}

/**
 * Cross-reference graph node
 */
export interface ReferenceGraphNode {
  id: string;
  label: string;
  category: ExplainerCategory;
  domain: Domain;
  x?: number;                     // Position (for force-directed layout)
  y?: number;
  vx?: number;                    // Velocity (for force-directed layout)
  vy?: number;
}

/**
 * Cross-reference graph edge
 */
export interface ReferenceGraphEdge {
  source: string;                 // Node ID
  target: string;                 // Node ID
  type: ReferenceType;
  strength?: number;
  label?: string;
}

/**
 * Complete cross-reference graph
 */
export interface ReferenceGraph {
  nodes: ReferenceGraphNode[];
  edges: ReferenceGraphEdge[];
}

/**
 * Explainer search result
 */
export interface ExplainerSearchResult {
  id: string;
  title: string;
  description: string;
  category: ExplainerCategory;
  domain: Domain;
  relevanceScore: number;
  matchedFields: string[];        // Which fields matched search
}

/**
 * Explainer filter options
 */
export interface ExplainerFilter {
  categories?: ExplainerCategory[];
  domains?: Domain[];
  status?: ExplainerStatus[];
  tags?: string[];
  searchQuery?: string;
}

