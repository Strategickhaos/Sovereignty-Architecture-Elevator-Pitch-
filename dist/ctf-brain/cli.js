#!/usr/bin/env node
/**
 * StrategicKhaos CTF Brain - CLI Interface
 * Interactive pentest methodology guidance
 */
import { CTFBrain } from './engine.js';
const brain = new CTFBrain();
function printBanner() {
    console.log(`
╔═══════════════════════════════════════════════════════════╗
║         StrategicKhaos CTF Brain v1.0.0                  ║
║    Rubik's PLL Algorithm → Pentest Methodology Mapping   ║
╚═══════════════════════════════════════════════════════════╝

Philosophy: See state → Recognize pattern → Execute algorithm → Objective achieved
Author: Dom (Me10101) - Strategickhaos DAO LLC
`);
}
function printHelp() {
    console.log(`
Commands:
  query <keywords>     - Find methodology nodes based on keywords
  tool <toolname>      - Find nodes that use a specific tool
  node <node-id>       - Get details about a specific node
  next <node-id>       - Get recommended next steps from a node
  path <from> <to>     - Find workflow path between two nodes
  list                 - List all methodology nodes
  graph                - Show full workflow graph
  help                 - Show this help message
  exit                 - Exit the program

Examples:
  query web application sql injection
  tool nmap
  node 01-Ua-Recon
  next 04-Z-Exploit
  path 01-Ua-Recon 08-T-Exfil
`);
}
function printNodeDetails(nodeId, node) {
    console.log(`
┌─────────────────────────────────────────────────────────┐
│ ${nodeId}: ${node.name.padEnd(48)} │
└─────────────────────────────────────────────────────────┘

📋 Description: ${node.description}
🧩 PLL Algorithm: ${node.pll_analog}

🛠️  Tools:
${node.tools.map((t) => `   • ${t}`).join('\n')}

🎯 Triggers:
${node.triggers.map((t) => `   • ${t}`).join('\n')}

📊 Expected Output:
${node.expected_output.map((o) => `   • ${o}`).join('\n')}
`);
}
function handleQuery(args) {
    const query = args.join(' ');
    if (!query) {
        console.log('❌ Error: Please provide search keywords');
        return;
    }
    console.log(`\n🔍 Searching for: "${query}"\n`);
    const results = brain.findNodesByTrigger(query);
    if (results.length === 0) {
        console.log('No matching nodes found.');
        return;
    }
    console.log(`Found ${results.length} matching node(s):\n`);
    results.forEach((result, index) => {
        console.log(`${index + 1}. ${result.nodeId}: ${result.node.name}`);
        console.log(`   Score: ${result.score} | ${result.reasoning}`);
        console.log(`   Description: ${result.node.description}`);
        console.log(`   PLL: ${result.node.pll_analog}\n`);
    });
}
function handleTool(args) {
    const toolName = args.join(' ');
    if (!toolName) {
        console.log('❌ Error: Please provide a tool name');
        return;
    }
    console.log(`\n🔧 Searching for tool: "${toolName}"\n`);
    const results = brain.findNodesByTool(toolName);
    if (results.length === 0) {
        console.log('No nodes found using this tool.');
        return;
    }
    console.log(`Found ${results.length} node(s) using this tool:\n`);
    results.forEach((result, index) => {
        console.log(`${index + 1}. ${result.nodeId}: ${result.node.name}`);
        console.log(`   ${result.reasoning}\n`);
    });
}
function handleNode(args) {
    const nodeId = args[0];
    if (!nodeId) {
        console.log('❌ Error: Please provide a node ID');
        return;
    }
    const node = brain.getNode(nodeId);
    if (!node) {
        console.log(`❌ Error: Node "${nodeId}" not found`);
        return;
    }
    printNodeDetails(nodeId, node);
    const nextNodes = brain.getNextNodes(nodeId);
    if (nextNodes.length > 0) {
        console.log('➡️  Next possible steps:');
        nextNodes.forEach(id => {
            const n = brain.getNode(id);
            console.log(`   • ${id}: ${n?.name}`);
        });
        console.log('');
    }
}
function handleNext(args) {
    const nodeId = args[0];
    if (!nodeId) {
        console.log('❌ Error: Please provide a node ID');
        return;
    }
    const node = brain.getNode(nodeId);
    if (!node) {
        console.log(`❌ Error: Node "${nodeId}" not found`);
        return;
    }
    const workflows = brain.getRecommendedWorkflow(nodeId);
    if (workflows.length === 0) {
        console.log(`\nNo next steps available from ${nodeId}: ${node.name}`);
        return;
    }
    console.log(`\n📍 Current: ${nodeId}: ${node.name}`);
    console.log('➡️  Recommended next steps:\n');
    workflows.forEach((workflow, index) => {
        console.log(`${index + 1}. ${workflow.description}\n`);
    });
}
function handlePath(args) {
    if (args.length < 2) {
        console.log('❌ Error: Please provide start and end node IDs');
        console.log('Example: path 01-Ua-Recon 08-T-Exfil');
        return;
    }
    const [start, end] = args;
    const path = brain.findPath(start, end);
    if (!path) {
        console.log(`\n❌ No path found from ${start} to ${end}`);
        return;
    }
    console.log(`\n🗺️  Workflow Path:\n`);
    console.log(path.description);
    console.log('\nDetailed steps:');
    path.path.forEach((nodeId, index) => {
        const node = brain.getNode(nodeId);
        console.log(`\n${index + 1}. ${nodeId}: ${node?.name}`);
        console.log(`   ${node?.description}`);
        console.log(`   PLL: ${node?.pll_analog}`);
    });
    console.log('');
}
function handleList() {
    console.log('\n📋 All CTF Brain Nodes:\n');
    const nodes = brain.getAllNodes();
    Object.entries(nodes).forEach(([nodeId, node]) => {
        console.log(`${nodeId}: ${node.name}`);
        console.log(`   ${node.description}`);
        console.log(`   PLL: ${node.pll_analog}\n`);
    });
}
function handleGraph() {
    console.log(brain.getGraphVisualization());
}
function processCommand(input) {
    const parts = input.trim().split(/\s+/);
    const command = parts[0].toLowerCase();
    const args = parts.slice(1);
    switch (command) {
        case 'query':
            handleQuery(args);
            break;
        case 'tool':
            handleTool(args);
            break;
        case 'node':
            handleNode(args);
            break;
        case 'next':
            handleNext(args);
            break;
        case 'path':
            handlePath(args);
            break;
        case 'list':
            handleList();
            break;
        case 'graph':
            handleGraph();
            break;
        case 'help':
            printHelp();
            break;
        case 'exit':
        case 'quit':
            console.log('\n👋 Goodbye!\n');
            process.exit(0);
            break;
        case '':
            break;
        default:
            console.log(`❌ Unknown command: ${command}`);
            console.log('Type "help" for available commands');
    }
}
// Handle command line arguments
const args = process.argv.slice(2);
if (args.length > 0) {
    // Non-interactive mode
    printBanner();
    processCommand(args.join(' '));
}
else {
    // Interactive mode
    printBanner();
    printHelp();
    const readline = require('readline');
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
        prompt: 'ctf-brain> '
    });
    rl.prompt();
    rl.on('line', (input) => {
        processCommand(input);
        rl.prompt();
    });
    rl.on('close', () => {
        console.log('\n👋 Goodbye!\n');
        process.exit(0);
    });
}
