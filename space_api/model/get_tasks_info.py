from pydantic import BaseModel, Field
from typing import Optional, List


class GetTasksInfo(BaseModel):
    tenantId: str
    userId: Optional[str] = Field(default="mesoor-admin")
    taskIds: List[str]
