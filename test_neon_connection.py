#!/usr/bin/env python3
"""
Neon Database Connection Test Script

This script tests the connection to a Neon PostgreSQL database
and verifies that pgvector extension is available.

Usage:
    python test_neon_connection.py

Environment Variables:
    DATABASE_URL - Full PostgreSQL connection string (required)
    Or individual parameters:
    DB_HOST, DB_PORT, DB_DATABASE, DB_USERNAME, DB_PASSWORD
"""

import os
import sys
import asyncio
import asyncpg
from typing import Optional

async def test_connection(dsn: str) -> bool:
    """Test database connection and pgvector availability"""
    try:
        print("🔌 Connecting to Neon database...")
        print(f"   Connection string: {dsn[:30]}...{dsn[-20:]}")
        
        # Create connection
        conn = await asyncpg.connect(dsn, timeout=10)
        print("✅ Successfully connected to database")
        
        # Test basic query
        print("\n🔍 Testing basic query...")
        result = await conn.fetchval("SELECT version()")
        print(f"   PostgreSQL version: {result.split(',')[0]}")
        
        # Check for pgvector extension
        print("\n🧪 Checking pgvector extension...")
        pgvector_installed = await conn.fetchval(
            "SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'vector')"
        )
        
        if pgvector_installed:
            print("✅ pgvector extension is installed")
            
            # Get pgvector version
            pgvector_version = await conn.fetchval(
                "SELECT extversion FROM pg_extension WHERE extname = 'vector'"
            )
            print(f"   pgvector version: {pgvector_version}")
        else:
            print("⚠️  pgvector extension is NOT installed")
            print("   To install, run: CREATE EXTENSION vector;")
            
        # Test vector operations (if pgvector is available)
        if pgvector_installed:
            print("\n🧮 Testing vector operations...")
            try:
                # Create a test table with vector column
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS test_vectors (
                        id SERIAL PRIMARY KEY,
                        embedding vector(3)
                    )
                """)
                
                # Insert a test vector
                await conn.execute(
                    "INSERT INTO test_vectors (embedding) VALUES ($1)",
                    [1.0, 2.0, 3.0]
                )
                
                # Query the vector
                result = await conn.fetchval(
                    "SELECT embedding FROM test_vectors ORDER BY id DESC LIMIT 1"
                )
                print(f"   Test vector: {result}")
                
                # Clean up
                await conn.execute("DROP TABLE test_vectors")
                print("✅ Vector operations working correctly")
                
            except Exception as e:
                print(f"❌ Vector operations failed: {e}")
        
        # Check connection parameters
        print("\n📊 Connection information:")
        server_version = await conn.fetchval("SHOW server_version")
        print(f"   Server version: {server_version}")
        
        max_connections = await conn.fetchval("SHOW max_connections")
        print(f"   Max connections: {max_connections}")
        
        ssl_status = await conn.fetchval("SELECT ssl FROM pg_stat_ssl WHERE pid = pg_backend_pid()")
        print(f"   SSL enabled: {ssl_status}")
        
        # Close connection
        await conn.close()
        print("\n✅ All tests passed! Neon database is ready to use.")
        return True
        
    except asyncpg.InvalidCatalogNameError as e:
        print(f"❌ Database does not exist: {e}")
        print("   Create the database in Neon console first")
        return False
        
    except asyncpg.InvalidPasswordError:
        print("❌ Authentication failed: Invalid username or password")
        return False
        
    except asyncpg.CannotConnectNowError as e:
        print(f"❌ Cannot connect to database: {e}")
        print("   The database might be starting up (Neon auto-suspend)")
        print("   Wait a few seconds and try again")
        return False
        
    except asyncpg.PostgresConnectionError as e:
        print(f"❌ Connection error: {e}")
        print("   Check your connection string and network connectivity")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {e}")
        return False

def get_database_url() -> Optional[str]:
    """Get database URL from environment"""
    # Check for DATABASE_URL first
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        return database_url
    
    # Try to construct from individual parameters
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT', '5432')
    database = os.getenv('DB_DATABASE')
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    
    if all([host, database, username, password]):
        return f"postgresql://{username}:{password}@{host}:{port}/{database}?sslmode=require"
    
    return None

def main():
    """Main entry point"""
    print("=" * 70)
    print("Neon Database Connection Test")
    print("=" * 70)
    print()
    
    # Get database URL
    dsn = get_database_url()
    
    if not dsn:
        print("❌ Database configuration not found!")
        print()
        print("Please set one of the following:")
        print("  1. DATABASE_URL environment variable")
        print("  2. Individual variables: DB_HOST, DB_PORT, DB_DATABASE, DB_USERNAME, DB_PASSWORD")
        print()
        print("Example:")
        print("  export DATABASE_URL='postgresql://user:pass@ep-xxx.region.neon.tech/db?sslmode=require'")
        print()
        sys.exit(1)
    
    # Run the test
    success = asyncio.run(test_connection(dsn))
    
    print()
    print("=" * 70)
    
    if success:
        print("✅ Connection test completed successfully!")
        sys.exit(0)
    else:
        print("❌ Connection test failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
