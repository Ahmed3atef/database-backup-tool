import subprocess
import paramiko
from abc import ABC, abstractmethod
from typing import List, Optional

class BaseExecutor(ABC):
    """
    Abstract Interface for execution environments (Local, Docker, SSH).
    The execute method must return the raw text output (dump data) of the command.
    """
    @abstractmethod
    def execute(self, cmd: List[str], env: Optional[dict] = None) -> str:
        """Executes the command and returns the string output containing data."""
        pass


class LocalExecutor(BaseExecutor):
    """Executes commands on the local machine (host)."""
    def execute(self, cmd: List[str], env: Optional[dict] = None) -> str:
        # Use shell=True dynamically for Windows to resolve commands not fully mapped in PATH
        import os
        is_windows = (os.name == 'nt')
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, shell=is_windows)
        
        if result.returncode != 0:
            raise Exception(f"Local Execution Error: {result.stderr}")
        return result.stdout


class DockerExecutor(BaseExecutor):
    """Executes commands inside a running Docker container."""
    def __init__(self, container_name: str):
        self.container_name = container_name
        
    def execute(self, cmd: List[str], env: Optional[dict] = None) -> str:
        # Prepend the Docker execution command
        docker_cmd = ["docker", "exec", "-i"]
        
        # Add environment variables directly into the docker command if needed 
        # (Since subprocess env variables apply to the local docker CLI, not inside the container)
        if env:
            for key, val in env.items():
                docker_cmd.extend(["-e", f"{key}={val}"])
                
        docker_cmd.append(self.container_name)
        docker_cmd.extend(cmd)
        
        result = subprocess.run(docker_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Docker Execution Error: {result.stderr}")
        return result.stdout


class SSHExecutor(BaseExecutor):
    """Executes commands remotely on a server via SSH connection."""
    def __init__(self, host: str, user: str, password: str):
        self.host = host
        self.user = user
        self.password = password
        
    def execute(self, cmd: List[str], env: Optional[dict] = None) -> str:
        # Convert the command list to a string recognizable by standard remote shells
        # Apply remote environment variables prefixing the command line
        env_prefix = ""
        if env:
            env_prefix = " ".join([f"{k}={v}" for k, v in env.items()]) + " "
            
        command_str = env_prefix + " ".join(cmd)
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.host, username=self.user, password=self.password)
            stdin, stdout, stderr = ssh.exec_command(command_str)
            
            error_data = stderr.read().decode('utf-8')
            output_data = stdout.read().decode('utf-8')
            
            # Paramiko SSH doesn't throw subprocess exceptions directly, so check errors
            if error_data and not output_data: 
                raise Exception(f"SSH Execution Error: {error_data}")
                
            return output_data
        finally:
            ssh.close()


class SSHDockerExecutor(BaseExecutor):
    """Executes commands remotely inside a Docker container via SSH connection."""
    def __init__(self, host: str, user: str, password: str, container_name: str):
        self.host = host
        self.user = user
        self.password = password
        self.container_name = container_name
        
    def execute(self, cmd: List[str], env: Optional[dict] = None) -> str:
        docker_cmd = ["docker", "exec", "-i"]
        if env:
            for key, val in env.items():
                docker_cmd.extend(["-e", f"{key}={val}"])
        docker_cmd.append(self.container_name)
        
        # We need to execute the command inside the container.
        # Note: if cmd arguments have spaces, it's safer to properly quote them, 
        # but for consistency with SSHExecutor we just join.
        docker_cmd.extend(cmd)
        command_str = " ".join(docker_cmd)
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.host, username=self.user, password=self.password)
            stdin, stdout, stderr = ssh.exec_command(command_str)
            
            error_data = stderr.read().decode('utf-8')
            output_data = stdout.read().decode('utf-8')
            
            if error_data and not output_data: 
                raise Exception(f"SSH Docker Execution Error: {error_data}")
                
            return output_data
        finally:
            ssh.close()
