"""
AppUser ORM model.
Represents application users (citizens, researchers, admins).
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class AppUser(Base):
    """
    AppUser model - represents users of the application.

    Attributes:
        id: Primary key
        name: User's full name
        email: User's email (should be unique)
        password_hash: Hashed password
        location: User's location (city or area)
        role_id: Foreign key to Role

    Relationships:
        role: The role assigned to this user
        alerts: Alerts configured by this user
        recommendations: Recommendations generated for this user
        reports: Reports created by this user
    """

    __tablename__ = "app_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    location = Column(String(255), nullable=True)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)

    # Relationships
    role = relationship("Role", back_populates="users")
    alerts = relationship("Alert", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<AppUser(id={self.id}, name='{self.name}', email='{self.email}')>"

