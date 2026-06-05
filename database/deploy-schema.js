#!/usr/bin/env node
/**
 * Neon Database Schema Deployment Script
 * 
 * Deploys the 17-table schema for the Strategickhaos Empire
 * Core nervous system infrastructure
 * 
 * Usage: node deploy-schema.js
 * Requires: DATABASE_URL environment variable
 */

import pkg from 'pg';
const { Client } = pkg;
import * as dotenv from 'dotenv';

dotenv.config();

const client = new Client({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});

const schema = `
-- ═══════════════════════════════════════════════════════════════════════════
-- STRATEGICKHAOS EMPIRE DATABASE SCHEMA
-- Version: 1.0.0
-- Purpose: Central nervous system for sovereignty architecture
-- ═══════════════════════════════════════════════════════════════════════════

-- CORE DOMAIN TABLES
-- ═══════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS legal_entities (
  id SERIAL PRIMARY KEY,
  entity_id VARCHAR(50) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  ein VARCHAR(20),
  file_number VARCHAR(50),
  status VARCHAR(50) NOT NULL,
  role TEXT,
  formation_date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS inventions (
  id SERIAL PRIMARY KEY,
  invention_id VARCHAR(50) UNIQUE NOT NULL,
  title VARCHAR(500) NOT NULL,
  classification VARCHAR(50) NOT NULL, -- NOVEL, CONVERGENT, HYBRID
  status VARCHAR(50) NOT NULL, -- DEPLOYED, NEW, PLANNED, RESEARCH
  description TEXT,
  patent_filed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_council (
  id SERIAL PRIMARY KEY,
  council_id VARCHAR(50) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  role VARCHAR(255) NOT NULL,
  aol_tier VARCHAR(50) NOT NULL, -- SOVEREIGN, TRUSTED, VERIFIED
  status VARCHAR(50) NOT NULL,
  specialization TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cluster_nodes (
  id SERIAL PRIMARY KEY,
  node_id VARCHAR(50) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  type VARCHAR(100) NOT NULL, -- primary_node, compute_node, mobile_node, etc.
  ram VARCHAR(50),
  status VARCHAR(50) NOT NULL,
  role TEXT,
  endpoint VARCHAR(255),
  region VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS genome_metadata (
  id SERIAL PRIMARY KEY,
  version VARCHAR(50) UNIQUE NOT NULL,
  generation INTEGER NOT NULL,
  birth_date DATE,
  last_updated TIMESTAMP,
  operator VARCHAR(255),
  entity VARCHAR(255),
  overall_score DECIMAL(3,2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- OPERATIONAL TABLES
-- ═══════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS council_sessions (
  id SERIAL PRIMARY KEY,
  session_id VARCHAR(100) UNIQUE NOT NULL,
  topic VARCHAR(500) NOT NULL,
  consensus_reached BOOLEAN,
  human_veto BOOLEAN DEFAULT FALSE,
  session_date TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS model_votes (
  id SERIAL PRIMARY KEY,
  session_id VARCHAR(100) REFERENCES council_sessions(session_id),
  council_member_id VARCHAR(50) REFERENCES ai_council(council_id),
  vote VARCHAR(50) NOT NULL, -- APPROVE, REJECT, ABSTAIN
  reasoning TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS consensus_outcomes (
  id SERIAL PRIMARY KEY,
  session_id VARCHAR(100) REFERENCES council_sessions(session_id),
  decision VARCHAR(50) NOT NULL, -- APPROVED, REJECTED, DEFERRED
  vote_count_approve INTEGER,
  vote_count_reject INTEGER,
  vote_count_abstain INTEGER,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS compilation_runs (
  id SERIAL PRIMARY KEY,
  run_id VARCHAR(100) UNIQUE NOT NULL,
  source_file VARCHAR(500),
  success BOOLEAN NOT NULL,
  error_count INTEGER DEFAULT 0,
  warning_count INTEGER DEFAULT 0,
  execution_time_ms INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transformation_logs (
  id SERIAL PRIMARY KEY,
  run_id VARCHAR(100) REFERENCES compilation_runs(run_id),
  stage VARCHAR(100) NOT NULL, -- lexer, parser, transformer, codegen
  status VARCHAR(50) NOT NULL,
  details TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS flamelang_stdlib (
  id SERIAL PRIMARY KEY,
  function_name VARCHAR(255) UNIQUE NOT NULL,
  signature TEXT NOT NULL,
  description TEXT,
  category VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS task_queue (
  id SERIAL PRIMARY KEY,
  task_id VARCHAR(100) UNIQUE NOT NULL,
  task_type VARCHAR(100) NOT NULL,
  priority INTEGER DEFAULT 5,
  status VARCHAR(50) NOT NULL, -- PENDING, IN_PROGRESS, COMPLETED, FAILED
  payload JSONB,
  assigned_node VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS node_metrics (
  id SERIAL PRIMARY KEY,
  node_id VARCHAR(50) REFERENCES cluster_nodes(node_id),
  cpu_usage DECIMAL(5,2),
  ram_usage DECIMAL(5,2),
  disk_usage DECIMAL(5,2),
  network_in_mbps DECIMAL(10,2),
  network_out_mbps DECIMAL(10,2),
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS swarm_events (
  id SERIAL PRIMARY KEY,
  event_id VARCHAR(100) UNIQUE NOT NULL,
  event_type VARCHAR(100) NOT NULL,
  source VARCHAR(255),
  description TEXT,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS patent_filings (
  id SERIAL PRIMARY KEY,
  invention_id VARCHAR(50) REFERENCES inventions(invention_id),
  filing_type VARCHAR(50) NOT NULL, -- PROVISIONAL, NON_PROVISIONAL, PCT
  filing_date DATE,
  application_number VARCHAR(100),
  status VARCHAR(50) NOT NULL,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS prior_art (
  id SERIAL PRIMARY KEY,
  invention_id VARCHAR(50) REFERENCES inventions(invention_id),
  source VARCHAR(255) NOT NULL,
  url TEXT,
  relevance_score DECIMAL(3,2),
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS provenance_chain (
  id SERIAL PRIMARY KEY,
  record_id VARCHAR(100) UNIQUE NOT NULL,
  record_type VARCHAR(100) NOT NULL,
  record_data JSONB NOT NULL,
  previous_hash VARCHAR(64),
  current_hash VARCHAR(64) NOT NULL,
  signature TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- INDEXES
-- ═══════════════════════════════════════════════════════════════════════════

CREATE INDEX IF NOT EXISTS idx_inventions_status ON inventions(status);
CREATE INDEX IF NOT EXISTS idx_inventions_classification ON inventions(classification);
CREATE INDEX IF NOT EXISTS idx_task_queue_status ON task_queue(status);
CREATE INDEX IF NOT EXISTS idx_task_queue_priority ON task_queue(priority);
CREATE INDEX IF NOT EXISTS idx_node_metrics_timestamp ON node_metrics(timestamp);
CREATE INDEX IF NOT EXISTS idx_swarm_events_type ON swarm_events(event_type);
CREATE INDEX IF NOT EXISTS idx_council_sessions_date ON council_sessions(session_date);

-- TRIGGERS FOR UPDATED_AT
-- ═══════════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = CURRENT_TIMESTAMP;
   RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_legal_entities_updated_at BEFORE UPDATE ON legal_entities
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_inventions_updated_at BEFORE UPDATE ON inventions
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ai_council_updated_at BEFORE UPDATE ON ai_council
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_cluster_nodes_updated_at BEFORE UPDATE ON cluster_nodes
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
`;

async function deploySchema() {
  try {
    console.log('🔗 Connecting to Neon database...');
    await client.connect();
    console.log('✅ Connected successfully');

    console.log('🚀 Deploying schema...');
    await client.query(schema);
    console.log('✅ Schema deployed successfully');

    // Verify tables
    const result = await client.query(`
      SELECT table_name 
      FROM information_schema.tables 
      WHERE table_schema = 'public' 
      ORDER BY table_name;
    `);

    console.log('\n📊 Tables created:');
    result.rows.forEach(row => {
      console.log(`  - ${row.table_name}`);
    });

    console.log(`\n✅ Total: ${result.rows.length} tables`);

  } catch (error) {
    console.error('❌ Error deploying schema:', error);
    process.exit(1);
  } finally {
    await client.end();
  }
}

deploySchema();
