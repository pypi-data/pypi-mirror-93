from typing import Dict, Tuple

from sqlalchemy import create_engine

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
            f"postgresql+psycopg2://{options.get('username', None)}:{options.get('password', None)}@{options.get('host', None)}:{options.get('port', None)}/{options.get('db_name', None)}",
        )
        # To see commit statement: add echo=True, echo_pool=True
        engine = create_engine(connection_uri)

        # Create db if missing
        self._create_database(name=options.get("db_nbame", None))
        return connection_uri, engine

        return connection_uri, engine

    def _create_database(self, db_name: str = "foobar", encoding="UTF8"):
        connection = None
        try:
            connection = self._engine.connect().execution_options(
                isolation_level="REPEATABLE READ"  # database creation requires not transaction support
            )
            with connection.begin():
                connection.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} ENCODING {encoding};")
        except BaseException as e:
            raise Exception() from e
        finally:
            if connection is not None:
                connection.close()

    def _migrate(self, options: Dict = {}):
        migrate(
            database_type=DatabaseType.POSTGRESQL,
            connection_url=self._conection_uri,
            migration_dirs=options.get("migrations_dirs", []),
            action=MigrationAction.UP,
            logger=self._logger,
        )
