from sqlalchemy import Column, Integer, String, Float, DateTime

from src.core import Base


class Upload(Base):
    __tablename__ = 'uploads'

    id = Column("id", Integer, primary_key=True)
    file_name = Column("file_name", String(255), nullable=False)
    file_size = Column("file_size", Float, nullable=False)
    file_content_type = Column("file_content_type", String(100))
    storage_url = Column("storage_url", String(1024), nullable=False)
    xd_creation = Column("xd_creation", DateTime, nullable=False)
    xd_creation_user = Column("xd_creationUser", String(100), nullable=False)
    xd_last_update = Column("xd_lastUpdate", DateTime, nullable=False)
    xd_last_update_user = Column("xd_lastUpdateUsr", String(100), nullable=False)


class Period(Base):
    __tablename__ = 'periods'

    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)
    calendar_code = Column("calendarCode", String(50), nullable=False)
    type = Column("type", String(50), nullable=False)
    sub_type = Column("subType", String(50), nullable=True)
    code = Column("code", String(50), nullable=False)
    p_year = Column("pYear", Integer, nullable=True)
    p_month = Column("pMonth", Integer, nullable=True)
    p_start = Column("pStart", DateTime, nullable=False)
    p_end = Column("pEnd", DateTime, nullable=False)
    label1 = Column("label1", String(50), nullable=False)
    label2 = Column("label2", String(50), nullable=True)
    label3 = Column("label3", String(50), nullable=True)
    entity_type = Column("entityType", String(20), nullable=False)
    xd_creation = Column("xd_creation", DateTime, nullable=False)
    xd_creation_user = Column("xd_creationUser", String(100), nullable=False)
    xd_last_update = Column("xd_lastUpdate", DateTime, nullable=False)
    xd_last_update_user = Column("xd_lastUpdateUsr", String(100), nullable=False)
