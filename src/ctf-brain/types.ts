/**
 * StrategicKhaos CTF Brain - Type Definitions
 * Rubik's PLL Algorithm → Pentest Methodology Mapping
 */

export interface CTFBrainMetadata {
  name: string;
  version: string;
  author: string;
  description: string;
  philosophy: string;
}

export interface CTFBrainNode {
  name: string;
  pll_analog: string;
  tools: string[];
  triggers: string[];
  description: string;
  expected_output: string[];
}

export interface CTFBrainNodes {
  [key: string]: CTFBrainNode;
}

export type CTFBrainEdge = [string, string];

export interface QuadrantWeights {
  tool_ready: number;
  context_match: number;
  success_rate: number;
  efficiency: number;
}

export interface CTFBrainConfig {
  metadata: CTFBrainMetadata;
  nodes: CTFBrainNodes;
  edges: CTFBrainEdge[];
  quadrant_weights: QuadrantWeights;
}

export interface NodeScore {
  nodeId: string;
  node: CTFBrainNode;
  score: number;
  matchedTriggers: string[];
  reasoning: string;
}

export interface WorkflowPath {
  path: string[];
  description: string;
}
