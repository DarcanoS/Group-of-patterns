#!/usr/bin/env python3
"""
Quick test for AQICN real-time ingestion
Tests the complete flow: API → Normalization → Database
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.config import settings
from app.db.session import get_db, test_connection
from app.services.ingestion_service import IngestionService
from app.logging_config import setup_logging

# Setup logging
logger = setup_logging(level="INFO")


def test_aqicn_ingestion():
    """Test AQICN ingestion end-to-end"""
    
    print("=" * 74)
    print("AQICN REAL-TIME INGESTION - QUICK TEST")
    print("=" * 74)
    
    # Check configuration
    print(f"\n📋 Configuration:")
    print(f"   API Key: {settings.aqicn_api_key[:20] if settings.aqicn_api_key else 'NOT SET'}...")
    print(f"   Base URL: {settings.aqicn_base_url}")
    print(f"   Cities: {settings.aqicn_cities}")
    
    if not settings.aqicn_api_key:
        print("\n❌ ERROR: AQICN_API_KEY not configured!")
        print("   Set TOKEN_API_AQICN in .env file")
        return False
    
    # Test database connection
    print(f"\n🔌 Testing database connection...")
    if not test_connection():
        print("❌ Database connection failed!")
        return False
    
    print("✅ Database connection OK")
    
    # Run ingestion
    print(f"\n🚀 Running AQICN ingestion...")
    
    db = next(get_db())
    
    try:
        service = IngestionService(db)
        service.preload_caches()
        
        stats = service.run_aqicn_ingestion()
        
        print("\n" + "=" * 74)
        print("✅ SUCCESS!")
        print("=" * 74)
        print(f"   Total fetched: {stats['total_fetched']}")
        print(f"   Inserted:      {stats['inserted']}")
        print(f"   Skipped:       {stats['skipped']}")
        print("=" * 74)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        db.close()


if __name__ == '__main__':
    success = test_aqicn_ingestion()
    sys.exit(0 if success else 1)
