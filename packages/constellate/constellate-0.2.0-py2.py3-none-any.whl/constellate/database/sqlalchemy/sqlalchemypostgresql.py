from typing import Dict, Tuple

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
        - db_file:str           . Absolute db file path
        - check_same_thread:bool. Default False
        - timeout:int           . Default 20s
        - uri:bool              . Default: True
        """
        return connection_uri, engine

    def migrate(self, options: Dict = {}):
        migrate(
            database_type=DatabaseType.POSTGRESQL,
            connection_url=self._conection_uri,
            migration_dirs=options.get("migrations_dirs", []),
            action=MigrationAction.UP,
            logger=self._logger,
        )
