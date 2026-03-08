import os
import logging
from .base import BaseDatabaseBackup

class PostgreSQLBackup(BaseDatabaseBackup):
    async def backup(self, output_file: str, logger: logging.Logger) -> str:
        try:
            # Ask pg_dump to output in Plain Text SQL directly to stdout so we can catch it from ANY executor
            # Note: We omit the '-f' flag to catch the raw stream instead.
            command = ["pg_dump", "-U", self.db_user, "-F", "p", "-b", "-v", self.db_name]
            
            # Pass the Password via Environment Dictionary
            env_vars = {}
            if self.db_pass:
                env_vars['PGPASSWORD'] = self.db_pass

            # Let the executor securely handle reaching the database internally
            # The executor will stream the stdout directly to output_file
            await self.executor.execute(command, output_file=output_file, env=env_vars)
                
            logger.info(f"PostgreSQL backup of {self.db_name} completed successfully, saved to {output_file}.")
            return output_file
        except Exception as e:
            logger.error(f"Error occurred during PostgreSQL backup of {self.db_name}: {e}")
            raise
