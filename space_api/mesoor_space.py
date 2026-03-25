from datetime import timedelta

import jmespath

from space_api.model.channel import CreateChannel
from space_api.model.flow import FlowFromSpace2Task, FlowFromSpace2Project
from space_api.model.project import CreateProject, GetProjectCircuit
from space_api.model.search_task_id_by_projectid_taskpayload_id import SearchTaskIdByProjectIdTaskPayloadId
from space_api.model.get_tasks_info import GetTasksInfo
from space_api.model.get_task_info import GetTaskInfo
from space_api.model.space import CreateSpace
from loguru import logger
from aiohttp_client_cache import CachedSession
from space_api.model.task import CreateTask
from space_api.exceptions import MesoorSpaceException, StageBackwardNotAllowedException
import aiohttp
import hashlib
from aiohttp_client_cache.backends.sqlite import SQLiteBackend

from space_api.model.update_task_stage import UpDateTaskStage


class MesoorSpaceApp:
    def __init__(self, host:str):
        self.host = host
        backend = SQLiteBackend(
            cache_name="mesoor-space-api-cache",
            expire_after=timedelta(minutes=1)
        )
        self.session = CachedSession(cache=backend)
        self.backend = backend

    async def get_session(self):
        if self.session is None:
            backend = SQLiteBackend(
                cache_name="mesoor-space-api-cache",
                expire_after=timedelta(minutes=1)
            )
            self.session = CachedSession(cache=backend)
            self.backend = backend
        await self.backend.delete_expired_responses()
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

    async def search_task_by_task_payload_id(self,data: dict):
        data = SearchTaskIdByProjectIdTaskPayloadId(**data)
        url = f"{self.host}/v2/memory-searches"
        body = {
            "entityType": "HydrogenTask",
            "filters": [
                {
                    "op": "Is",
                    "key": "data.standardFields.taskPayload.openId",
                    "values": [
                        data.taskPayloadOpenId
                    ]
                }
                ,{
                    "op": "Is",
                    "key": "data.standardFields.project.openId",
                    "values": [
                        data.projectId
                    ]
                }
            ],
            "pageSize": 1,
            "sort": "meta.updatedAt:desc",
            "pointer": "/",
            "select": [
                "meta.openId"
            ]
        }
        headers = {
            "tenant-Id": data.tenantId,
            "user-Id": data.userId
        }
        session = await self.get_session()
        res = await session.post(url, json=body, headers=headers)
        assert res.status in [200]
        res = await res.json()
        if res["total"] > 1:
            raise MesoorSpaceException("此查询不具有唯一性")
        task_id = res["data"][0]["meta"]["openId"]
        return task_id


    async def get_project_circuit(self, data: dict):
        data = GetProjectCircuit(**data)
        headers = {
            "tenant-Id": data.tenantId,
            "user-Id": data.userId
        }
        url = f"{self.host}/v3/projects/{data.projectId}/circuits"
        body = {
            "projectId": data.projectId,
        }
        session = await self.get_session()
        res = await session.get(url, json=body, headers=headers)
        assert res.status in [200]
        res = await res.json()
        return res["data"]


    async def update_task_stage(self, _data: dict):
        data = UpDateTaskStage(**_data)
        # 如果开启流程阶段不允许回退
        if not data.allowStageBackward:
            # 获取当前 task_id
            task_id = await self.search_task_by_task_payload_id(_data)

            # 获取当前 task 详情（用于拿当前 stageId）
            task_detail_url = f"{self.host}/v3/tasks/{task_id}"
            session = await self.get_session()
            task_res = await session.get(task_detail_url, headers={
                "tenant-Id": data.tenantId,
                "user-Id": data.userId
            })
            assert task_res.status in [200]
            task_json = await task_res.json()
            current_stage_id = jmespath.search("data.current.stageId", task_json)
            assert current_stage_id is not None
            # 目标 stageId
            target_stage_id = data.stageId

            # 如果是通过 stageName 更新，需要从 circuit 解析 stageId
            circuit = await self.get_project_circuit(_data)
            if not target_stage_id and data.stageName:
                for stage in circuit.get("stages", []):
                    if stage.get("name") == data.stageName:
                        target_stage_id = stage["id"]
                        break
            assert target_stage_id is not None
            if current_stage_id and target_stage_id:
                if self._is_backward_transition(
                    circuit=circuit,
                    current_stage_id=current_stage_id,
                    target_stage_id=target_stage_id,
                ):
                    raise StageBackwardNotAllowedException(
                        f"Backward transition from {current_stage_id} to {target_stage_id} is not allowed."
                    )
        assert bool(data.stageId) != bool(data.stageName)
        headers = {
            "tenant-Id": data.tenantId,
            "user-Id": data.userId
        }
        task_id = await self.search_task_by_task_payload_id(_data)
        body = {
            "id": task_id,
        }
        if data.stageId:
            body["stageId"] = data.stageId
        elif data.stageName:
            body["stageName"] = data.stageName
        else:
            raise MesoorSpaceException(f"stageId or stageName not found->{body}")
        body = [body]
        url = f"{self.host}/v3/tasks/stages"
        session = await self.get_session()
        res = await session.put(url, json=body, headers=headers)

        if res.status in [200, 409]:
            logger.info(f"stage {'create' if res.status == 200 else 'exist'} "
                        f"success stage->{data.stageId} {data.stageName} taskId->{task_id}->{res.status}")
            return await res.json() if res.content_type == 'application/json' else await res.text()
        else:
            response_text = await res.text()
            logger.error(f"update stage失败: {response_text}")
            raise MesoorSpaceException(
                message=f"update stage失败: {response_text}",
                status_code=res.status,
                response_data={"error": response_text}
            )

    def _is_backward_transition(
        self,
        circuit: dict,
        current_stage_id: str,
        target_stage_id: str,
    ) -> bool:
        """
        判断是否为回退流转：
        通过比较阶段的 rank 值来判断，如果目标阶段的 rank 小于当前阶段的 rank，则为回退。
        """
        stages = circuit.get("stages", [])
        
        # 构建 stage_id -> rank 的映射
        stage_rank_map = {}
        for stage in stages:
            stage_id = stage.get("openId") or stage.get("id")
            rank = stage.get("rank")
            if stage_id and rank is not None:
                stage_rank_map[stage_id] = rank
        
        # 获取当前阶段和目标阶段的 rank
        current_rank = stage_rank_map.get(current_stage_id)
        target_rank = stage_rank_map.get(target_stage_id)
        
        # 如果任一阶段的 rank 不存在，无法判断，默认不是回退
        if current_rank is None or target_rank is None:
            return False
        
        # 目标 rank < 当前 rank，则为回退
        return target_rank < current_rank

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

    async def get_tasks_info(self, data: dict):
        try:
            data = GetTasksInfo(**data)
            headers = {
                "tenant-Id": data.tenantId,
                "user-Id": data.userId
            }
            task_ids_param = ",".join(data.taskIds)
            url = f"{self.host}/v3/tasks?taskIds={task_ids_param}"
            session = await self.get_session()
            res = await session.get(url, headers=headers)
            
            if res.status in [200]:
                logger.info(f"get tasks info success, taskIds->{task_ids_param}")
                return await res.json() if res.content_type == 'application/json' else await res.text()
            else:
                response_text = await res.text()
                logger.error(f"获取任务信息失败: {response_text}")
                raise MesoorSpaceException(
                    message=f"获取任务信息失败: {response_text}",
                    status_code=res.status,
                    response_data={"error": response_text}
                )
        except aiohttp.ClientError as e:
            logger.error(f"网络请求失败: {str(e)}")
            raise MesoorSpaceException(f"网络请求失败: {str(e)}")
        except Exception as e:
            logger.error(f"获取任务信息时发生未知错误: {str(e)}")
            raise MesoorSpaceException(f"获取任务信息时发生未知错误: {str(e)}")

    async def get_task_info(self, data: dict):
        data = GetTaskInfo(**data)
        res = await self.get_tasks_info({
            "tenantId": data.tenantId,
            "userId": data.userId,
            "taskIds": [data.taskId]
        })
        return res["data"][0]
