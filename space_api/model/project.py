from typing import Optional

from pydantic import BaseModel, Field


class CreateProject(BaseModel):
    channelId: str
    projectId: str
    tenantId: str
    userId: Optional[str] = Field(default="mesoor-admin")
    projectName: str
    extraBody: Optional[dict] = Field(default={})

