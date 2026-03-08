import logging
from .base import BaseDatabaseBackup

class MySQLBackup(BaseDatabaseBackup):
    def backup(self, output_file: str, logger: logging.Logger) -> str:
        try:
            # mysqldump outputs raw text directly. 
            # We fetch the exact command and delegate its execution to the attached executor.
            command = ["mysqldump", "-u", self.db_user, f"-p{self.db_pass}", self.db_name]
            
            # The executor (Local, Docker, SSH) runs the command and returns the raw SQL dump as a string.
            backup_data = self.executor.execute(command)
            
            # Save the raw dump securely into the desired local output file.
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(backup_data)
            
            logger.info(f"MySQL backup of {self.db_name} completed successfully, saved to {output_file}.")
            return output_file
        except Exception as e:
            logger.error(f"Error occurred during MySQL backup of {self.db_name}: {e}")
            raise
