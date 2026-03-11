import logging
from .factory import BackupFactory
from .base import BaseDatabaseBackup
from .mysql import MySQLBackup
from .postgres import PostgreSQLBackup
from .mongo import MongoDBBackup
from .sqlite import SQLiteBackup
from .executors import LocalExecutor, DockerExecutor, SSHExecutor, SSHDockerExecutor, BaseExecutor

async def full_backup(db_type: str, db_name: str, db_user: str, db_pass: str, output_file: str, logger: logging.Logger, executor: BaseExecutor = None) -> str:
    """
    Main entry point function for performing backups. 
    It is safely isolated in this dedicated module structure.
    If no executor is provided, defaults to the LocalExecutor.
    """
    if executor is None:
        executor = LocalExecutor()
        
    try:
        # The factory provides the correct database class strategy combined with its execution environment
        strategy = BackupFactory.get_strategy(db_type, db_name, db_user, db_pass, executor)
        
        # Execute the unified backup method
        return await strategy.backup(output_file, logger)
        
    except ValueError as e:
        logger.error(str(e))
        raise

async def full_restore(db_type: str, db_name: str, db_user: str, db_pass: str, input_file: str, logger: logging.Logger, executor: BaseExecutor = None) -> None:
    """
    Main entry point function for performing restores.
    """
    if executor is None:
        executor = LocalExecutor()
        
    try:
        strategy = BackupFactory.get_strategy(db_type, db_name, db_user, db_pass, executor)
        await strategy.restore(input_file, logger)
    except ValueError as e:
        logger.error(str(e))
        raise

__all__ = [
    "full_backup",
    "full_restore",
    "BackupFactory",
    "BaseDatabaseBackup",
    "BaseExecutor",
    "LocalExecutor",
    "DockerExecutor",
    "SSHExecutor",
    "SSHDockerExecutor",
    "MySQLBackup",
    "PostgreSQLBackup",
    "MongoDBBackup",
    "SQLiteBackup",
]
