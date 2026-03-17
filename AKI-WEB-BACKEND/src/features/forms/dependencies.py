from fastapi import Depends

from .repositories import FormRepository, FormPeriodRepository, SceneryRepository, LocationStructureRepository, \
    MeasureRepository
from .services import FormService, FormPeriodService, SceneryService, LocationStructureService, MeasureService
from ...core import AsyncSessionDep


async def get_form_repository(session: AsyncSessionDep):
    yield FormRepository(session)


async def get_form_service(repository: FormRepository = Depends(get_form_repository)):
    yield FormService(repository)


async def get_form_period_repository(db: AsyncSessionDep):
    yield FormPeriodRepository(db)


async def get_form_period_service(repository: FormPeriodRepository = Depends(get_form_period_repository)):
    yield FormPeriodService(repository)


async def get_scenery_repository(db: AsyncSessionDep):
    yield SceneryRepository(db)


async def get_scenery_service(repository: SceneryRepository = Depends(get_scenery_repository)):
    yield SceneryService(repository)


async def get_location_repository(db: AsyncSessionDep):
    yield LocationStructureRepository(db)


async def get_location_service(repository: LocationStructureRepository = Depends(get_location_repository)):
    yield LocationStructureService(repository)


async def get_measure_repository(db: AsyncSessionDep):
    yield MeasureRepository(db)


async def get_measure_service(repository: MeasureRepository = Depends(get_measure_repository)):
    yield MeasureService(repository)
