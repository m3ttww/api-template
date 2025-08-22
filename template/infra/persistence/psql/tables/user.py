from uuid import uuid4

from sqlalchemy import Column, String, Table
from sqlalchemy.dialects.postgresql import UUID

from template.domain.entities.user import User

from .base import mapper_registry, metadata

user_table = Table(
    "user",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("login", String(255), nullable=False, unique=True),
    Column("password_hash", String(255), nullable=False),
)
mapper_registry.map_imperatively(User, user_table)
