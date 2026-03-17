from datetime import timedelta, datetime, UTC

import jwt
from fastapi import HTTPException, status
from pwdlib import PasswordHash
from pydantic import validate_email

from .repositories import UserRepository
from .schemas import UserWithPassword, Token, TokenData


class AuthService:
    def __init__(self, user_repository: UserRepository | None = None,
                 access_token_expire_minutes: int = 60,
                 secret_key: str = None,
                 algorithm: str = 'HS256'):
        self.user_repository = user_repository
        self.password_hash = PasswordHash.recommended()
        self.access_token_expire_minutes = access_token_expire_minutes
        self._secret_key = secret_key
        self.algorithm = algorithm

    async def authenticate(self, username: str, password: str):
        if self.check_is_email(username):
            user = await self.get_user_by_email(username)
        else:
            user = await self.get_user(username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    async def get_user(self, username: str):
        user = await self.user_repository.get_user(username)
        return UserWithPassword.model_validate(user)

    def verify_password(self, plain_password, hashed_password):
        return self.password_hash.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.password_hash.hash(password)

    @staticmethod
    def check_is_email(username):
        is_email = False
        try:
            validate_email(username)
            is_email = True
        finally:
            return is_email

    async def get_user_by_email(self, username):
        user = await self.user_repository.get_user_by_email(username)
        return UserWithPassword.model_validate(user)


    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        current_time = datetime.now(UTC)
        if expires_delta:
            expire = current_time + expires_delta
        else:
            expire = current_time + timedelta(minutes=15)
        to_encode.update({"iat": current_time, "exp": expire})
        encoded_jwt = jwt.encode(to_encode, self._secret_key, algorithm=self.algorithm)
        return encoded_jwt, expire

    def generate_token(self, user: UserWithPassword):
        access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
        access_token, expire = self.create_access_token(
            data={"sub": user.username, "name": user.display_name, "email": user.email},
            expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="Bearer", expires_in=expire.timestamp())

    def validate_token(self, token):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self.algorithm])
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
            return TokenData(username=username)
        except:
            raise credentials_exception
