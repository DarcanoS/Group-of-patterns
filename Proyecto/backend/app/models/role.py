"""
Role ORM model.
Represents user roles (Citizen, Researcher, Admin).
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class Role(Base):
    """
    Role model - represents user roles in the system.

    Attributes:
        id: Primary key
        name: Role name (must be unique)

    Relationships:
        users: Users with this role
        permissions: Permissions granted to this role (via RolePermission)
    """

    __tablename__ = "role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)

    # Relationships
    users = relationship("AppUser", back_populates="role")

    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"

