from datetime import datetime
from typing import List

from sqlalchemy import select, text, CursorResult
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.forms import models


class FormRepository:
    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with a database session.

        Args:
            session (AsyncSession): The SQLAlchemy session to interact with the database.
        """
        self._session = session

    async def list(self, form_id: str | None = None):
        """
        List all form periods, optionally filtered by form ID.

        Args:
            form_id (str, optional): The ID of the form to filter by.

        Returns:
            List of form periods.
        """
        filters = []

        if form_id:
            filters.append(models.FormPeriod.form_id == form_id)
        stmt = select(models.FormPeriod)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_forms_by_user_id(self, user_id: str, language_id: int | None = None) -> List[dict] | None:
        """
        Get forms summary by user ID.

        Args:
            user_id (str): The ID of the user.
            language_id (int, optional): The language ID.

        Returns:
            List of dictionaries containing the forms summary.
        """
        query = text('''EXECUTE [dbo].[sp_getUserFormsSummary] 
                        @userLogin = :user_id,
                        @languageId = :language_id
                    ''')
        params = {'user_id': user_id, 'language_id': language_id}
        async with self._session as session:
            results = await session.execute(query, params)

            if isinstance(results, CursorResult) and results.returns_rows:
                rows = results.fetchall()
                keys = results.keys()

                return [dict(zip(keys, row)) for row in rows]
            return None

    async def get(self, form_id: str | int | None = None, status: str | None = None):
        filters = []
        if form_id:
            filters.append(models.Form.id == form_id)
        if status:
            filters.append(models.Form.status == status)

        stmt = select(models.Form).filter(*filters).order_by(models.Form.xd_creation)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_form_data_by_id(self, form_id: int, period_id: int, user_id: str | None = None,
                                  language_id: int | None = None):
        """
        Get form data by form ID and period ID, optionally filtered by user ID and language ID.

        Args:
            form_id (int): The ID of the form.
            period_id (int): The ID of the period.
            user_id (str, optional): The ID of the user.
            language_id (int, optional): The language ID.

        Returns:
            List of dictionaries containing the form data, or None if no results found.
        """
        query = text('''EXECUTE [dbo].[sp_getFormData] 
                                @userLogin = :user_id,
                                @formId = :form_id,
                                @periodId = :period_id,
                                @languageId = :language_id
                            ''')
        params = {'user_id': user_id, 'form_id': form_id, 'period_id': period_id, 'language_id': language_id}
        async with self._session as session:
            results = await session.execute(query, params)

            if isinstance(results, CursorResult) and results.returns_rows:
                rows = results.fetchall()
                keys = results.keys()

                return [dict(zip(keys, row)) for row in rows]
            return None

    async def save_form_data(self,
                             form_id: int | None = None,
                             period_id: int | None = None,
                             period_point: datetime | None = None,
                             scenario_id: int | None = None,
                             location_id: int | None = None,
                             measure_id: int | None = None,
                             form_code: str | None = None,
                             period_code: str | None = None,
                             scenario_code: str | None = None,
                             location_code: str | None = None,
                             measure_code: str | None = None,
                             value_int: int | None = None,
                             value_dec: float | None = None,
                             value_float: float | None = None,
                             value_text: str | None = None,
                             value_boolean: bool | None = None,
                             value_datetime: datetime | None = None,
                             user_id: str | None = None,
                             ):
        query = text('''EXECUTE [dbo].[sp_setFormData] 
                                        @userLogin = :user_id,
                                        @formId = :form_id,
                                        @periodId = :period_id,
                                        @periodPoint = :period_point,
                                        @scenarioId = :scenario_id,
                                        @locationId = :location_id,
                                        @measureId = :measure_id,
                                        @formCode = :form_code,
                                        @periodCode = :period_code,
                                        @scenarioCode = :scenario_code,
                                        @locationCode = :location_code,
                                        @measureCode = :measure_code,
                                        @valueInt = :value_int,
                                        @valueDec = :value_dec,
                                        @valueFloat = :value_float,
                                        @valueText = :value_text,
                                        @valueBoolean = :value_boolean,
                                        @valueDateTime = :value_datetime
                                    ''')
        params = {
            'user_id': user_id,
            'form_id': form_id,
            'period_id': period_id,
            'period_point': period_point,
            'scenario_id': scenario_id,
            'location_id': location_id,
            'measure_id': measure_id,
            'form_code': form_code,
            'period_code': period_code,
            'scenario_code': scenario_code,
            'location_code': location_code,
            'measure_code': measure_code,
            'value_int': value_int,
            'value_dec': value_dec,
            'value_float': value_float,
            'value_text': value_text,
            'value_boolean': value_boolean,
            'value_datetime': value_datetime
        }

        try:
            results = await self._session.execute(query, params)

            await self._session.commit()

            if isinstance(results, CursorResult) and results.returns_rows:
                rows = results.fetchall()
                keys = results.keys()

                return [dict(zip(keys, row)) for row in rows]
            return None
        except SQLAlchemyError as e:
            await self._session.rollback()
            return None

    async def get_form_history_by_id(self, form_id: int):
        query = text('''EXECUTE [dbo].[sp_getFormHistory] @formId = :form_id''')
        params = {'form_id': form_id}
        async with self._session as session:
            results = await session.execute(query, params)

            if isinstance(results, CursorResult) and results.returns_rows:
                rows = results.fetchall()
                keys = results.keys()

                return [dict(zip(keys, row)) for row in rows]
            return None

    async def get_next_period_by_id(self, form_id: int):
        query = text('''EXECUTE [dbo].[sp_getNextFormPeriod] @formId = :form_id''')
        params = {'form_id': form_id}

        async with self._session as session:
            results = await session.execute(query, params)

            if isinstance(results, CursorResult) and results.returns_rows:
                row = results.fetchone()
                keys = results.keys()

                return dict(zip(keys, row)) if row else None
            return None

    async def add_period(self, form_id: int, user_id: str):
        query = text('''EXECUTE [dbo].[sp_addFormPeriod] @formId = :form_id, @userLogin = :user_id''')
        params = {
            'form_id': form_id,
            'user_id': user_id,
        }

        try:
            results = await self._session.execute(query, params)

            await self._session.commit()

            if isinstance(results, CursorResult) and results.returns_rows:
                rows = results.fetchall()
                keys = results.keys()

                return [dict(zip(keys, row)) for row in rows]
            return True
        except SQLAlchemyError as e:
            await self._session.rollback()
            return False


class FormPeriodRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def list(self, form_id: str | int | None = None, status: str | None = None):
        filters = []
        if form_id:
            filters.append(models.FormPeriod.form_id == form_id)
        if status:
            filters.append(models.FormPeriod.status == status)

        stmt = select(models.FormPeriod).filter(*filters).order_by(models.FormPeriod.xd_creation)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get(self, period_id: str | int | None = None, status: str | None = None):
        filters = []
        if period_id:
            filters.append(models.FormPeriod.period_id == period_id)
        if status:
            filters.append(models.FormPeriod.status == status)

        stmt = select(models.FormPeriod).filter(*filters).order_by(models.FormPeriod.xd_creation)
        result = await self._session.execute(stmt)
        return result.scalars().first()


class SceneryRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def list(self, status: str | None = None):
        filters = []
        if status:
            filters.append(models.Scenery.status == status)

        stmt = select(models.Scenery).filter(*filters).order_by(models.Scenery.xd_creation)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get(self, scenery_id: str | int | None = None, status: str | None = None):
        filters = []
        if scenery_id:
            filters.append(models.Scenery.id == scenery_id)
        if status:
            filters.append(models.Scenery.status == status)

        stmt = select(models.Scenery).filter(*filters).order_by(models.Scenery.xd_creation)
        result = await self._session.execute(stmt)
        return result.scalars().first()


class LocationStructureRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def list(self, status: str | None = None):
        filters = []
        if status:
            filters.append(models.LocationStructure.status == status)

        stmt = select(models.LocationStructure).filter(*filters).order_by(models.LocationStructure.xd_creation)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get(self, location_id: str | int | None = None, status: str | None = None):
        filters = []
        if location_id:
            filters.append(models.LocationStructure.id == location_id)
        if status:
            filters.append(models.LocationStructure.status == status)

        stmt = select(models.LocationStructure).filter(*filters).order_by(models.LocationStructure.xd_creation)
        result = await self._session.execute(stmt)
        return result.scalars().first()


class MeasureRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def list(self, status: str | None = None):
        filters = []
        if status:
            filters.append(models.Measure.status == status)

        stmt = select(models.Measure).filter(*filters).order_by(models.Measure.xd_creation)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get(self, measure_id: str | int | None = None, status: str | None = None):
        filters = []
        if measure_id:
            filters.append(models.Measure.id == measure_id)
        if status:
            filters.append(models.Measure.status == status)

        stmt = select(models.Measure).filter(*filters).order_by(models.Measure.xd_creation)
        result = await self._session.execute(stmt)
        return result.scalars().first()
