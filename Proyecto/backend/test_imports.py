#!/usr/bin/env python3
"""
Simple test script to verify the application can start.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing imports...")

    print("1. Importing config...")
    from app.core.config import settings
    print(f"   ✓ Config loaded: {settings.PROJECT_NAME}")

    print("2. Importing security...")
    from app.core.security import get_password_hash
    print("   ✓ Security module loaded")

    print("3. Importing database session...")
    from app.db.session import get_db
    print("   ✓ Database session module loaded")

    print("4. Importing FastAPI app...")
    from app.main import app
    print(f"   ✓ FastAPI app loaded: {app.title}")

    print("\n✅ All imports successful!")
    print(f"\nAPI Documentation will be available at: http://localhost:8000/docs")
    print(f"API Root: http://localhost:8000{settings.API_V1_STR}")

except Exception as e:
    print(f"\n❌ Error during import: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

