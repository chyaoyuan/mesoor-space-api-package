from typing import Optional

from pydantic import BaseModel, Field


class CreateTask(BaseModel):
    projectId: str
    taskPayloadOpenId: str
    tenantId: str
    userId: Optional[str] = Field(default="mesoor-admin")
    extraBody: Optional[dict] = Field(default={})
