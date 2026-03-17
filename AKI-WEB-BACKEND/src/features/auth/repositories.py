from sqlalchemy import select, text, CursorResult
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with a database session.

        Args:
            session (AsyncSession): The SQLAlchemy session to interact with the database.
        """
        self._session = session

    async def get_user(self, username: str) -> User | None:
        stmt = select(User).filter(User.loginId == username).order_by(User.xd_creation)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).filter(User.email == email).order_by(User.xd_creation)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def create_user(self, login_id: str, email: str, name: str, last_name: str, user_type: str,
                          hashed_password: str, status: str = 'A', creation_user: str | None = None):
        if creation_user is None:
            creation_user = login_id

        query = text('''EXECUTE [dbo].[sp_createUser] 
                        @loginId = :login_id,
                        @email = :email,
                        @name = :name,
                        @lastName = :last_name,
                        @userType = :user_type,
                        @hashedPassword = :hashed_password,
                        @status = :status,
                        @creationUser = :creation_user
                    ''')
        params = {
            'login_id': login_id,
            'email': email,
            'name': name,
            'last_name': last_name,
            'user_type': user_type,
            'hashed_password': hashed_password,
            'status': status,
            'creation_user': creation_user
        }
        #
        # try:
        #     results = await self._session.execute(query, params)
        #
        #     await self._session.commit()
        #
        #     if isinstance(results, CursorResult) and results.returns_rows:
        #         rows = results.fetchall()
        #         keys = results.keys()
        #
        #         return [dict(zip(keys, row)) for row in rows]
        #     return None
        # except SQLAlchemyError as e:
        #     await self._session.rollback()
        #     return None

        async with self._session as session:
            try:
                results = await session.execute(query, params)
                await session.commit()

                if isinstance(results, CursorResult) and results.returns_rows:
                    rows = results.fetchall()
                    keys = results.keys()

                    return [dict(zip(keys, row)) for row in rows]
                return None
            except SQLAlchemyError as e:
                await self._session.rollback()
                return None
