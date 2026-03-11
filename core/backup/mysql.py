import logging
from .base import BaseDatabaseBackup

class MySQLBackup(BaseDatabaseBackup):
    async def backup(self, output_file: str, logger: logging.Logger) -> str:
        try:
            # mysqldump outputs raw text directly. 
            # We fetch the exact command and delegate its execution to the attached executor.
            command = ["mysqldump", "-u", self.db_user, f"-p{self.db_pass}", self.db_name]
            
            # The executor (Local, Docker, SSH) runs the command and streams raw SQL dump to the file.
            await self.executor.execute(command, output_file=output_file)
            
            logger.info(f"MySQL backup of {self.db_name} completed successfully, saved to {output_file}.")
            return output_file
        except Exception as e:
            logger.error(f"Error occurred during MySQL backup of {self.db_name}: {e}")
            raise

    async def restore(self, input_file: str, logger: logging.Logger) -> None:
        try:
            command = ["mysql", "-u", self.db_user, f"-p{self.db_pass}", self.db_name]
            await self.executor.restore(command, input_file=input_file)
            logger.info(f"MySQL restore of {self.db_name} from {input_file} completed successfully.")
        except Exception as e:
            logger.error(f"Error occurred during MySQL restore of {self.db_name}: {e}")
            raise
