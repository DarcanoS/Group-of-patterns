#!/usr/bin/env python3
"""
Verification script for historical ingestion
Checks the number of records inserted into the database
"""
import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'port': 5433,
    'database': 'air_quality_db',
    'user': 'air_quality_admin',
    'password': 'admin_secure_password'
}

def verify_ingestion():
    """Verify the results of historical ingestion"""
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("=" * 74)
        print("HISTORICAL INGESTION VERIFICATION")
        print("=" * 74)
        
        # Total readings
        cursor.execute("SELECT COUNT(*) FROM air_quality_reading")
        total_readings = cursor.fetchone()[0]
        print(f"\n📊 Total readings inserted: {total_readings:,}")
        
        # Readings per station
        cursor.execute("""
            SELECT s.name, COUNT(r.id) as reading_count
            FROM station s
            LEFT JOIN air_quality_reading r ON s.id = r.station_id
            GROUP BY s.name
            ORDER BY reading_count DESC
        """)
        print(f"\n📍 Readings per station:")
        for station, count in cursor.fetchall():
            print(f"  • {station}: {count:,} readings")
        
        # Readings per pollutant
        cursor.execute("""
            SELECT p.name, COUNT(r.id) as reading_count
            FROM pollutant p
            LEFT JOIN air_quality_reading r ON p.id = r.pollutant_id
            GROUP BY p.name
            ORDER BY reading_count DESC
        """)
        print(f"\n🧪 Readings per pollutant:")
        for pollutant, count in cursor.fetchall():
            print(f"  • {pollutant}: {count:,} readings")
        
        # Date range
        cursor.execute("""
            SELECT MIN(datetime), MAX(datetime)
            FROM air_quality_reading
        """)
        min_date, max_date = cursor.fetchone()
        print(f"\n📅 Date range:")
        print(f"  • From: {min_date}")
        print(f"  • To:   {max_date}")
        
        # Sample AQI values
        cursor.execute("""
            SELECT p.name, AVG(r.aqi)::int as avg_aqi, MAX(r.aqi) as max_aqi
            FROM air_quality_reading r
            JOIN pollutant p ON r.pollutant_id = p.id
            WHERE r.aqi IS NOT NULL
            GROUP BY p.name
            ORDER BY avg_aqi DESC
        """)
        print(f"\n🌡️  AQI Statistics:")
        for pollutant, avg_aqi, max_aqi in cursor.fetchall():
            print(f"  • {pollutant}: Avg AQI = {avg_aqi}, Max AQI = {max_aqi}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 74)
        print("✅ Verification completed!")
        print("=" * 74 + "\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    verify_ingestion()
