from typing import Optional

from pydantic import BaseModel, Field


class CreateSpace(BaseModel):
    tenantId: str
    userId: Optional[str] = Field(default="mesoor-admin")
    spaceId: str
    spaceName: str
    extraBody: Optional[dict] = Field(default={})

if __name__ == '__main__':
    import hashlib
    space_name = "插件收录"
    o = hashlib.md5()
    data = o.update(space_name.encode("utf-8"))
    data = o.hexdigest()

    b = {"tenantId":"exyc","spaceId": o.hexdigest(),"spaceName": space_name}
    data = CreateSpace(**b)
    print(data)