from fastapi import Depends

from src.features.groups.repositories import GroupRepository
from src.features.groups.services import GroupService
from ...core import AsyncSessionDep


async def get_group_repository(session: AsyncSessionDep):
    yield GroupRepository(session)


async def get_group_service(repository: GroupRepository = Depends(get_group_repository)):
    yield GroupService(repository)
