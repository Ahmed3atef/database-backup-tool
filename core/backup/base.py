import logging
from abc import ABC, abstractmethod

class BaseDatabaseBackup(ABC):
    """Abstract Interface for all database backup strategies."""
    def __init__(self, db_name: str, config: dict):
        self.db_name = db_name
        self.config = config

    @abstractmethod
    def backup(self, output_file: str, logger: logging.Logger) -> str:
        """Every database class must implement this method."""
        pass
