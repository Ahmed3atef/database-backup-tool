import asyncio
import subprocess
import paramiko
from abc import ABC, abstractmethod
from typing import List, Optional

class BaseExecutor(ABC):
    """
    Abstract Interface for execution environments (Local, Docker, SSH).
    The execute method must stream its output directly to an output file.
    """
    @abstractmethod
    async def execute(self, cmd: List[str], output_file: str, env: Optional[dict] = None) -> None:
        """Executes the command asynchronously and writes output directly to output_file."""
        pass


class LocalExecutor(BaseExecutor):
    """Executes commands on the local machine (host)."""
    async def execute(self, cmd: List[str], output_file: str, env: Optional[dict] = None) -> None:
        import os
        is_windows = (os.name == 'nt')
        
        # Merge current environ with given env variables to ensure commands like mysqldump/pg_dump are found
        full_env = os.environ.copy()
        if env:
            full_env.update(env)
            
        with open(output_file, 'wb') as f:
            if is_windows:
                # asyncio.create_subprocess_exec on Windows sometimes struggles with .exe resolution if not specified, 
                # but usually works fine. Using create_subprocess_shell is generally safer for Windows paths.
                cmd_str = " ".join(cmd)
                process = await asyncio.create_subprocess_shell(
                    cmd_str,
                    stdout=f,
                    stderr=asyncio.subprocess.PIPE,
                    env=full_env
                )
            else:
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=f,
                    stderr=asyncio.subprocess.PIPE,
                    env=full_env
                )
                
            _, stderr = await process.communicate()
            
            if process.returncode != 0:
                raise Exception(f"Local Execution Error: {stderr.decode('utf-8', errors='replace')}")


class DockerExecutor(BaseExecutor):
    """Executes commands inside a running Docker container."""
    def __init__(self, container_name: str):
        self.container_name = container_name
        
    async def execute(self, cmd: List[str], output_file: str, env: Optional[dict] = None) -> None:
        # Prepend the Docker execution command
        docker_cmd = ["docker", "exec", "-i"]
        
        # Add environment variables directly into the docker command if needed 
        # (Since subprocess env variables apply to the local docker CLI, not inside the container)
        if env:
            for key, val in env.items():
                docker_cmd.extend(["-e", f"{key}={val}"])
                
        docker_cmd.append(self.container_name)
        docker_cmd.extend(cmd)
        
        with open(output_file, 'wb') as f:
            process = await asyncio.create_subprocess_exec(
                *docker_cmd,
                stdout=f,
                stderr=asyncio.subprocess.PIPE
            )
            
            _, stderr = await process.communicate()
            
            if process.returncode != 0:
                raise Exception(f"Docker Execution Error: {stderr.decode('utf-8', errors='replace')}")


class SSHExecutor(BaseExecutor):
    """Executes commands remotely on a server via SSH connection."""
    def __init__(self, host: str, user: str, password: str):
        self.host = host
        self.user = user
        self.password = password
        
    def _run_ssh_sync(self, command_str: str, output_file: str) -> None:
        """Synchronous wrapper to stream SSH output so we can run it in a thread."""
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.host, username=self.user, password=self.password)
            _, stdout, stderr = ssh.exec_command(command_str)
            
            # Stream the raw bytes directly to disk to prevent OOM
            with open(output_file, 'wb') as f:
                while True:
                    data = stdout.read(1024 * 1024) # read 1MB chunks
                    if not data:
                        break
                    f.write(data)
            
            error_data = stderr.read().decode('utf-8', errors='replace')
            exit_status = stdout.channel.recv_exit_status()
            
            if exit_status != 0: 
                raise Exception(f"SSH Execution Error: {error_data}")
        finally:
            ssh.close()
            
    async def execute(self, cmd: List[str], output_file: str, env: Optional[dict] = None) -> None:
        env_prefix = ""
        if env:
            env_prefix = " ".join([f"{k}={v}" for k, v in env.items()]) + " "
            
        command_str = env_prefix + " ".join(cmd)
        
        # Run the synchronous SSH loop inside a thread to not block asyncio
        await asyncio.to_thread(self._run_ssh_sync, command_str, output_file)


class SSHDockerExecutor(BaseExecutor):
    """Executes commands remotely inside a Docker container via SSH connection."""
    def __init__(self, host: str, user: str, password: str, container_name: str):
        self.host = host
        self.user = user
        self.password = password
        self.container_name = container_name
        
    def _run_ssh_sync(self, command_str: str, output_file: str) -> None:
        """Synchronous wrapper to stream SSH Output."""
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.host, username=self.user, password=self.password)
            _, stdout, stderr = ssh.exec_command(command_str)
            
            with open(output_file, 'wb') as f:
                while True:
                    data = stdout.read(1024 * 1024) # read 1MB chunks
                    if not data:
                        break
                    f.write(data)
            
            error_data = stderr.read().decode('utf-8', errors='replace')
            exit_status = stdout.channel.recv_exit_status()
            
            if exit_status != 0: 
                raise Exception(f"SSH Docker Execution Error: {error_data}")
        finally:
            ssh.close()
        
    async def execute(self, cmd: List[str], output_file: str, env: Optional[dict] = None) -> None:
        docker_cmd = ["docker", "exec", "-i"]
        
        # Docker needs explicit -e flags to pass variables into the container environment.
        if env:
            for key, val in env.items():
                # Avoid quoting issues by formatting it simply 
                # (paramiko will send the whole string to the shell)
                docker_cmd.extend(["-e", f"{key}={val}"])
                
        docker_cmd.append(self.container_name)
        docker_cmd.extend(cmd)
        
        command_str = " ".join(docker_cmd)
        
        await asyncio.to_thread(self._run_ssh_sync, command_str, output_file)
