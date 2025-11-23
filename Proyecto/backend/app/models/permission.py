"""
Permission ORM model.
Represents system permissions that can be granted to roles.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from app.db.base import Base


class Permission(Base):
    """
    Permission model - represents granular permissions.

    Attributes:
        id: Primary key
        name: Permission name (must be unique)
    """

    __tablename__ = "permission"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<Permission(id={self.id}, name='{self.name}')>"


# Many-to-many relationship table between Role and Permission
role_permission = Table(
    'role_permission',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('role.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permission.id'), primary_key=True)
)

