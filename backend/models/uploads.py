from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Upload(BaseModel):
    id: Optional[int] = None
    filename: str
    path: str
    created_at: datetime = datetime.utcnow()


# Note: This is a lightweight Pydantic model used as a placeholder.
# For production, replace with SQLModel/SQLAlchemy models and proper migrations.
