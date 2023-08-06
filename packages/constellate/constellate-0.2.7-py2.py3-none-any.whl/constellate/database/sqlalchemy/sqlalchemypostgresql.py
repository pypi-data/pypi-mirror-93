from typing import Dict, Tuple

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from constellate.database.migration.databasetype import DatabaseType
from constellate.database.migration.migrate import migrate
from constellate.database.migration.migrationaction import MigrationAction
from constellate.database.sqlalchemy.sqlalchemy import SQLAlchemy


class SQLAlchemyPostgresql(SQLAlchemy):
    def __init__(self):
        super().__init__()

    def _create_engine(self, options: Dict) -> Tuple[str, object]:
        """
        :options:
        - host:str               . DB host
        - port:str               . DB port
        - username:str           . DB user name
        - password:str           . DB password
        - db_name:str            . DB name
        """
        # Create engine
        # - https://docs.sqlalchemy.org/en/14/dialects/postgresql.html
        connection_uri = (
            f"postgresql://{options.get('username', None)}:{options.get('password', None)}@"
            f"{options.get('host', None)}:{options.get('port', None)}/{options.get('db_name',None)}"
        )
        if not database_exists(connection_uri):
            self._create_database(connection_uri=connection_uri)

        engine = create_engine(connection_uri)
        return connection_uri, engine

    def _create_database(self, connection_uri: str = None, encoding="UTF8"):
        create_database(connection_uri, encoding=encoding)

    def _migrate(self, options: Dict = {}):
        migrate(
            database_type=DatabaseType.POSTGRESQL,
            connection_url=self._conection_uri,
            migration_dirs=options.get("migrations_dirs", []),
            action=MigrationAction.UP,
            logger=self._logger,
        )
