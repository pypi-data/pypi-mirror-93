from pathlib import Path
from typing import List

from yoyo import read_migrations
from yoyo import get_backend

from constellate.database.migration.databasetype import DatabaseType
from constellate.database.migration.migrationaction import MigrationAction
from constellate.database.migration.migrationerror import MigrationException


def _migrate_with_yoyo(
    connection_url: str = None,
    migration_dirs: List[Path] = [],
    action: MigrationAction = MigrationAction.UNKNOWN,
    logger=None,
):
    """Run database migrations using yoyo library: https://ollycope.com/software/yoyo/latest/#migrations-as-sql-scripts"""

    backend = get_backend(connection_url)
    migrations = read_migrations([str(path) for path in migration_dirs])

    try:
        with backend.lock():
            if action == MigrationAction.UP:
                # Apply any outstanding migrations
                backend.apply_migrations(backend.to_apply(migrations))
            elif action == MigrationAction.DOWN:
                # Rollback all migrations
                backend.rollback_migrations(backend.to_rollback(migrations))
    except BaseException as e:
        raise MigrationException() from e


def _migrate_unsupported(
    connection_url: str = None,
    migration_dirs: List[Path] = [],
    action: MigrationAction = MigrationAction.UNKNOWN,
    logger=None,
):
    raise MigrationException("Migration not supported")


def migrate(
    database_type: DatabaseType = DatabaseType.UNKNOWN,
    connection_url: str = None,
    migration_dirs: List[Path] = [],
    action: MigrationAction = MigrationAction.UNKNOWN,
    logger=None,
):
    """Run database migrations.
    :migration_dirs: List of directory contains SQL file scripts (or equivalent)
    :raises:
        MigrationException When migration fails
    """
    DB_TYPE_TO_MIGRATOR = {
        DatabaseType.SQLITE: _migrate_with_yoyo,
        DatabaseType.POSTGRESQL: _migrate_with_yoyo,
    }

    migrate = DB_TYPE_TO_MIGRATOR(database_type, self._migrate_unsupported)
    migrate(
        connection_url=connection_url, migration_dir=migration_dirs, action=action, logger=logger
    )
