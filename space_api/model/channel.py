from typing import Optional

from pydantic import BaseModel, Field


class CreateChannel(BaseModel):
    channelId: str
    tenantId: str
    userId: Optional[str] = Field(default="mesoor-admin")
    spaceId: str
    channelName: str
    extraBody: Optional[dict] = Field(default={})
