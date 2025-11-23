"""
SQLAlchemy declarative base.
All ORM models should inherit from Base.
"""

from sqlalchemy.orm import declarative_base

# Create the declarative base
Base = declarative_base()

# Note: Models will be imported by app.models.__init__.py
# This avoids circular import issues

