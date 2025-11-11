from datetime import timedelta

from space_api.model.channel import CreateChannel
from space_api.model.flow import FlowFromSpace2Task, FlowFromSpace2Project
from space_api.model.project import CreateProject
from space_api.model.space import CreateSpace
from loguru import logger
from aiohttp_client_cache import CachedSession
from space_api.model.task import CreateTask
from space_api.exceptions import MesoorSpaceException
import aiohttp
import hashlib
from aiohttp_client_cache.backends.filesystem import FileBackend


class MesoorSpaceApp:
    def __init__(self, host:str):
        self.host = host
        self.session = CachedSession(cache=FileBackend(cache_name="space-cache",expire_after=timedelta(minutes=1)))

    async def get_session(self):
        if self.session is None:
            self.session = CachedSession(cache=FileBackend(cache_name="space-cache"),expire_after=timedelta(minutes=1))
        return self.session

    async def create_spaces(self, data: dict):
        try:
            data = CreateSpace(**data)
            headers = {
                "tenant-Id": data.tenantId,
                "user-Id": data.userId,
            }
            body = {
                **data.extraBody,
                "name": data.spaceName
            }
            url = f"{self.host}/v2/spaces?spaceId={data.spaceId}"
            logger.info(url)
            session = await self.get_session()
            logger.info(body)
            res = await session.post(url, json=body, headers=headers)
            
            if res.status in [200, 409]:
                logger.info(f"spaces {'Create' if res.status == 200 else 'exist'} success")
                return await res.json() if res.content_type == 'application/json' else await res.text()
            else:
                response_text = await res.text()
                logger.error(f"创建空间失败: {response_text}")
                raise MesoorSpaceException(
                    message=f"创建空间失败: {response_text}",
                    status_code=res.status,
                    response_data={"error": response_text}
                )
        except aiohttp.ClientError as e:
            logger.error(f"网络请求失败: {str(e)}")
            raise MesoorSpaceException(f"网络请求失败: {str(e)}")
        except Exception as e:
            logger.error(f"创建空间时发生未知错误: {str(e)}")
            raise MesoorSpaceException(f"创建空间时发生未知错误: {str(e)}")

    async def create_channel(self, data: dict):
        try:
            data = CreateChannel(**data)
            headers = {
                "tenant-Id": data.tenantId,
                "user-Id": data.userId
            }
            body = {
                **data.extraBody,
                "name": data.channelName,
                "spaceId": data.spaceId
            }
            url = f"{self.host}/v3/channels?channelId={data.channelId}"
            session = await self.get_session()
            res = await session.post(url, json=body, headers=headers)
            
            if res.status in [200, 409]:
                logger.info(f"channel {'Create' if res.status == 200 else 'exist'} success")
                return await res.json() if res.content_type == 'application/json' else await res.text()
            else:
                response_text = await res.text()
                logger.error(f"创建频道失败: {response_text}")
                raise MesoorSpaceException(
                    message=f"创建频道失败: {response_text}",
                    status_code=res.status,
                    response_data={"error": response_text}
                )
        except aiohttp.ClientError as e:
            logger.error(f"网络请求失败: {str(e)}")
            raise MesoorSpaceException(f"网络请求失败: {str(e)}")
        except Exception as e:
            logger.error(f"创建频道时发生未知错误: {str(e)}")
            raise MesoorSpaceException(f"创建频道时发生未知错误: {str(e)}")

    async def create_project(self, data: dict):
        try:
            data = CreateProject(**data)
            headers = {
                "tenant-Id": data.tenantId,
                "user-Id": data.userId
            }
            url = f"{self.host}/v3/projects?projectId={data.projectId}"
            body = {
                **data.extraBody,
                "name": data.projectName,
                "channelId": data.channelId
            }
            session = await self.get_session()
            res = await session.post(url, json=body, headers=headers)
            
            if res.status in [200, 409]:
                logger.info(f"Project {'Create' if res.status == 200 else 'exist'} success")
                return await res.json() if res.content_type == 'application/json' else await res.text()
            else:
                response_text = await res.text()
                logger.error(f"创建项目失败: {response_text}")
                raise MesoorSpaceException(
                    message=f"创建项目失败: {response_text}",
                    status_code=res.status,
                    response_data={"error": response_text}
                )
        except aiohttp.ClientError as e:
            logger.error(f"网络请求失败: {str(e)}")
            raise MesoorSpaceException(f"网络请求失败: {str(e)}")
        except Exception as e:
            logger.error(f"创建项目时发生未知错误: {str(e)}")
            raise MesoorSpaceException(f"创建项目时发生未知错误: {str(e)}")

    async def create_task(self, data: dict):
        try:
            data = CreateTask(**data)
            headers = {
                "tenant-Id": data.tenantId,
                "user-Id": data.userId
            }
            url = f"{self.host}/v3/tasks"
            body = {
                **data.extraBody,
                "taskPayloadOpenId": data.taskPayloadOpenId,
                "projectId": data.projectId,
            }
            session = await self.get_session()
            res = await session.post(url, json=body, headers=headers)
            
            if res.status in [200, 409]:
                logger.info(f"task {'create' if res.status == 200 else 'exist'} "
                            f"success projectId->{data.projectId} taskId->{data.taskPayloadOpenId}->{res.status}")
                return await res.json() if res.content_type == 'application/json' else await res.text()
            else:
                response_text = await res.text()
                logger.error(f"创建任务失败: {response_text}")
                raise MesoorSpaceException(
                    message=f"创建任务失败: {response_text}",
                    status_code=res.status,
                    response_data={"error": response_text}
                )
        except aiohttp.ClientError as e:
            logger.error(f"网络请求失败: {str(e)}")
            raise MesoorSpaceException(f"网络请求失败: {str(e)}")
        except Exception as e:
            logger.error(f"创建任务时发生未知错误: {str(e)}")
            raise MesoorSpaceException(f"创建任务时发生未知错误: {str(e)}")

    @staticmethod
    def to_md5(content: str):
        return hashlib.md5(content.encode('utf-8')).hexdigest()


    async def flow_from_space_to_project(self, data: dict):
        data = FlowFromSpace2Project(**data)
        _data = data.dict()
        if data.spaceIdByMd5Name:
            space_id = self.to_md5(data.spaceName)
            _data["spaceId"] = space_id
        if data.channelIdByMd5Name:
            channel_id = self.to_md5(data.channelName)
            _data["channelId"] = channel_id
        if data.projectIdByMd5Name:
            content = f"{data.projectIdByMd5NamePrefixSalt}-{data.projectName}"
            project_id = self.to_md5(content)
            _data["projectId"] = project_id
        await self.create_spaces(_data)
        await self.create_channel({**_data,"extraBody":data.channelData})
        await self.create_project({**_data,"extraBody":data.projectData})



    async def flow_from_space_to_task(self, data: dict):
        data = FlowFromSpace2Task(**data)
        _data = data.dict()
        if data.spaceIdByMd5Name:
            space_id = self.to_md5(data.spaceName)
            _data["spaceId"] = space_id
        if data.channelIdByMd5Name:
            channel_id = self.to_md5(data.channelName)
            _data["channelId"] = channel_id
        if data.projectIdByMd5Name:
            content = f"{data.projectIdByMd5NamePrefixSalt}-{data.projectName}"
            project_id = self.to_md5(content)
            _data["projectId"] = project_id
        await self.create_spaces(_data)
        await self.create_channel({**_data,"extraBody":data.channelData})
        await self.create_project({**_data,"extraBody":data.projectData})
        await self.create_task(_data)