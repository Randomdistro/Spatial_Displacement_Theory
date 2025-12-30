/**
 * Content type definitions for SDT 3D Interactive Website
 * Defines the structure for all narrative paths and nodes
 */

export type PathType = 'path1' | 'path2' | 'path3';
export type ExpansionType = 'know-more' | 'tech-specs' | 'simulation' | 'example' | 'history';

export interface ExpansionContent {
  title: string;
  content: string;
  simulationId?: string;
}

export interface NodeContent {
  id: string;
  title: string;
  path: PathType;
  readingTime: number; // minutes
  hook?: string; // Starship Troopers-style hook headline
  content: {
    main: string; // Markdown content
    expansions?: {
      [key: string]: string | ExpansionContent;
    };
  };
  narration?: {
    script: string;
    audioFile?: string;
    duration?: number; // seconds
    timing?: number[]; // segment timestamps in seconds
  };
  visualizations?: {
    animation3d?: string;
    formulas?: string[];
    charts?: string[];
    simulationId?: string;
  };
  position: [number, number, number]; // 3D position in scene
  cameraTarget?: [number, number, number];
  nextNodeId?: string;
  previousNodeId?: string;
}

export interface PathStructure {
  id: PathType;
  name: string;
  description: string;
  targetAudience: string;
  tone: string;
  nodes: NodeContent[];
  cameraPosition: [number, number, number];
}

export interface ContentManifest {
  paths: PathStructure[];
}





