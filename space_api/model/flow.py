from typing import Optional

from pydantic import BaseModel, Field


class FlowFromSpace2Task(BaseModel):
    spaceName: str
    spaceIdByMd5Name: bool = Field(default=True)
    spaceId: Optional[str] = Field(default=None, )
    channelName:Optional[str] = Field(default=None, )
    channelIdByMd5Name:bool  = Field(default=True)
    channelId:Optional[str] = Field(default=None, )
    channelData: Optional[dict] = Field(default={}, )
    projectName: str
    projectIdByMd5Name: bool = Field(default=False)
    projectIdByMd5NamePrefixSalt: Optional[str] = Field(default="",description="为了避免名字一样导致的project重复")
    projectData: Optional[dict] = Field(default={}, )
    projectId: Optional[str] = Field(default=None, )
    taskPayloadOpenId: str
    tenantId: str
    userId: Optional[str] = Field(default="mesoor-admin")


class FlowFromSpace2Project(BaseModel):
    spaceName: str
    spaceIdByMd5Name: bool = Field(default=True)
    spaceId: Optional[str] = Field(default=None, )
    channelName:Optional[str] = Field(default=None, )
    channelIdByMd5Name:bool  = Field(default=True)
    channelId:Optional[str] = Field(default=None, )
    channelData: Optional[dict] = Field(default={}, )
    projectName: str
    projectIdByMd5Name: bool = Field(default=False)
    projectIdByMd5NamePrefixSalt: Optional[str] = Field(default="",description="为了避免名字一样导致的project重复")
    projectData: Optional[dict] = Field(default={}, )
    projectId: Optional[str] = Field(default=None, )
    tenantId: str
    userId: Optional[str] = Field(default="mesoor-admin")

if __name__ == '__main__':
    a = {
        "spaceName": "插件收录",
        "spaceIdByMd5Name": True,
        "channelName": "智联招聘",
        "channelIdByMd5Name": True,

        "projectName":"职位名称",
        "projectId": "前缀+招聘网站ID",
    }
