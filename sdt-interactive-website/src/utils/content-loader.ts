/**
 * Content Loader Utility
 * 
 * Loads content from JSON files for the SDT Interactive Website.
 * Supports all three narrative paths with Veritasium-style VO scripts
 * and "Would you like to know more?" expansion pattern.
 */

import type { NodeContent, PathType, PathStructure } from '../types/content';

// Path metadata with Starship Troopers-style hooks
export const PATH_METADATA: Record<PathType, Omit<PathStructure, 'nodes' | 'cameraPosition'>> = {
  path1: {
    id: 'path1',
    name: 'Quick Tour',
    description: "A 15-minute introduction to SDT's core ideas",
    targetAudience: 'General public, science enthusiasts, students',
    tone: 'Conversational, Veritasium-style, engaging',
  },
  path2: {
    id: 'path2',
    name: 'Deep Dive',
    description: 'Comprehensive exploration of all SDT concepts',
    targetAudience: 'Deep learners, graduate students, curious minds',
    tone: 'Thorough, comprehensive, well-structured',
  },
  path3: {
    id: 'path3',
    name: 'Scientific Framework',
    description: 'Complete mathematical and physical derivation',
    targetAudience: 'Physicists, researchers, peer reviewers',
    tone: 'Formal, precise, mathematically rigorous',
  },
};

// Node manifest for each path
const PATH_NODES: Record<PathType, string[]> = {
  path1: ['node1', 'node2', 'node3', 'node4', 'node5'],
  path2: ['node1', 'node2', 'node3'],
  path3: ['node1', 'node2'],
};

/**
 * Load a single node's content
 */
export async function loadNodeContent(
  path: PathType,
  nodeId: string
): Promise<NodeContent | null> {
  try {
    // Dynamic import for the content file
    const content = await import(`../content/${path}/${nodeId}.json`);
    return content.default || content;
  } catch (error) {
    console.error(`Failed to load content for ${path}/${nodeId}:`, error);
    return null;
  }
}

/**
 * Load all nodes for a path
 */
export async function loadPathContent(path: PathType): Promise<NodeContent[]> {
  const nodeIds = PATH_NODES[path] || [];
  const nodes: NodeContent[] = [];

  for (const nodeId of nodeIds) {
    const content = await loadNodeContent(path, nodeId);
    if (content) {
      nodes.push(content);
    }
  }

  return nodes;
}

/**
 * Load complete path structure with metadata
 */
export async function loadPathStructure(path: PathType): Promise<PathStructure> {
  const metadata = PATH_METADATA[path];
  const nodes = await loadPathContent(path);

  // Camera positions for each path
  const cameraPositions: Record<PathType, [number, number, number]> = {
    path1: [0, 1, 3],
    path2: [0, 0, 4],
    path3: [0, -1, 5],
  };

  return {
    ...metadata,
    nodes,
    cameraPosition: cameraPositions[path],
  };
}

/**
 * Get node summary for path overview
 */
export interface NodeSummary {
  id: string;
  title: string;
  readingTime: number;
  hook?: string;
}

export async function getPathNodeSummaries(path: PathType): Promise<NodeSummary[]> {
  const nodes = await loadPathContent(path);
  return nodes.map((node) => ({
    id: node.id,
    title: node.title,
    readingTime: node.readingTime,
    hook: (node as any).hook,
  }));
}

/**
 * Preload all content for faster navigation
 */
export async function preloadAllContent(): Promise<Map<PathType, NodeContent[]>> {
  const allContent = new Map<PathType, NodeContent[]>();

  const paths: PathType[] = ['path1', 'path2', 'path3'];

  await Promise.all(
    paths.map(async (path) => {
      const nodes = await loadPathContent(path);
      allContent.set(path, nodes);
    })
  );

  return allContent;
}

/**
 * Get narration script for a node
 */
export interface NarrationData {
  script: string;
  duration: number;
  timing: number[];
  audioFile?: string;
}

export function getNarrationData(node: NodeContent): NarrationData | null {
  if (!node.narration) return null;

  return {
    script: node.narration.script,
    duration: node.narration.duration || 60,
    timing: node.narration.timing || [],
    audioFile: node.narration.audioFile,
  };
}

/**
 * Get expansion content (Would you like to know more?)
 */
export interface ExpansionContent {
  id: string;
  title: string;
  content: string;
  simulationId?: string;
}

export function getExpansions(node: NodeContent): ExpansionContent[] {
  if (!node.content.expansions) return [];

  return Object.entries(node.content.expansions).map(([id, expansion]) => {
    if (typeof expansion === 'string') {
      return { id, title: id, content: expansion };
    }
    return {
      id,
      title: expansion.title || id,
      content: expansion.content,
      simulationId: expansion.simulationId,
    };
  });
}


