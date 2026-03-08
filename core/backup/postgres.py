import os
import logging
from .base import BaseDatabaseBackup

class PostgreSQLBackup(BaseDatabaseBackup):
    def backup(self, output_file: str, logger: logging.Logger) -> str:
        try:
            # Ask pg_dump to output in Plain Text SQL directly to stdout so we can catch it from ANY executor
            # Note: We omit the '-f' flag to catch the raw stream instead.
            command = ["pg_dump", "-U", self.db_user, "-F", "p", "-b", "-v", self.db_name]
            
            # Pass the Password via Environment Dictionary
            env_vars = {}
            if self.db_pass:
                env_vars['PGPASSWORD'] = self.db_pass

            # Let the executor securely handle reaching the database internally
            backup_data = self.executor.execute(command, env=env_vars)
            
            # Save the raw DB stream dump into the desired local output file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(backup_data)
                
            logger.info(f"PostgreSQL backup of {self.db_name} completed successfully, saved to {output_file}.")
            return output_file
        except Exception as e:
            logger.error(f"Error occurred during PostgreSQL backup of {self.db_name}: {e}")
            raise
