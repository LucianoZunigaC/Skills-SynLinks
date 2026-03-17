import logging
from logging import Handler
from typing import Optional

try:
    from asgi_correlation_id import CorrelationIdFilter
except ImportError:
    CorrelationIdFilter = None  # type: ignore


def _make_handler(level: int, fmt: str) -> Handler:
    handler = logging.StreamHandler()
    if CorrelationIdFilter is not None:
        try:
            handler.addFilter(CorrelationIdFilter())
        except Exception:
            pass
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    handler.setLevel(level)
    return handler


def setup_logging(settings: Optional[object] = None) -> None:
    """
    Configure logging with separated handlers for application, access and SQL logs.

    - Application logs: root logger
    - Access logs: logger 'uvicorn.access'
    - SQL logs: logger 'sqlalchemy.engine'
    """
    # Derive levels from settings when available
    api_debug = getattr(settings, "api_debug", False)
    sqlalchemy_echo = getattr(settings, "sqlalchemy_echo", False)

    app_level = logging.DEBUG if api_debug else logging.INFO
    access_level = logging.INFO
    sql_level = logging.INFO if sqlalchemy_echo else logging.WARNING

    has_corr = CorrelationIdFilter is not None
    fmt_app = (
        "%(levelname)s app [%(correlation_id)s] %(name)s %(message)s"
        if has_corr else
        "%(levelname)s app %(name)s %(message)s"
    )
    fmt_access = (
        "%(levelname)s access [%(correlation_id)s] %(message)s"
        if has_corr else
        "%(levelname)s access %(message)s"
    )
    fmt_sql = (
        "%(levelname)s sql [%(correlation_id)s] %(name)s %(message)s"
        if has_corr else
        "%(levelname)s sql %(name)s %(message)s"
    )

    # Handlers and formatters
    app_handler = _make_handler(app_level, fmt_app)
    access_handler = _make_handler(access_level, fmt_access)
    sql_handler = _make_handler(sql_level, fmt_sql)

    # Root application logger
    root_logger = logging.getLogger()
    root_logger.handlers = []
    root_logger.addHandler(app_handler)
    root_logger.setLevel(app_level)

    # Uvicorn access logger
    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_access.handlers = []
    uvicorn_access.addHandler(access_handler)
    uvicorn_access.setLevel(access_level)
    uvicorn_access.propagate = False

    # SQLAlchemy engine logger
    sa_engine = logging.getLogger("sqlalchemy.engine")
    sa_engine.handlers = []
    sa_engine.addHandler(sql_handler)
    sa_engine.setLevel(sql_level)
    sa_engine.propagate = False

    # Optional: pool/ORM detailed logs when echo enabled
    if sqlalchemy_echo:
        for name in ("sqlalchemy.pool", "sqlalchemy.orm"):  # more verbose only when echo
            lg = logging.getLogger(name)
            lg.handlers = []
            lg.addHandler(sql_handler)
            lg.setLevel(sql_level)
            lg.propagate = False