import logging
from contextlib import asynccontextmanager
from datetime import datetime

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from uvicorn.config import LOGGING_CONFIG

from src.api import protected_api_router, public_api_router
from src.config import settings
from src.core import session_manager
from src.logging_config import setup_logging

try:
    from asgi_correlation_id import CorrelationIdMiddleware, CorrelationIdFilter
except ImportError:
    CorrelationIdMiddleware = None
    CorrelationIdFilter = None

@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    setup_logging(settings)
    session_manager.init(
        settings.sqlalchemy_database_uri,
        sqlalchemy_echo=settings.sqlalchemy_echo,
        otel_enable_commenter=settings.otel_sqlalchemy_enable_commenter,
        otel_enable_attribute_commenter=settings.otel_sqlalchemy_enable_attribute_commenter,
        otel_commenter_options={
            "db_driver": settings.otel_sqlalchemy_commenter_db_driver,
            "db_framework": settings.otel_sqlalchemy_commenter_db_framework,
            "opentelemetry_values": settings.otel_sqlalchemy_commenter_otel_values,
        },
    )
    yield
    await session_manager.close(raise_exception=False)


app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    docs_url=settings.api_docs_url,
    redoc_url=settings.api_redoc_url,
    openapi_url=settings.api_openapi_url,
    debug=settings.api_debug,
    lifespan=lifespan
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
    allow_credentials=settings.cors_allow_credentials,
    allow_origin_regex=settings.cors_allow_origin_regex,
    expose_headers=settings.cors_expose_headers,
    max_age=settings.cors_max_age,
)

app.include_router(protected_api_router)

app.include_router(public_api_router)
if CorrelationIdMiddleware is not None:
    try:
        app.add_middleware(CorrelationIdMiddleware)
    except Exception:
        pass
else:
    logging.debug("asgi_correlation_id not installed; skipping instrumentation.")
try:
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    FastAPIInstrumentor.instrument_app(app)
except Exception:
    logging.debug("opentelemetry-instrumentation-fastapi not installed; skipping instrumentation.")


@app.head("/")
@app.get("/", include_in_schema=False)
async def root_health():
    return {"status": "healthy"}


@app.get("/health", include_in_schema=False)
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": settings.api_version
    }

if __name__ == "__main__":
    if CorrelationIdFilter is not None:
        LOGGING_CONFIG["handlers"]["access"]["filters"] = [CorrelationIdFilter()]
        LOGGING_CONFIG["formatters"]["access"]["fmt"] = "%(levelname)s access [%(correlation_id)s] %(name)s %(message)s"
    uvicorn.run(app, host="localhost", port=8000, log_level="debug")
