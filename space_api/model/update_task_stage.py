from typing import Optional

from pydantic import BaseModel, Field


class UpDateTaskStage(BaseModel):
    stageName: Optional[str] = Field(None)
    stageId: Optional[str] = Field(None)
    taskPayloadOpenId: str
    tenantId: str
    userId: Optional[str] = Field(default="mesoor-admin")

