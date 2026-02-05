#!/usr/bin/env node
/**
 * Neon Database CLI Tool
 * 
 * Command-line utility for managing the Strategickhaos Empire database
 * 
 * Usage:
 *   node neon-cli.js status              - Show database status
 *   node neon-cli.js inventions list     - List all inventions
 *   node neon-cli.js inventions add      - Add new invention (interactive)
 *   node neon-cli.js entities list       - List legal entities
 *   node neon-cli.js council list        - List AI council members
 *   node neon-cli.js nodes list          - List cluster nodes
 *   node neon-cli.js nodes heartbeat     - Send node heartbeat
 *   node neon-cli.js events log          - Log swarm event
 */

import pkg from 'pg';
const { Client } = pkg;
import * as dotenv from 'dotenv';
import readline from 'readline';

dotenv.config();

const client = new Client({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function ask(question) {
  return new Promise(resolve => {
    rl.question(question, answer => {
      resolve(answer);
    });
  });
}

async function showStatus() {
  try {
    await client.connect();
    
    // Get counts
    const inventions = await client.query('SELECT COUNT(*) as count FROM inventions;');
    const entities = await client.query('SELECT COUNT(*) as count FROM legal_entities;');
    const council = await client.query('SELECT COUNT(*) as count FROM ai_council;');
    const nodes = await client.query('SELECT COUNT(*) as count FROM cluster_nodes;');
    const events = await client.query('SELECT COUNT(*) as count FROM swarm_events WHERE created_at > NOW() - INTERVAL \'24 hours\';');
    
    // Get genome version
    const genome = await client.query('SELECT version, overall_score FROM genome_metadata ORDER BY created_at DESC LIMIT 1;');
    
    console.log('╔══════════════════════════════════════════════════╗');
    console.log('║     STRATEGICKHAOS EMPIRE DATABASE STATUS       ║');
    console.log('╚══════════════════════════════════════════════════╝\n');
    
    if (genome.rows.length > 0) {
      console.log(`📊 Genome Version: ${genome.rows[0].version}`);
      console.log(`🎯 Overall Score: ${genome.rows[0].overall_score}\n`);
    }
    
    console.log('📈 Record Counts:');
    console.log(`  Inventions:       ${inventions.rows[0].count}`);
    console.log(`  Legal Entities:   ${entities.rows[0].count}`);
    console.log(`  AI Council:       ${council.rows[0].count}`);
    console.log(`  Cluster Nodes:    ${nodes.rows[0].count}`);
    console.log(`  Events (24h):     ${events.rows[0].count}`);
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  } finally {
    await client.end();
  }
}

async function listInventions() {
  try {
    await client.connect();
    
    const result = await client.query(`
      SELECT invention_id, title, classification, status, created_at
      FROM inventions
      ORDER BY invention_id;
    `);
    
    console.log('\n📚 INVENTIONS\n');
    console.log('ID          | Title                                    | Class       | Status');
    console.log('------------|------------------------------------------|-------------|----------');
    
    result.rows.forEach(row => {
      const id = row.invention_id.padEnd(11);
      const title = row.title.substring(0, 40).padEnd(40);
      const classification = row.classification.padEnd(11);
      const status = row.status;
      console.log(`${id} | ${title} | ${classification} | ${status}`);
    });
    
    console.log(`\nTotal: ${result.rows.length} inventions`);
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  } finally {
    await client.end();
  }
}

async function addInvention() {
  try {
    await client.connect();
    
    console.log('\n📝 ADD NEW INVENTION\n');
    
    const inventionId = await ask('Invention ID (e.g., INV-042): ');
    const title = await ask('Title: ');
    const classification = await ask('Classification (NOVEL/CONVERGENT/HYBRID): ');
    const status = await ask('Status (NEW/DEPLOYED/PLANNED/RESEARCH): ');
    const description = await ask('Description: ');
    
    await client.query(`
      INSERT INTO inventions (invention_id, title, classification, status, description)
      VALUES ($1, $2, $3, $4, $5)
    `, [inventionId, title, classification.toUpperCase(), status.toUpperCase(), description]);
    
    console.log('\n✅ Invention added successfully!');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  } finally {
    rl.close();
    await client.end();
  }
}

async function listEntities() {
  try {
    await client.connect();
    
    const result = await client.query(`
      SELECT entity_id, name, ein, status, role
      FROM legal_entities
      ORDER BY entity_id;
    `);
    
    console.log('\n🏛️  LEGAL ENTITIES\n');
    
    result.rows.forEach(row => {
      console.log(`ID:     ${row.entity_id}`);
      console.log(`Name:   ${row.name}`);
      console.log(`EIN:    ${row.ein || 'PENDING'}`);
      console.log(`Status: ${row.status}`);
      console.log(`Role:   ${row.role}`);
      console.log('─────────────────────────────────────────────────');
    });
    
    console.log(`Total: ${result.rows.length} entities`);
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  } finally {
    await client.end();
  }
}

async function listCouncil() {
  try {
    await client.connect();
    
    const result = await client.query(`
      SELECT council_id, name, role, aol_tier, specialization
      FROM ai_council
      ORDER BY council_id;
    `);
    
    console.log('\n🤖 AI COUNCIL (Legion of Minds)\n');
    
    result.rows.forEach(row => {
      console.log(`${row.name} (${row.aol_tier})`);
      console.log(`  Role: ${row.role}`);
      console.log(`  Specialization: ${row.specialization}`);
      console.log('─────────────────────────────────────────────────');
    });
    
    console.log(`Total: ${result.rows.length} council members`);
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  } finally {
    await client.end();
  }
}

async function listNodes() {
  try {
    await client.connect();
    
    const result = await client.query(`
      SELECT node_id, name, type, ram, status, role
      FROM cluster_nodes
      ORDER BY node_id;
    `);
    
    console.log('\n🖥️  CLUSTER NODES\n');
    
    result.rows.forEach(row => {
      console.log(`${row.name} (${row.status})`);
      console.log(`  Type: ${row.type}`);
      console.log(`  RAM:  ${row.ram || 'N/A'}`);
      console.log(`  Role: ${row.role}`);
      console.log('─────────────────────────────────────────────────');
    });
    
    console.log(`Total: ${result.rows.length} nodes`);
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  } finally {
    await client.end();
  }
}

async function sendHeartbeat() {
  try {
    await client.connect();
    
    const nodeId = await ask('Node ID (e.g., INFRA-001): ');
    const cpuUsage = parseFloat(await ask('CPU Usage % (0-100): '));
    const ramUsage = parseFloat(await ask('RAM Usage % (0-100): '));
    const diskUsage = parseFloat(await ask('Disk Usage % (0-100): '));
    
    await client.query(`
      INSERT INTO node_metrics (node_id, cpu_usage, ram_usage, disk_usage)
      VALUES ($1, $2, $3, $4)
    `, [nodeId, cpuUsage, ramUsage, diskUsage]);
    
    console.log('\n✅ Heartbeat logged successfully!');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  } finally {
    rl.close();
    await client.end();
  }
}

async function logEvent() {
  try {
    await client.connect();
    
    const eventType = await ask('Event Type: ');
    const source = await ask('Source: ');
    const description = await ask('Description: ');
    
    const eventId = `EVT-${Date.now()}`;
    
    await client.query(`
      INSERT INTO swarm_events (event_id, event_type, source, description)
      VALUES ($1, $2, $3, $4)
    `, [eventId, eventType, source, description]);
    
    console.log(`\n✅ Event logged: ${eventId}`);
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  } finally {
    rl.close();
    await client.end();
  }
}

// Parse command
const args = process.argv.slice(2);

if (args.length === 0 || args[0] === 'status') {
  showStatus();
} else if (args[0] === 'inventions' && args[1] === 'list') {
  listInventions();
} else if (args[0] === 'inventions' && args[1] === 'add') {
  addInvention();
} else if (args[0] === 'entities' && args[1] === 'list') {
  listEntities();
} else if (args[0] === 'council' && args[1] === 'list') {
  listCouncil();
} else if (args[0] === 'nodes' && args[1] === 'list') {
  listNodes();
} else if (args[0] === 'nodes' && args[1] === 'heartbeat') {
  sendHeartbeat();
} else if (args[0] === 'events' && args[1] === 'log') {
  logEvent();
} else {
  console.log('Usage:');
  console.log('  node neon-cli.js status              - Show database status');
  console.log('  node neon-cli.js inventions list     - List all inventions');
  console.log('  node neon-cli.js inventions add      - Add new invention');
  console.log('  node neon-cli.js entities list       - List legal entities');
  console.log('  node neon-cli.js council list        - List AI council members');
  console.log('  node neon-cli.js nodes list          - List cluster nodes');
  console.log('  node neon-cli.js nodes heartbeat     - Send node heartbeat');
  console.log('  node neon-cli.js events log          - Log swarm event');
}
