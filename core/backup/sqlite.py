import logging
from .base import BaseDatabaseBackup

class SQLiteBackup(BaseDatabaseBackup):
    def backup(self, output_file: str, logger: logging.Logger) -> str:
        try:
            # SQLite does not rely on an external execution environment (Docker/SSH) 
            # because its instance lives internally in the local file system. 
            # We bypass the executor attribute and use the Python iter-dump directly.
            with open(output_file, 'w') as f:
                for line in self.config['conn'].iterdump():
                    f.write('%s\n' % line)
                    
            logger.info(f"SQLite backup of {self.db_name} completed successfully, saved to {output_file}.")
            return output_file
        except Exception as e:
            logger.error(f"Error occurred during SQLite backup of {self.db_name}: {e}")
            raise
