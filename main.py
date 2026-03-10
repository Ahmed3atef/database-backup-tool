import logging
import os
import asyncio
from core.backup import full_backup
from datetime import datetime
from core.backup.executors import DockerExecutor, LocalExecutor, SSHExecutor, SSHDockerExecutor
from core.utils import setup_logger, setup_backups_dir, project_root


if __name__ == "__main__":
    try:
        from UI.app import BackupApp
        app = BackupApp()
        app.run()
    except ImportError as e:
        raise e