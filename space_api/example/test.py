import asyncio
import json

import aiohttp
from loguru import logger


Channel_Default_Config = {
        "memberIds": [],
        "visible": False,
        "style": {
            "icon": "icon-temphuiyi",
            "color": "#6f59f7"
        },
        "templateId": "56b26d46-9d5c-4b57-ad1a-e07431cf2947",
        "dumpId": 19,
        "circuitTemplate": {
            "rules": [],
            "stages": [
                {
                    "id": "fbc61ee3-877c-4bf9-b342-4bd48632dec7",
                    "name": "待开始",
                    "rank": 0,
                    "type": "Edit",
                    "extend": {
                        "color": "#C8C8C8",
                        "category": "active"
                    },
                    "parent": None,
                    "deleted": False,
                    "carryFieldsSchema": {
                        "type": [
                            "object",
                            "null"
                        ],
                        "order": 0,
                        "title": "StageFields",
                        "$schema": "https://json-schema.org/draft/2020-12/schema",
                        "nullable": True,
                        "properties": {},
                        "description": "StageFields"
                    }
                },
                {
                    "id": "b24ca7ec-aafb-4131-b88c-a80917a865c7",
                    "name": "进行中",
                    "rank": 1,
                    "type": "Edit",
                    "extend": {
                        "color": "#6F59F7",
                        "category": "active"
                    },
                    "parent": None,
                    "deleted": False,
                    "carryFieldsSchema": {
                        "type": [
                            "object",
                            "null"
                        ],
                        "order": 0,
                        "title": "StageFields",
                        "$schema": "https://json-schema.org/draft/2020-12/schema",
                        "nullable": True,
                        "properties": {},
                        "description": "StageFields"
                    }
                },
                {
                    "id": "dfc19f02-577b-4f48-ad53-b752413de2fd",
                    "name": "已完成",
                    "rank": 2,
                    "type": "Edit",
                    "extend": {
                        "color": "#4FCDA0",
                        "category": "success"
                    },
                    "parent": None,
                    "deleted": False,
                    "carryFieldsSchema": {
                        "type": [
                            "object",
                            "null"
                        ],
                        "order": 0,
                        "title": "StageFields",
                        "$schema": "https://json-schema.org/draft/2020-12/schema",
                        "nullable": True,
                        "properties": {},
                        "description": "StageFields"
                    }
                },
                {
                    "id": "0b932d2c-9c7b-4983-9997-7b95308a54ce",
                    "name": "已关闭",
                    "rank": 3,
                    "type": "End&Edit",
                    "extend": {
                        "color": "#459BEA",
                        "category": "fail"
                    },
                    "parent": None,
                    "deleted": False,
                    "carryFieldsSchema": {
                        "type": [
                            "object",
                            "null"
                        ],
                        "order": 0,
                        "title": "StageFields",
                        "$schema": "https://json-schema.org/draft/2020-12/schema",
                        "nullable": True,
                        "properties": {},
                        "description": "StageFields"
                    }
                }
            ]
        },
        "taskPayloadType": {
            "name": "简历",
            "entityType": "Resume"
        },
        "projectPayloadType": {
            "name": "职位",
            "entityType": "Job"
        }
    }


from space_api import MesoorSpaceApp


async def run():
    mesoor_space = MesoorSpaceApp("http://localhost:60879")
    index = "0"
    tenantId = "exyc"
    job_name = "包装操作员"
    project_id = f"mesoorExtension-rd6.zhaopin.com-CC883810730J40838296602-{index}"
    job_id = "mesoorExtension-rd6.zhaopin.com-CC883810730J40838296602"
    project_data = {"projectPayloadEntityType": "Job", "projectPayloadOpenId": job_id}
    data = {
        "spaceName": f"插件收录-{index}",
        "spaceIdByMd5Name": True,
        "channelName": f"智联招聘-{index}",
        "channelData": Channel_Default_Config,
        "channelIdByMd5Name": True,
        "projectName": job_name,
        "projectId": project_id,
        "tenantId":tenantId,
        "projectData": project_data,
        "taskPayloadOpenId":"mesoorExtension-rd6.zhaopin.com-zaAQ57(q9BxYt7eYTMRMXeXl9cPh6nZN"
    }

    await mesoor_space.flow_from_space_to_task(data)
if __name__ == '__main__':
    asyncio.run(run())