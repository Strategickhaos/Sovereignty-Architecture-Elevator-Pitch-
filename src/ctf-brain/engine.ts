/**
 * StrategicKhaos CTF Brain - Core Engine
 * Rubik's PLL Algorithm → Pentest Methodology Mapping
 * 
 * Philosophy: "See state → Recognize pattern → Execute algorithm → Objective achieved"
 */

import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import type {
  CTFBrainConfig,
  CTFBrainNode,
  NodeScore,
  WorkflowPath,
  CTFBrainEdge
} from './types.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export class CTFBrain {
  private config: CTFBrainConfig;
  private adjacencyList: Map<string, string[]>;

  constructor(configPath?: string) {
    const path = configPath || join(__dirname, 'config.json');
    this.config = JSON.parse(readFileSync(path, 'utf-8'));
    this.adjacencyList = this.buildAdjacencyList();
  }

  /**
   * Build adjacency list from edges for graph traversal
   */
  private buildAdjacencyList(): Map<string, string[]> {
    const adjList = new Map<string, string[]>();
    
    // Initialize all nodes
    Object.keys(this.config.nodes).forEach(nodeId => {
      adjList.set(nodeId, []);
    });

    // Add edges
    this.config.edges.forEach(([from, to]) => {
      adjList.get(from)?.push(to);
    });

    return adjList;
  }

  /**
   * Get metadata about the CTF Brain
   */
  getMetadata() {
    return this.config.metadata;
  }

  /**
   * Get all nodes
   */
  getAllNodes() {
    return this.config.nodes;
  }

  /**
   * Get a specific node by ID
   */
  getNode(nodeId: string): CTFBrainNode | undefined {
    return this.config.nodes[nodeId];
  }

  /**
   * Get next possible nodes from current node
   */
  getNextNodes(nodeId: string): string[] {
    return this.adjacencyList.get(nodeId) || [];
  }

  /**
   * Find nodes based on trigger keywords
   * Returns scored matches based on context
   */
  findNodesByTrigger(query: string): NodeScore[] {
    const queryLower = query.toLowerCase();
    const queryWords = queryLower.split(/\s+/);
    const scores: NodeScore[] = [];

    Object.entries(this.config.nodes).forEach(([nodeId, node]) => {
      const matchedTriggers: string[] = [];
      let score = 0;

      // Check triggers
      node.triggers.forEach(trigger => {
        const triggerLower = trigger.toLowerCase();
        
        // Exact match
        if (queryLower.includes(triggerLower)) {
          matchedTriggers.push(trigger);
          score += 10;
        }
        
        // Word match
        queryWords.forEach(word => {
          if (triggerLower.includes(word) && word.length > 2) {
            if (!matchedTriggers.includes(trigger)) {
              matchedTriggers.push(trigger);
            }
            score += 3;
          }
        });
      });

      // Check tools
      node.tools.forEach(tool => {
        if (queryLower.includes(tool.toLowerCase())) {
          score += 5;
          if (!matchedTriggers.includes(`tool:${tool}`)) {
            matchedTriggers.push(`tool:${tool}`);
          }
        }
      });

      if (score > 0) {
        scores.push({
          nodeId,
          node,
          score,
          matchedTriggers,
          reasoning: this.generateReasoning(node, matchedTriggers, score)
        });
      }
    });

    // Sort by score descending
    return scores.sort((a, b) => b.score - a.score);
  }

  /**
   * Generate reasoning for why a node was selected
   */
  private generateReasoning(node: CTFBrainNode, triggers: string[], score: number): string {
    const reasons: string[] = [];
    
    if (triggers.length > 0) {
      reasons.push(`Matched ${triggers.length} trigger(s): ${triggers.join(', ')}`);
    }
    
    reasons.push(`PLL Algorithm: ${node.pll_analog}`);
    reasons.push(`Score: ${score}`);
    
    return reasons.join(' | ');
  }

  /**
   * Get workflow path from one node to another
   */
  findPath(startNodeId: string, endNodeId: string): WorkflowPath | null {
    const visited = new Set<string>();
    const path: string[] = [];

    const dfs = (current: string): boolean => {
      if (current === endNodeId) {
        path.push(current);
        return true;
      }

      visited.add(current);
      path.push(current);

      const neighbors = this.adjacencyList.get(current) || [];
      for (const neighbor of neighbors) {
        if (!visited.has(neighbor)) {
          if (dfs(neighbor)) {
            return true;
          }
        }
      }

      path.pop();
      return false;
    };

    if (dfs(startNodeId)) {
      const description = path
        .map(id => this.config.nodes[id].name)
        .join(' → ');

      return { path, description };
    }

    return null;
  }

  /**
   * Get recommended workflow based on current state
   */
  getRecommendedWorkflow(currentNodeId: string): WorkflowPath[] {
    const nextNodes = this.getNextNodes(currentNodeId);
    const workflows: WorkflowPath[] = [];

    nextNodes.forEach(nextNodeId => {
      const node = this.config.nodes[nextNodeId];
      workflows.push({
        path: [currentNodeId, nextNodeId],
        description: `${this.config.nodes[currentNodeId].name} → ${node.name}: ${node.description}`
      });
    });

    return workflows;
  }

  /**
   * Get full workflow graph visualization
   */
  getGraphVisualization(): string {
    const lines: string[] = [];
    lines.push('CTF Brain Workflow Graph:');
    lines.push('='.repeat(50));
    lines.push('');

    Object.entries(this.config.nodes).forEach(([nodeId, node]) => {
      lines.push(`${nodeId}: ${node.name}`);
      lines.push(`  PLL: ${node.pll_analog}`);
      lines.push(`  Tools: ${node.tools.join(', ')}`);
      
      const nextNodes = this.getNextNodes(nodeId);
      if (nextNodes.length > 0) {
        lines.push(`  Next: ${nextNodes.map(id => this.config.nodes[id].name).join(', ')}`);
      }
      lines.push('');
    });

    return lines.join('\n');
  }

  /**
   * Get tools for a specific phase
   */
  getToolsForPhase(nodeId: string): string[] {
    const node = this.config.nodes[nodeId];
    return node ? node.tools : [];
  }

  /**
   * Search for nodes by tool name
   */
  findNodesByTool(toolName: string): NodeScore[] {
    const toolLower = toolName.toLowerCase();
    const results: NodeScore[] = [];

    Object.entries(this.config.nodes).forEach(([nodeId, node]) => {
      const matchingTools = node.tools.filter(tool => 
        tool.toLowerCase().includes(toolLower)
      );

      if (matchingTools.length > 0) {
        results.push({
          nodeId,
          node,
          score: matchingTools.length * 10,
          matchedTriggers: matchingTools.map(t => `tool:${t}`),
          reasoning: `Found tool(s): ${matchingTools.join(', ')}`
        });
      }
    });

    return results.sort((a, b) => b.score - a.score);
  }

  /**
   * Get the quadrant weights configuration
   */
  getQuadrantWeights() {
    return this.config.quadrant_weights;
  }

  /**
   * Get all edges in the graph
   */
  getEdges(): CTFBrainEdge[] {
    return this.config.edges;
  }
}
