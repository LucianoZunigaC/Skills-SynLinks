from pydantic import Field
from pydantic_settings import BaseSettings


class SQLAlchemySettings(BaseSettings):
    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
    sqlalchemy_database_uri: str = (
        Field(default='',
              validation_alias='SQLALCHEMY_DATABASE_URI',
              description='The database URI that should be used for the connection.'))
    sqlalchemy_echo: bool = (
        Field(default=False,
              validation_alias='SQLALCHEMY_ECHO',
              description='If set to True SQLAlchemy will log all the statements issued to stderr which can be useful '
                          'for debugging.'))

    # OpenTelemetry SQLAlchemy instrumentation configuration
    otel_sqlalchemy_enable_commenter: bool = (
        Field(default=True,
              validation_alias='OTEL_SQLALCHEMY_ENABLE_COMMENTER',
              description='Enable SQLCommenter to append contextual tags to SQL queries.'))
    otel_sqlalchemy_enable_attribute_commenter: bool = (
        Field(default=False,
              validation_alias='OTEL_SQLALCHEMY_ENABLE_ATTRIBUTE_COMMENTER',
              description='Append SQLCommenter tags to db.statement span attribute. Use carefully due to cardinality.'))
    otel_sqlalchemy_commenter_db_driver: bool = (
        Field(default=True,
              validation_alias='OTEL_SQLALCHEMY_COMMENTER_DB_DRIVER',
              description='Include underlying DB driver in SQLCommenter tags.'))
    otel_sqlalchemy_commenter_db_framework: bool = (
        Field(default=True,
              validation_alias='OTEL_SQLALCHEMY_COMMENTER_DB_FRAMEWORK',
              description='Include framework and version in SQLCommenter tags.'))
    otel_sqlalchemy_commenter_otel_values: bool = (
        Field(default=True,
              validation_alias='OTEL_SQLALCHEMY_COMMENTER_OTEL_VALUES',
              description='Include traceparent values in SQLCommenter tags for correlation.'))
