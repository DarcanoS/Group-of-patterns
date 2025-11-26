"""
Makes the app directory executable as a module.

Usage:
    python -m app.main --mode historical
"""

from app.main import main

if __name__ == "__main__":
    main()
