import logging
import asyncio
import sqlite3
from .base import BaseDatabaseBackup

class SQLiteBackup(BaseDatabaseBackup):
    def _dump_sync(self, output_file: str) -> None:
        """Run the backup synchronously because iter-dump is blocking IO."""
        conn = sqlite3.connect(self.db_name)
        try:
            with open(output_file, 'w') as f:
                for line in conn.iterdump():
                    f.write('%s\n' % line)
        finally:
            conn.close()

    async def backup(self, output_file: str, logger: logging.Logger) -> str:
        try:
            # SQLite does not rely on an external execution environment (Docker/SSH) 
            # because its instance lives internally in the local file system. 
            # We bypass the executor attribute and use the Python iter-dump directly in a thread.
            await asyncio.to_thread(self._dump_sync, output_file)
                    
            logger.info(f"SQLite backup of {self.db_name} completed successfully, saved to {output_file}.")
            return output_file
        except Exception as e:
            logger.error(f"Error occurred during SQLite backup of {self.db_name}: {e}")
            raise

    def _restore_sync(self, input_file: str) -> None:
        """Run the restore synchronously."""
        conn = sqlite3.connect(self.db_name)
        try:
            with open(input_file, 'r') as f:
                sql = f.read()
                conn.executescript(sql)
        finally:
            conn.close()

    async def restore(self, input_file: str, logger: logging.Logger) -> None:
        try:
            await asyncio.to_thread(self._restore_sync, input_file)
            logger.info(f"SQLite restore of {self.db_name} from {input_file} completed successfully.")
        except Exception as e:
            logger.error(f"Error occurred during SQLite restore of {self.db_name}: {e}")
            raise
