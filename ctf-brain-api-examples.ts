#!/usr/bin/env tsx
/**
 * CTF Brain API Usage Examples
 * Demonstrates how to use the CTF Brain programmatically in TypeScript/JavaScript
 */

import { CTFBrain } from './src/ctf-brain/index.js';

// Initialize the CTF Brain
const brain = new CTFBrain();

console.log('╔═══════════════════════════════════════════════════════════╗');
console.log('║         CTF Brain Programmatic API Examples              ║');
console.log('╚═══════════════════════════════════════════════════════════╝\n');

// Example 1: Get metadata
console.log('Example 1: Get CTF Brain Metadata');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
const metadata = brain.getMetadata();
console.log(`Name: ${metadata.name}`);
console.log(`Version: ${metadata.version}`);
console.log(`Author: ${metadata.author}`);
console.log(`Philosophy: ${metadata.philosophy}\n`);

// Example 2: Query nodes by trigger
console.log('Example 2: Find Nodes by Trigger Keywords');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
const webResults = brain.findNodesByTrigger('web sql injection');
console.log(`Query: "web sql injection"`);
console.log(`Found ${webResults.length} matching node(s):\n`);
webResults.forEach(result => {
  console.log(`  ${result.nodeId}: ${result.node.name}`);
  console.log(`  Score: ${result.score}`);
  console.log(`  Matched Triggers: ${result.matchedTriggers.join(', ')}`);
  console.log(`  PLL: ${result.node.pll_analog}\n`);
});

// Example 3: Get specific node details
console.log('Example 3: Get Node Details');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
const reconNode = brain.getNode('01-Ua-Recon');
if (reconNode) {
  console.log(`Node: 01-Ua-Recon - ${reconNode.name}`);
  console.log(`Description: ${reconNode.description}`);
  console.log(`PLL: ${reconNode.pll_analog}`);
  console.log(`Tools: ${reconNode.tools.join(', ')}`);
  console.log(`Triggers: ${reconNode.triggers.join(', ')}\n`);
}

// Example 4: Get next possible steps
console.log('Example 4: Get Next Steps from a Node');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
const nextSteps = brain.getNextNodes('04-Z-Exploit');
console.log('After exploitation (04-Z-Exploit), next steps:');
nextSteps.forEach(nodeId => {
  const node = brain.getNode(nodeId);
  console.log(`  → ${nodeId}: ${node?.name}`);
});
console.log('');

// Example 5: Get recommended workflows
console.log('Example 5: Get Recommended Workflows');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
const workflows = brain.getRecommendedWorkflow('04-Z-Exploit');
console.log('Recommended workflows from Exploitation:');
workflows.forEach((workflow, index) => {
  console.log(`  ${index + 1}. ${workflow.description}`);
});
console.log('');

// Example 6: Find path between nodes
console.log('Example 6: Find Workflow Path');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
const path = brain.findPath('01-Ua-Recon', '08-T-Exfil');
if (path) {
  console.log('Path from Reconnaissance to Exfiltration:');
  console.log(`  ${path.description}`);
  console.log('\nDetailed path:');
  path.path.forEach((nodeId, index) => {
    const node = brain.getNode(nodeId);
    console.log(`  ${index + 1}. ${nodeId}: ${node?.name}`);
  });
}
console.log('');

// Example 7: Find nodes by tool
console.log('Example 7: Find Nodes by Tool');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
const nmapNodes = brain.findNodesByTool('nmap');
console.log('Nodes that use nmap:');
nmapNodes.forEach(result => {
  console.log(`  ${result.nodeId}: ${result.node.name}`);
  console.log(`    Tools: ${result.node.tools.join(', ')}`);
});
console.log('');

// Example 8: Get tools for a specific phase
console.log('Example 8: Get Tools for a Phase');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
const webAppTools = brain.getToolsForPhase('03-H-WebApp');
console.log('Tools for Web Application phase:');
webAppTools.forEach(tool => {
  console.log(`  • ${tool}`);
});
console.log('');

// Example 9: Get quadrant weights
console.log('Example 9: Get Quadrant Weights');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
const weights = brain.getQuadrantWeights();
console.log('Scoring weights used by CTF Brain:');
console.log(`  Tool Ready: ${weights.tool_ready * 100}%`);
console.log(`  Context Match: ${weights.context_match * 100}%`);
console.log(`  Success Rate: ${weights.success_rate * 100}%`);
console.log(`  Efficiency: ${weights.efficiency * 100}%`);
console.log('');

// Example 10: Get all edges (connections)
console.log('Example 10: Get Workflow Edges');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
const edges = brain.getEdges();
console.log(`Total workflow connections: ${edges.length}`);
console.log('Sample edges:');
edges.slice(0, 5).forEach(([from, to]) => {
  const fromNode = brain.getNode(from);
  const toNode = brain.getNode(to);
  console.log(`  ${from} (${fromNode?.name}) → ${to} (${toNode?.name})`);
});
console.log('');

// Example 11: Custom workflow advisor
console.log('Example 11: Custom Workflow Advisor');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

function getWorkflowAdvice(currentPhase: string, findings: string[]): string {
  const nextSteps = brain.getRecommendedWorkflow(currentPhase);
  
  // Score each next step based on findings
  const scored = nextSteps.map(workflow => {
    const targetNodeId = workflow.path[1];
    const targetNode = brain.getNode(targetNodeId);
    
    if (!targetNode) return { workflow, score: 0 };
    
    // Count how many findings match the target node's triggers
    const matchCount = findings.filter(finding => 
      targetNode.triggers.some(trigger => 
        finding.toLowerCase().includes(trigger.toLowerCase())
      )
    ).length;
    
    return { workflow, score: matchCount };
  });
  
  // Sort by score and get the best match
  scored.sort((a, b) => b.score - a.score);
  
  if (scored.length > 0 && scored[0].score > 0) {
    return `Recommended: ${scored[0].workflow.description}`;
  }
  
  return `Continue with: ${nextSteps[0]?.description || 'No recommendation'}`;
}

// Simulate findings from an assessment
const currentPhase = '02-Ub-Enum';
const findings = [
  'Found login form',
  'SQL database detected',
  'Possible injection point in search',
];

console.log(`Current Phase: ${currentPhase}`);
console.log('Findings:', findings);
console.log('\nAdvice:', getWorkflowAdvice(currentPhase, findings));
console.log('');

// Example 12: Get all nodes
console.log('Example 12: List All Nodes');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
const allNodes = brain.getAllNodes();
console.log(`Total methodology nodes: ${Object.keys(allNodes).length}`);
Object.entries(allNodes).forEach(([nodeId, node]) => {
  console.log(`  ${nodeId}: ${node.name} (${node.pll_analog.split(' - ')[0]})`);
});
console.log('');

console.log('╔═══════════════════════════════════════════════════════════╗');
console.log('║         All Examples Complete!                           ║');
console.log('╚═══════════════════════════════════════════════════════════╝');
