import logging
from backup import full_backup
from datetime import datetime
from backup.executors import DockerExecutor

if __name__ == "__main__":
    # Configure Logger for demonstration testing
    logging.basicConfig(level=logging.INFO)
    test_logger = logging.getLogger("BackupTool")
    
    pg_config = {"user": "admin", "password": "admin123"}
    docker_runner = DockerExecutor(container_name="backup_postgres")
    
    full_backup(
        db_type="postgresql", 
        db_name="shop_db", 
        config=pg_config, 
        output_file=f"shop_db_backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.dump", 
        logger=test_logger,
        executor=docker_runner
    )
    
    # 2. SQLite Database Example (Runs locally naturally)
    # import sqlite3
    # sqlite_conn = sqlite3.connect("test.db")
    # sqlite_config = {"conn": sqlite_conn}
    # full_backup("sqlite", "test_db", sqlite_config, "test_backup.sql", test_logger)
