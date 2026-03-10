import logging
import os
import asyncio
from core.backup import full_backup
from datetime import datetime
from core.backup.executors import DockerExecutor, LocalExecutor, SSHExecutor, SSHDockerExecutor
from core.utils import setup_logger, setup_backups_dir, project_root


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
        print("Invalid Choice, please try again.")
        raise ValueError("Invalid Choice, please try again.")
    
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
        print("Invalid Executor Type")
        raise TypeError("Invalid Executor Type")
    
    executor_type = type_of_executor[choice]
    if executor_type == "docker":
        container_name = input("Enter the name of the docker container: ")
        return DockerExecutor(container_name=container_name)
    elif executor_type == "local":
        return LocalExecutor()
    elif executor_type == "ssh":
        host = input("Enter the host: ")
        username = input("Enter the username: ")
        password = input("Enter the password: ")
        return SSHExecutor(host=host, user=username, password=password)
    elif executor_type == "ssh_docker":
        host = input("Enter the host: ")
        username = input("Enter the username: ")
        password = input("Enter the password: ")
        container_name = input("Enter the name of the docker container: ")
        return SSHDockerExecutor(host=host, user=username, password=password, container_name=container_name)
    return executor_type

    
async def main():
    logger = setup_logger()
    db_name = input("Enter the name of the database you want to backup: ")
    user = input("Enter the username: ")
    password = input("Enter the password: ")
    db_type = get_db_type()
    executor_type = get_executor_type()
    backups_dir = setup_backups_dir(db_name)
    
    await full_backup(
        db_type=db_type,
        db_name=db_name,
        db_user= user,
        db_pass = password,
        output_file=backups_dir,
        logger=logger,
        executor=executor_type
    )

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        asyncio.run(main())
    else:
        try:
            from UI.app import BackupApp
            app = BackupApp()
            app.run()
        except ImportError as e:
            raise e
            print("Textual not found or UI.tui missing. Falling back to CLI.")
            asyncio.run(main())
