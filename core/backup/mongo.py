import logging
from .base import BaseDatabaseBackup

class MongoDBBackup(BaseDatabaseBackup):
    async def backup(self, output_file: str, logger: logging.Logger) -> str:
        try:
            # mongodump doesn't naturally act like pg_dump using streams,
            # but using --archive flag instead of --out outputs the raw dump bytes directly to stdout.
            command = ["mongodump", "--db", self.db_name, "--archive"]
            
            # Raw Archive Execution through the injected Docker/SSH/Local strategy
            await self.executor.execute(command, output_file=output_file)
                
            logger.info(f"MongoDB backup of {self.db_name} completed successfully, saved to {output_file}.")
            return output_file
        except Exception as e:
            logger.error(f"Error occurred during MongoDB backup of {self.db_name}: {e}")
            raise
