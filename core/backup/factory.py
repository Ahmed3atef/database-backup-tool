from .base import BaseDatabaseBackup
from .mysql import MySQLBackup
from .postgres import PostgreSQLBackup
from .mongo import MongoDBBackup
from .sqlite import SQLiteBackup
from .executors import BaseExecutor

class BackupFactory:
    """Helper class designed to inspect the database type and return the appropriate strategy."""
    @staticmethod
    def get_strategy(db_type: str, db_name: str, db_user:str, db_pass: str, executor: BaseExecutor = None) -> BaseDatabaseBackup:
        db_type = db_type.lower()
        if db_type == "mysql":
            strategy = MySQLBackup(db_name, db_user, db_pass)
        elif db_type == "postgresql":
            strategy = PostgreSQLBackup(db_name, db_user, db_pass)
        elif db_type == "mongodb":
            strategy = MongoDBBackup(db_name, db_user, db_pass)
        elif db_type == "sqlite":
            strategy = SQLiteBackup(db_name, db_user, db_pass)
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
            
        # Attach the designated execution environment (Local/Docker/SSH)
        strategy.executor = executor
        return strategy
