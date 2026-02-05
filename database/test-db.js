#!/usr/bin/env node
/**
 * Neon Database Connection Test Script
 * 
 * Tests connectivity to the Neon PostgreSQL instance
 * 
 * Usage: node test-db.js
 * Requires: DATABASE_URL environment variable
 */

import pkg from 'pg';
const { Client } = pkg;
import * as dotenv from 'dotenv';

dotenv.config();

async function testConnection() {
  const client = new Client({
    connectionString: process.env.DATABASE_URL,
    ssl: { rejectUnauthorized: false }
  });

  try {
    console.log('🔗 Testing Neon database connection...');
    console.log(`📍 Target: ${process.env.DATABASE_URL?.split('@')[1]?.split('/')[0] || 'unknown'}`);
    
    await client.connect();
    console.log('✅ Connection successful!\n');

    // Test query
    const result = await client.query('SELECT version(), current_database(), current_user;');
    
    console.log('📊 Database Information:');
    console.log(`  Version: ${result.rows[0].version.split(' ').slice(0, 2).join(' ')}`);
    console.log(`  Database: ${result.rows[0].current_database}`);
    console.log(`  User: ${result.rows[0].current_user}`);

    // Check tables
    const tables = await client.query(`
      SELECT COUNT(*) as count
      FROM information_schema.tables 
      WHERE table_schema = 'public';
    `);

    console.log(`\n📈 Tables in database: ${tables.rows[0].count}`);

    // Check if schema is deployed
    if (tables.rows[0].count >= 17) {
      console.log('✅ Schema appears to be deployed');
      
      // Sample a few key tables
      const inventions = await client.query('SELECT COUNT(*) as count FROM inventions;');
      const entities = await client.query('SELECT COUNT(*) as count FROM legal_entities;');
      const council = await client.query('SELECT COUNT(*) as count FROM ai_council;');
      
      console.log('\n📊 Record counts:');
      console.log(`  Inventions: ${inventions.rows[0].count}`);
      console.log(`  Legal Entities: ${entities.rows[0].count}`);
      console.log(`  AI Council: ${council.rows[0].count}`);
    } else {
      console.log('⚠️  Schema not fully deployed. Run deploy-schema.js');
    }

  } catch (error) {
    console.error('❌ Connection failed:', error.message);
    process.exit(1);
  } finally {
    await client.end();
  }
}

testConnection();
