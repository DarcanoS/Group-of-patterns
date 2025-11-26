#!/usr/bin/env python3
"""
Seed data loader for Air Quality Platform
Executes seed_data.sql using psycopg2
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'ingestion'))

import psycopg2
from psycopg2 import sql

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5433,
    'database': 'air_quality_db',
    'user': 'air_quality_admin',
    'password': 'admin_secure_password'
}

def run_seed_script():
    """Execute the seed_data.sql script"""
    
    # Read the SQL script
    sql_file = Path(__file__).parent / 'seed_data.sql'
    
    if not sql_file.exists():
        print(f"❌ Error: {sql_file} not found!")
        return False
    
    print("=" * 74)
    print("AIR QUALITY PLATFORM - SEED DATA LOADER")
    print("=" * 74)
    print(f"\n📄 Reading SQL script: {sql_file}")
    
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    # Remove psql-specific commands
    lines = []
    for line in sql_script.split('\n'):
        if not line.strip().startswith('\\echo'):
            lines.append(line)
    
    sql_script = '\n'.join(lines)
    
    try:
        print(f"🔌 Connecting to database: {DB_CONFIG['database']} @ {DB_CONFIG['host']}:{DB_CONFIG['port']}")
        
        # Connect to database
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("✅ Connected successfully")
        print("\n🚀 Executing seed script...\n")
        
        # Execute the script
        cursor.execute(sql_script)
        
        # Get counts
        cursor.execute("""
            SELECT 
                (SELECT COUNT(*) FROM pollutant) as pollutants,
                (SELECT COUNT(*) FROM role) as roles,
                (SELECT COUNT(*) FROM permission) as permissions,
                (SELECT COUNT(*) FROM role_permission) as role_permissions,
                (SELECT COUNT(*) FROM map_region) as regions,
                (SELECT COUNT(*) FROM station) as stations,
                (SELECT COUNT(*) FROM app_user) as users
        """)
        
        result = cursor.fetchone()
        
        print("=" * 74)
        print("SEED DATA SUMMARY")
        print("=" * 74)
        print(f"  Pollutants:        {result[0]}")
        print(f"  Roles:             {result[1]}")
        print(f"  Permissions:       {result[2]}")
        print(f"  Role-Permissions:  {result[3]}")
        print(f"  Regions:           {result[4]}")
        print(f"  Stations:          {result[5]}")
        print(f"  Users:             {result[6]}")
        print("=" * 74)
        print("\n✅ Seed data loaded successfully!\n")
        
        # Show pollutants
        cursor.execute("SELECT name, unit, description FROM pollutant ORDER BY name")
        pollutants = cursor.fetchall()
        
        print("📋 Pollutants in database:")
        for name, unit, desc in pollutants:
            print(f"  • {name} ({unit}): {desc[:60]}...")
        
        cursor.close()
        conn.close()
        
        return True
        
    except psycopg2.Error as e:
        print(f"\n❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == '__main__':
    success = run_seed_script()
    sys.exit(0 if success else 1)
