from typing import Optional

from pydantic import BaseModel, Field


class SearchTaskIdByProjectIdTaskPayloadId(BaseModel):
    projectId: str
    taskPayloadOpenId: str
    tenantId: str
    userId: Optional[str] = Field(default="mesoor-admin")

