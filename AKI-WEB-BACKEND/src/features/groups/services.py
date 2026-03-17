from typing import Sequence
from uuid import UUID

from faker import Faker

from .repositories import GroupRepository
from .schemas import Group


class GroupService:
    def __init__(self, group_repository: GroupRepository):
        self.group_repository = group_repository
        self.fake = Faker()

    async def get_all_groups(self) -> Sequence[Group]:
        result = []
        for _ in range(self.fake.random_int(min=1, max=5)):
            result.append(
                Group(id=self.fake.uuid4(cast_to=None),
                      title=self.fake.company()))
        return result

    async def get_group_by_id(self, group_id: str):
        return Group(id=UUID(group_id),
                    title=self.fake.company())
