#!/usr/bin/env node
/**
 * Empire Genome Importer
 * 
 * Imports data from EMPIRE_GENOME_v1.7.yaml into Neon database
 * Handles inventions, legal entities, AI council, cluster nodes, and genome metadata
 * 
 * Usage: node import-genome.js
 * Requires: DATABASE_URL environment variable
 */

import pkg from 'pg';
const { Client } = pkg;
import * as dotenv from 'dotenv';
import fs from 'fs';
import yaml from 'js-yaml';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

dotenv.config();

const client = new Client({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});

async function importGenome() {
  try {
    // Load EMPIRE_GENOME_v1.7.yaml
    const genomePath = path.join(__dirname, '..', 'EMPIRE_GENOME_v1.7.yaml');
    console.log(`📖 Reading genome from: ${genomePath}`);
    
    if (!fs.existsSync(genomePath)) {
      throw new Error(`Genome file not found at ${genomePath}`);
    }

    const genomeData = yaml.load(fs.readFileSync(genomePath, 'utf8'));
    console.log('✅ Genome loaded successfully\n');

    await client.connect();
    console.log('🔗 Connected to Neon database\n');

    // Import genome metadata
    console.log('📥 Importing genome metadata...');
    await client.query(`
      INSERT INTO genome_metadata (version, generation, birth_date, last_updated, operator, entity, overall_score)
      VALUES ($1, $2, $3, $4, $5, $6, $7)
      ON CONFLICT (version) DO UPDATE
      SET generation = EXCLUDED.generation,
          last_updated = EXCLUDED.last_updated,
          overall_score = EXCLUDED.overall_score
    `, [
      genomeData.metadata.version,
      genomeData.metadata.generation,
      genomeData.metadata.birth_date,
      genomeData.metadata.last_updated,
      genomeData.metadata.operator,
      genomeData.metadata.entity,
      genomeData.fitness.overall_score
    ]);
    console.log(`✅ Genome metadata: v${genomeData.metadata.version}`);

    // Import legal entities
    console.log('\n📥 Importing legal entities...');
    let entityCount = 0;
    for (const gene of genomeData.chromosomes.LEGAL.genes) {
      await client.query(`
        INSERT INTO legal_entities (entity_id, name, ein, file_number, status, role, formation_date)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        ON CONFLICT (entity_id) DO UPDATE
        SET name = EXCLUDED.name,
            ein = EXCLUDED.ein,
            file_number = EXCLUDED.file_number,
            status = EXCLUDED.status,
            role = EXCLUDED.role
      `, [
        gene.id,
        gene.name,
        gene.ein || null,
        gene.file_number || null,
        gene.status,
        gene.role,
        gene.formation_date_target || null
      ]);
      entityCount++;
    }
    console.log(`✅ Imported ${entityCount} legal entities`);

    // Import AI Council
    console.log('\n📥 Importing AI Council members...');
    let councilCount = 0;
    for (const gene of genomeData.chromosomes.AI_GOVERNANCE.genes) {
      await client.query(`
        INSERT INTO ai_council (council_id, name, role, aol_tier, status, specialization)
        VALUES ($1, $2, $3, $4, $5, $6)
        ON CONFLICT (council_id) DO UPDATE
        SET name = EXCLUDED.name,
            role = EXCLUDED.role,
            aol_tier = EXCLUDED.aol_tier,
            status = EXCLUDED.status,
            specialization = EXCLUDED.specialization
      `, [
        gene.id,
        gene.name,
        gene.role,
        gene.aol_tier,
        gene.status,
        gene.specialization
      ]);
      councilCount++;
    }
    console.log(`✅ Imported ${councilCount} AI Council members`);

    // Import cluster nodes
    console.log('\n📥 Importing cluster nodes...');
    let nodeCount = 0;
    for (const gene of genomeData.chromosomes.INFRASTRUCTURE.genes) {
      await client.query(`
        INSERT INTO cluster_nodes (node_id, name, type, ram, status, role, endpoint, region)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        ON CONFLICT (node_id) DO UPDATE
        SET name = EXCLUDED.name,
            type = EXCLUDED.type,
            ram = EXCLUDED.ram,
            status = EXCLUDED.status,
            role = EXCLUDED.role,
            endpoint = EXCLUDED.endpoint,
            region = EXCLUDED.region
      `, [
        gene.id,
        gene.name,
        gene.type,
        gene.ram || null,
        gene.status,
        gene.role,
        gene.endpoint || null,
        gene.region || null
      ]);
      nodeCount++;
    }
    console.log(`✅ Imported ${nodeCount} cluster nodes`);

    // Import key inventions
    console.log('\n📥 Importing key inventions...');
    let inventionCount = 0;
    if (genomeData.inventions && genomeData.inventions.key_inventions) {
      for (const inv of genomeData.inventions.key_inventions) {
        await client.query(`
          INSERT INTO inventions (invention_id, title, classification, status, description)
          VALUES ($1, $2, $3, $4, $5)
          ON CONFLICT (invention_id) DO UPDATE
          SET title = EXCLUDED.title,
              classification = EXCLUDED.classification,
              status = EXCLUDED.status
        `, [
          `INV-${String(inv.number).padStart(3, '0')}`,
          inv.name,
          'NOVEL', // Default to NOVEL for key inventions
          inv.status,
          inv.name
        ]);
        inventionCount++;
      }
    }
    console.log(`✅ Imported ${inventionCount} inventions`);

    // Summary
    console.log('\n═══════════════════════════════════════════════════');
    console.log('📊 IMPORT SUMMARY');
    console.log('═══════════════════════════════════════════════════');
    console.log(`  Genome Version: ${genomeData.metadata.version}`);
    console.log(`  Legal Entities: ${entityCount}`);
    console.log(`  AI Council: ${councilCount}`);
    console.log(`  Cluster Nodes: ${nodeCount}`);
    console.log(`  Inventions: ${inventionCount}`);
    console.log('═══════════════════════════════════════════════════');
    console.log('✅ Import completed successfully');

  } catch (error) {
    console.error('❌ Import failed:', error);
    process.exit(1);
  } finally {
    await client.end();
  }
}

importGenome();
