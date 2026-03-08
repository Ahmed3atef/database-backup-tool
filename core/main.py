import logging
import os
from backup import full_backup
from datetime import datetime
from backup.executors import DockerExecutor, LocalExecutor, SSHExecutor

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

def setup_backups_dir() -> str:
    backups_dir = os.path.join(project_root, "backups")
    os.makedirs(backups_dir, exist_ok=True)
    filename = f"shop_db_backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sql"
    output_file = os.path.join(backups_dir, filename)
    return output_file

def get_db_type() -> str:
    type_of_db = {
        1: "mysql",
        2: "postgresql",
        3: "sqlite",
        4: "mongodb"
    }
    
    print("\nSelect the type of database you want to backup:")
    print(type_of_db)
    choice = int(input("Enter your choice: "))
    
    if choice not in type_of_db:
        logger.error("Invalid Choice, pelease try again.")
        raise ValueError("Invalid Choice, pelease try again.")
    
    db_type = type_of_db[choice]
    return db_type

def get_executor_type() -> str:
    type_of_executor = {
        1: "local",
        2: "docker",
        3: "ssh",
        4: "ssh_docker"
    }
    
    print("\nEnter the type of executor:")
    print(type_of_executor)
    choice = int(input("Enter your choice: "))
    
    if choice not in type_of_executor:
        logger.error("Invalid Executor Type")
        raise TypeError("Invalid Executor Type")
    
    executor_type = type_of_executor[choice]
    if executor_type == "docker":
        container_name = input("Enter the name of the docker container: ")
        return DockerExecutor(container_name="backup_postgres")
    elif executor_type == "local":
        return LocalExecutor()
    elif executor_type == "ssh":
        host = input("Enter the host: ")
        port = input("Enter the port: ")
        username = input("Enter the username: ")
        password = input("Enter the password: ")
        return SshExecutor(host=host, port=port, username=username, password=password)
    elif executor_type == "ssh_docker":
        host = input("Enter the host: ")
        port = input("Enter the port: ")
        username = input("Enter the username: ")
        password = input("Enter the password: ")
        container_name = input("Enter the name of the docker container: ")
        return SshDockerExecutor(host=host, port=port, username=username, password=password, container_name=container_name)
    return executor_type

def get_db_config(username: str, password: str) -> dict:
    return {
        "user": username,
        "password": password
    }
    
def main():
    logger = setup_logger()
    backups_dir = setup_backups_dir()
    db_name = input("Enter the name of the database you want to backup: ")
    user = input("Enter the username: ")
    password = input("Enter the password: ")
    db_type = get_db_type()
    executor_type = get_executor_type()
    db_config = get_db_config(user, password)
    
    full_backup(
        db_type=db_type,
        db_name="shop_db",
        config=db_config,
        output_file=backups_dir,
        logger=logger,
        executor=executor_type
    )

if __name__ == "__main__":
    
    main()
    
    # 2. SQLite Database Example (Runs locally naturally)
    # import sqlite3
    # sqlite_conn = sqlite3.connect("test.db")
    # sqlite_config = {"conn": sqlite_conn}
    # full_backup("sqlite", "test_db", sqlite_config, "test_backup.sql", test_logger)
