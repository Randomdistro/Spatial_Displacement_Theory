/**
 * Explainer Data Loader
 * Loads explainer metadata and cross-references from JSON files
 */

import type {
  ExplainerMetadata,
  CrossReference,
  ReferenceGraph,
  ReferenceGraphNode,
  ReferenceGraphEdge,
  ExplainerSearchResult,
  ExplainerFilter,
} from '../types/explainers';

// Cache for loaded explainers
const explainerCache = new Map<string, ExplainerMetadata>();
const crossReferenceCache = new Map<string, CrossReference[]>();

/**
 * Load explainer metadata from JSON file
 */
export async function loadExplainerMetadata(explainerId: string): Promise<ExplainerMetadata | null> {
  // Check cache first
  if (explainerCache.has(explainerId)) {
    return explainerCache.get(explainerId)!;
  }

  try {
    // Load from public/data/explainers/{category}/{id}.json
    // We'll determine category from ID pattern or try multiple paths
    const possiblePaths = [
      `/data/explainers/papers/${explainerId}.json`,
      `/data/explainers/phases/${explainerId}.json`,
      `/data/explainers/benchmarks/${explainerId}.json`,
      `/data/explainers/formulas/${explainerId}.json`,
      `/data/explainers/rules/${explainerId}.json`,
      `/data/explainers/elements/${explainerId}.json`,
    ];

    for (const path of possiblePaths) {
      try {
        const response = await fetch(path);
        if (response.ok) {
          const data = await response.json();
          const metadata = data as ExplainerMetadata;
          
          // Validate basic structure
          if (!metadata.id || !metadata.title || !metadata.content) {
            console.warn(`Invalid explainer metadata structure for ${explainerId}`);
            continue;
          }

          explainerCache.set(explainerId, metadata);
          return metadata;
        }
      } catch (error) {
        // Try next path
        continue;
      }
    }

    console.warn(`Explainer not found: ${explainerId}`);
    return null;
  } catch (error) {
    console.error(`Error loading explainer ${explainerId}:`, error);
    return null;
  }
}

/**
 * Load multiple explainers by ID
 */
export async function loadExplainerMetadataBatch(
  explainerIds: string[]
): Promise<Map<string, ExplainerMetadata>> {
  const results = new Map<string, ExplainerMetadata>();
  
  await Promise.all(
    explainerIds.map(async (id) => {
      const metadata = await loadExplainerMetadata(id);
      if (metadata) {
        results.set(id, metadata);
      }
    })
  );

  return results;
}

/**
 * Load cross-references from JSON file
 */
export async function loadCrossReferences(): Promise<CrossReference[]> {
  // Check cache
  if (crossReferenceCache.has('all')) {
    return crossReferenceCache.get('all')!;
  }

  try {
    const response = await fetch('/data/explainers/crossReferences.json');
    if (!response.ok) {
      console.warn('Cross-references file not found, returning empty array');
      return [];
    }

    const data = await response.json();
    const references = data.references as CrossReference[];
    
    crossReferenceCache.set('all', references);
    return references;
  } catch (error) {
    console.error('Error loading cross-references:', error);
    return [];
  }
}

/**
 * Get cross-references for a specific explainer
 */
export async function getExplainerReferences(explainerId: string): Promise<CrossReference[]> {
  const allReferences = await loadCrossReferences();
  return allReferences.filter(ref => ref.sourceId === explainerId);
}

/**
 * Get explainers that reference a specific explainer
 */
export async function getReferencingExplainers(explainerId: string): Promise<CrossReference[]> {
  const allReferences = await loadCrossReferences();
  return allReferences.filter(ref => ref.targetId === explainerId);
}

/**
 * Build reference graph from loaded data
 */
export async function buildReferenceGraph(
  explainerIds?: string[]
): Promise<ReferenceGraph> {
  const references = await loadCrossReferences();
  
  // Get all unique concept IDs
  const allIds = new Set<string>();
  references.forEach(ref => {
    allIds.add(ref.sourceId);
    allIds.add(ref.targetId);
  });

  // Filter to requested IDs if provided
  const targetIds = explainerIds ? new Set(explainerIds) : allIds;

  // Load metadata for all nodes
  const metadataMap = await loadExplainerMetadataBatch(Array.from(targetIds));

  // Build nodes
  const nodes: ReferenceGraphNode[] = Array.from(targetIds)
    .filter(id => metadataMap.has(id))
    .map(id => {
      const metadata = metadataMap.get(id)!;
      return {
        id,
        label: metadata.title,
        category: metadata.category,
        domain: metadata.domain,
      };
    });

  // Build edges (only between nodes in graph)
  const edges: ReferenceGraphEdge[] = references
    .filter(ref => targetIds.has(ref.sourceId) && targetIds.has(ref.targetId))
    .map(ref => ({
      source: ref.sourceId,
      target: ref.targetId,
      type: ref.referenceType,
      strength: ref.strength ?? 0.5,
      label: ref.context,
    }));

  return { nodes, edges };
}

/**
 * Search explainers by query
 */
export async function searchExplainers(
  query: string,
  filter?: ExplainerFilter
): Promise<ExplainerSearchResult[]> {
  // This is a simplified search - in production, you'd want to index content
  const results: ExplainerSearchResult[] = [];
  const queryLower = query.toLowerCase();

  // Load all explainers (in production, use an index)
  // For now, we'll need to maintain a registry of all explainer IDs
  const registryResponse = await fetch('/data/explainers/registry.json');
  if (!registryResponse.ok) {
    console.warn('Explainer registry not found');
    return [];
  }

  const registry = await registryResponse.json();
  const explainerIds: string[] = registry.ids || [];

  // Search through explainers
  for (const id of explainerIds) {
    const metadata = await loadExplainerMetadata(id);
    if (!metadata) continue;

    // Apply filters
    if (filter) {
      if (filter.categories && !filter.categories.includes(metadata.category)) continue;
      if (filter.domains && !filter.domains.includes(metadata.domain)) continue;
      if (filter.status && !filter.status.includes(metadata.status)) continue;
      if (filter.tags && !filter.tags.some(tag => metadata.tags?.includes(tag))) continue;
    }

    // Search in title, description, content
    const matchedFields: string[] = [];
    let relevanceScore = 0;

    if (metadata.title.toLowerCase().includes(queryLower)) {
      matchedFields.push('title');
      relevanceScore += 10;
    }

    if (metadata.description.toLowerCase().includes(queryLower)) {
      matchedFields.push('description');
      relevanceScore += 5;
    }

    if (metadata.content.markdown.toLowerCase().includes(queryLower)) {
      matchedFields.push('content');
      relevanceScore += 1;
    }

    if (metadata.tags?.some(tag => tag.toLowerCase().includes(queryLower))) {
      matchedFields.push('tags');
      relevanceScore += 3;
    }

    if (relevanceScore > 0) {
      results.push({
        id: metadata.id,
        title: metadata.title,
        description: metadata.description,
        category: metadata.category,
        domain: metadata.domain,
        relevanceScore,
        matchedFields,
      });
    }
  }

  // Sort by relevance
  results.sort((a, b) => b.relevanceScore - a.relevanceScore);

  return results;
}

/**
 * Clear caches (useful for development)
 */
export function clearExplainerCache(): void {
  explainerCache.clear();
  crossReferenceCache.clear();
}

/**
 * Preload explainers (for performance)
 */
export async function preloadExplainers(explainerIds: string[]): Promise<void> {
  await loadExplainerMetadataBatch(explainerIds);
}

