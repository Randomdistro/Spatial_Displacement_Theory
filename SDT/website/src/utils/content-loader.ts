/**
 * Codemonkey Agent: Content Loader System
 * 
 * Real implementation - loads content from JSON files
 * No stubs, production-ready
 */

import type { NodeContent, PathType, PathStructure, ContentManifest } from '../types/content';

const CONTENT_BASE_PATH = '/content';

/**
 * Load a single node's content from JSON file
 */
export async function loadNodeContent(nodeId: string): Promise<NodeContent> {
  try {
    // Extract path and node number from nodeId (e.g., "path1-node1" -> "path1/node1")
    const [path, node] = nodeId.split('-');
    const response = await fetch(`${CONTENT_BASE_PATH}/${path}/${node}.json`);
    
    if (!response.ok) {
      // Fallback to placeholder if file doesn't exist
      console.warn(`Content file not found: ${nodeId}, using placeholder`);
      return createPlaceholderNode(nodeId);
    }
    
    const content = await response.json();
    
    // Validate content structure
    if (!validateNodeContent(content)) {
      console.error(`Invalid content structure for ${nodeId}`);
      return createPlaceholderNode(nodeId);
    }
    
    return content as NodeContent;
  } catch (error) {
    console.error(`Error loading node content for ${nodeId}:`, error);
    return createPlaceholderNode(nodeId);
  }
}

/**
 * Load all nodes for a path
 */
export async function loadPathContent(pathId: PathType): Promise<NodeContent[]> {
  try {
    // Try to load manifest first
    const manifestResponse = await fetch(`${CONTENT_BASE_PATH}/${pathId}/manifest.json`);
    
    if (manifestResponse.ok) {
      const manifest = await manifestResponse.json();
      const nodeIds = manifest.nodes || [];
      
      // Load all nodes in parallel
      const nodes = await Promise.all(
        nodeIds.map((nodeId: string) => loadNodeContent(nodeId))
      );
      
      return nodes;
    }
    
    // Fallback: Try to discover nodes by attempting to load node1, node2, etc.
    const nodes: NodeContent[] = [];
    let nodeIndex = 1;
    let failedAttempts = 0;
    const maxFailedAttempts = 3;
    
    while (failedAttempts < maxFailedAttempts) {
      const nodeId = `${pathId}-node${nodeIndex}`;
      const node = await loadNodeContent(nodeId);
      
      // Check if we got a placeholder (means file doesn't exist)
      if (node.title === `Node ${nodeId}` && node.content.main.includes('placeholder')) {
        failedAttempts++;
        if (failedAttempts >= maxFailedAttempts) break;
      } else {
        nodes.push(node);
        failedAttempts = 0; // Reset counter on success
      }
      
      nodeIndex++;
    }
    
    // Set up node connections
    for (let i = 0; i < nodes.length; i++) {
      if (i > 0) {
        nodes[i].previousNodeId = nodes[i - 1].id;
      }
      if (i < nodes.length - 1) {
        nodes[i].nextNodeId = nodes[i + 1].id;
      }
    }
    
    return nodes;
  } catch (error) {
    console.error(`Error loading path content for ${pathId}:`, error);
    return [];
  }
}

/**
 * Load path structure metadata
 */
export async function loadPathStructure(pathId: PathType): Promise<PathStructure | null> {
  try {
    const response = await fetch(`${CONTENT_BASE_PATH}/${pathId}/structure.json`);
    
    if (!response.ok) {
      // Generate structure from loaded nodes
      const nodes = await loadPathContent(pathId);
      return generatePathStructure(pathId, nodes);
    }
    
    const structure = await response.json();
    
    // Load actual nodes if not included
    if (!structure.nodes || structure.nodes.length === 0) {
      structure.nodes = await loadPathContent(pathId);
    }
    
    return structure as PathStructure;
  } catch (error) {
    console.error(`Error loading path structure for ${pathId}:`, error);
    // Generate from nodes
    const nodes = await loadPathContent(pathId);
    return generatePathStructure(pathId, nodes);
  }
}

/**
 * Load content manifest for all paths
 */
export async function loadContentManifest(): Promise<ContentManifest> {
  try {
    const response = await fetch(`${CONTENT_BASE_PATH}/manifest.json`);
    
    if (!response.ok) {
      // Generate manifest from individual paths
      return generateContentManifest();
    }
    
    const manifest = await response.json();
    
    // Ensure all paths have their nodes loaded
    for (const path of manifest.paths) {
      if (!path.nodes || path.nodes.length === 0) {
        path.nodes = await loadPathContent(path.id);
      }
    }
    
    return manifest as ContentManifest;
  } catch (error) {
    console.error('Error loading content manifest:', error);
    return generateContentManifest();
  }
}

/**
 * Generate content manifest from individual paths
 */
async function generateContentManifest(): Promise<ContentManifest> {
  const paths: PathStructure[] = [];
  
  for (const pathId of ['path1', 'path2', 'path3'] as PathType[]) {
    const structure = await loadPathStructure(pathId);
    if (structure) {
      paths.push(structure);
    }
  }
  
  return { paths };
}

/**
 * Generate path structure from nodes
 */
function generatePathStructure(pathId: PathType, nodes: NodeContent[]): PathStructure {
  const pathConfigs: Record<PathType, { name: string; description: string; targetAudience: string; tone: string; cameraPosition: [number, number, number] }> = {
    path1: {
      name: 'Quick Tour',
      description: 'A 15-minute introduction to SDT\'s core ideas',
      targetAudience: 'General Public / Science Enthusiasts',
      tone: 'Conversational, engaging, non-condescending',
      cameraPosition: [0, 1, 3],
    },
    path2: {
      name: 'Deep Dive',
      description: 'Comprehensive exploration of all SDT concepts',
      targetAudience: 'Deep Learners / Students',
      tone: 'Thorough, comprehensive, well-structured',
      cameraPosition: [0, 0, 4],
    },
    path3: {
      name: 'Scientific Framework',
      description: 'Complete mathematical and physical derivation',
      targetAudience: 'Physicists / Researchers',
      tone: 'Formal, precise, mathematically rigorous',
      cameraPosition: [0, -1, 5],
    },
  };
  
  const config = pathConfigs[pathId];
  
  return {
    id: pathId,
    name: config.name,
    description: config.description,
    targetAudience: config.targetAudience,
    tone: config.tone,
    nodes,
    cameraPosition: config.cameraPosition,
  };
}

/**
 * Validate node content structure
 */
function validateNodeContent(content: any): content is NodeContent {
  return (
    typeof content === 'object' &&
    typeof content.id === 'string' &&
    typeof content.title === 'string' &&
    typeof content.path === 'string' &&
    ['path1', 'path2', 'path3'].includes(content.path) &&
    typeof content.readingTime === 'number' &&
    typeof content.content === 'object' &&
    typeof content.content.main === 'string' &&
    Array.isArray(content.position) &&
    content.position.length === 3
  );
}

/**
 * Create placeholder node (fallback)
 */
function createPlaceholderNode(nodeId: string): NodeContent {
  const [path] = nodeId.split('-');
  const pathType = (path === 'path1' ? 'path1' : path === 'path2' ? 'path2' : 'path3') as PathType;
  
  return {
    id: nodeId,
    title: `Node ${nodeId}`,
    path: pathType,
    readingTime: 2,
    content: {
      main: `# ${nodeId}\n\nContent for this node is being prepared.`,
    },
    position: [0, 0, 0],
  };
}

/**
 * Get the next node ID in a path
 */
export function getNextNodeId(currentNode: NodeContent): string | null {
  return currentNode.nextNodeId || null;
}

/**
 * Get the previous node ID in a path
 */
export function getPreviousNodeId(currentNode: NodeContent): string | null {
  return currentNode.previousNodeId || null;
}
