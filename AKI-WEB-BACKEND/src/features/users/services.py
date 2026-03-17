from pwdlib import PasswordHash

from ..auth.repositories import UserRepository
from ..auth.schemas import User
from ..users.schemas import UserCreate


class UserService:
    def __init__(self, user_repository: UserRepository | None = None):
        self.user_repository = user_repository
        self.password_hash = PasswordHash.recommended()

    def get_password_hash(self, password):
        return self.password_hash.hash(password)

    async def get_user(self, username: str) -> User | None:
        user = await self.user_repository.get_user(username=username)

        return User.model_validate(user)

    async def get_user_by_email(self, email: str) -> User | None:
        user = await self.user_repository.get_user_by_email(email)
        return User.model_validate(user)

    async def create_user(self, user: UserCreate):
        hashed_password = self.get_password_hash(user.password)
        await self.user_repository.create_user(login_id=user.username, email=user.email, name=user.name, last_name=user.last_name, user_type='ROOT', hashed_password=hashed_password)

        return await self.get_user(username=user.username)