from sqlalchemy import Column, Integer, String, DateTime, Boolean, CHAR, Date, BigInteger, Float

from src.core import Base


class Form(Base):
    __tablename__ = 'forms'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    code = Column("code", String(50), nullable=False, unique=True)
    form_type_id = Column("formTypeId", Integer, nullable=False)
    template_id = Column("templateId", Integer, nullable=False)
    short_name = Column("shortName", String(30), nullable=False)
    full_name = Column("fullName", String(100), nullable=False)
    description = Column("description", String(200), nullable=False)
    layout = Column("layout", String(15), nullable=True)
    trasposed = Column("trasposed", Boolean, nullable=True)
    granularity = Column("granularity", String(50), nullable=False)
    form_type_code = Column("formTypeCode", String(50), nullable=False)
    template_code = Column("templateCode", String(50), nullable=False)
    status = Column("status", CHAR(1), nullable=False)
    entity_type = Column("entityType", String(20), nullable=False)
    xd_creation = Column("xd_creation", DateTime, nullable=False)
    xd_creation_user = Column("xd_creationUser", String(100), nullable=False)
    xd_last_update = Column("xd_lastUpdate", DateTime, nullable=False)
    xd_last_update_user = Column("xd_lastUpdateUsr", String(100), nullable=False)


class FormPeriod(Base):
    __tablename__ = 'form_periods'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    form_id = Column("formId", Integer, nullable=False)
    period_id = Column("periodId", Integer, nullable=False)
    form_code = Column("formCode", String(50), nullable=False)
    period_code = Column("periodCode",String(50), nullable=False)
    status = Column("status", CHAR(1), nullable=False)
    xd_creation = Column("xd_creation", DateTime, nullable=False)
    xd_creation_user = Column("xd_creationUser", String(100), nullable=False)
    xd_last_update = Column("xd_lastUpdate", DateTime, nullable=False)
    xd_last_update_user = Column("xd_lastUpdateUsr",String(100), nullable=False)


class FormPeriodValue(Base):
    __tablename__ = 'form_period_values'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    form_id = Column("formId", Integer, nullable=False)
    period_id = Column("periodId", Integer, nullable=False)
    period_point = Column("periodPoint", Date, nullable=False)
    scenario_id = Column("scenarioId", Integer, nullable=False)
    location_id = Column("locationId", Integer, nullable=False)
    measure_id = Column("measureId", Integer, nullable=False)
    form_code = Column("formCode", String(50), nullable=False)
    period_code = Column("periodCode", String(50), nullable=False)
    scenario_code = Column("scenarioCode", String(50), nullable=False)
    location_code = Column("locationCode", String(50), nullable=False)
    measure_code = Column("measureCode", String(50), nullable=False)
    value_int = Column("valueInt", BigInteger, nullable=True)
    value_decimal = Column("valueDec", Float, nullable=True)
    value_float = Column("valueFloat", Float, nullable=True)
    value_text = Column("valueText", String, nullable=True)
    value_boolean = Column("valueBoolean", Boolean, nullable=True)
    value_datetime = Column("valueDateTime", DateTime, nullable=True)
    status = Column("status", CHAR(1), nullable=False)
    xd_creation = Column("xd_creation", DateTime, nullable=False)
    xd_creation_user = Column("xd_creationUser", String(100), nullable=False)
    xd_last_update = Column("xd_lastUpdate", DateTime, nullable=False)
    xd_last_update_user = Column("xd_lastUpdateUsr", String(100), nullable=False)


class Scenery(Base):
    __tablename__ = 'scenarios'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    code = Column("code", String(50), nullable=False)
    short_name = Column("shortName", String(30), nullable=False)
    full_name = Column("fullName", String(100), nullable=False)
    description = Column("description", String(200), nullable=False)
    status = Column("status", CHAR(1), nullable=False)
    entity_type = Column("entityType", String(20), nullable=False)
    xd_creation = Column("xd_creation", DateTime, nullable=False)
    xd_creation_user = Column("xd_creationUser", String(100), nullable=False)
    xd_last_update = Column("xd_lastUpdate", DateTime, nullable=False)
    xd_last_update_user = Column("xd_lastUpdateUsr", String(100), nullable=False)


class LocationStructure(Base):
    __tablename__ = 'location_structure'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    node_type_id = Column("nodeTypeId", Integer, nullable=False)
    node_type_code = Column("nodeTypeCode", CHAR(5), nullable=False)
    node_code = Column("nodeCode", CHAR(5), nullable=False)
    short_name = Column("shortName", String(30), nullable=False)
    full_name = Column("fullName", String(100), nullable=False)
    description = Column("description", String(200), nullable=False)
    parent_id = Column("parentId", Integer, nullable=False)
    parent_code = Column("parentCode", CHAR(5), nullable=False)
    path = Column("Path", String(100), nullable=False)
    depth = Column("depth", Integer, nullable=False)
    height = Column("height", Integer, nullable=False)
    has_children = Column("hasChildren", Boolean, nullable=False)
    status = Column("status", CHAR(1), nullable=False)
    entity_type = Column("entityType", String(20), nullable=False)
    xd_creation = Column("xd_creation", DateTime, nullable=False)
    xd_creation_user = Column("xd_creationUser", String(100), nullable=False)
    xd_last_update = Column("xd_lastUpdate", DateTime, nullable=False)
    xd_last_update_user = Column("xd_lastUpdateUsr", String(100), nullable=False)


class Measure(Base):
    __tablename__ = 'measures'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    code = Column("code", String(50), nullable=False)
    short_name = Column("shortName", String(30), nullable=False)
    full_name = Column("fullName", String(100), nullable=False)
    description = Column("description", String(200), nullable=False)
    uom_id = Column("uomId", Integer, nullable=False)
    data_type_code = Column("dataTypeCode", String(20), nullable=False)
    status = Column("status", CHAR(1), nullable=False)
    entity_type = Column("entityType", String(20), nullable=False)
    xd_creation = Column("xd_creation", DateTime, nullable=False)
    xd_creation_user = Column("xd_creationUser", String(100), nullable=False)
    xd_last_update = Column("xd_lastUpdate", DateTime, nullable=False)
    xd_last_update_user = Column("xd_lastUpdateUsr", String(100), nullable=False)
