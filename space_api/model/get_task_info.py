from pydantic import BaseModel, Field
from typing import Optional


class GetTaskInfo(BaseModel):
    tenantId: str
    userId: Optional[str] = Field(default="mesoor-admin")
    taskId: str
