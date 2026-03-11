import logging
import os
import asyncio
from core.backup import full_backup
from datetime import datetime


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def setup_logger() -> logging.Logger:
    logs_dir = os.path.join(project_root, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    log_filename = f"backup_run_{datetime.now().strftime('%Y-%m-%d')}.log"
    log_filepath = os.path.join(logs_dir, log_filename)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filepath, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    test_logger = logging.getLogger("BackupTool")
    return test_logger

def setup_backups_dir(db_name: str) -> str:
    backups_dir = os.path.join(project_root, "backups")
    os.makedirs(backups_dir, exist_ok=True)
    filename = f"{db_name}_backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sql"
    output_file = os.path.join(backups_dir, filename)
    return output_file
