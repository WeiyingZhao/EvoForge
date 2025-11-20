"""
Docker-based sandbox for secure code execution.
Implements AlphaEvolve's safety requirements.
"""
import docker
from typing import Dict, Any, Optional
import time
import tempfile
import os
from .executor import SandboxExecutor, ExecutionStatus
from loguru import logger


class DockerSandbox(SandboxExecutor):
    """
    Docker-based sandbox executor.

    Features:
    - Isolated container per execution
    - Resource limits enforced by Docker
    - Automatic cleanup
    - Support for multiple languages
    """

    def __init__(
        self,
        timeout: int = 30,
        memory_limit: str = "512m",
        cpu_limit: float = 1.0,
        network_enabled: bool = False,
        image: str = "python:3.11-slim",
    ):
        super().__init__(timeout, memory_limit, cpu_limit, network_enabled)
        self.image = image

        # Initialize Docker client
        try:
            self.client = docker.from_env()
            # Pull image if not available
            try:
                self.client.images.get(self.image)
            except docker.errors.ImageNotFound:
                logger.info(f"Pulling Docker image: {self.image}")
                self.client.images.pull(self.image)
        except Exception as e:
            logger.error(f"Failed to initialize Docker client: {e}")
            self.client = None

    def execute(
        self, code: str, language: str = "python", context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Execute code in a Docker container.

        Args:
            code: Code to execute
            language: Programming language (python, javascript, etc.)
            context: Execution context

        Returns:
            Execution results
        """
        if not self.client:
            return {
                "status": ExecutionStatus.ERROR,
                "output": "",
                "error": "Docker client not available",
                "execution_time": 0.0,
                "memory_used": 0.0,
            }

        start_time = time.time()

        try:
            # Create temporary file with code
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=f".{self._get_file_extension(language)}", delete=False
            ) as f:
                f.write(code)
                temp_file = f.name

            # Prepare Docker run command
            command = self._get_run_command(language, os.path.basename(temp_file))

            # Run container
            container = self.client.containers.run(
                self.image,
                command=command,
                volumes={os.path.dirname(temp_file): {"bind": "/workspace", "mode": "ro"}},
                working_dir="/workspace",
                mem_limit=self.memory_limit,
                nano_cpus=int(self.cpu_limit * 1e9),
                network_disabled=not self.network_enabled,
                detach=True,
                remove=False,  # We'll remove manually after getting stats
            )

            # Wait for completion or timeout
            try:
                result = container.wait(timeout=self.timeout)
                exit_code = result["StatusCode"]

                # Get logs
                output = container.logs().decode("utf-8")

                # Get stats
                stats = container.stats(stream=False)
                memory_used = stats["memory_stats"].get("usage", 0) / (1024 * 1024)  # MB

                execution_time = time.time() - start_time

                # Determine status
                if exit_code == 0:
                    status = ExecutionStatus.SUCCESS
                    error = None
                else:
                    status = ExecutionStatus.ERROR
                    error = output

                result = {
                    "status": status,
                    "output": output if exit_code == 0 else "",
                    "error": error,
                    "execution_time": execution_time,
                    "memory_used": memory_used,
                    "exit_code": exit_code,
                }

            except Exception as e:
                # Timeout or other error
                container.kill()
                result = {
                    "status": ExecutionStatus.TIMEOUT,
                    "output": "",
                    "error": f"Execution timeout or error: {str(e)}",
                    "execution_time": time.time() - start_time,
                    "memory_used": 0.0,
                }

            finally:
                # Clean up container
                try:
                    container.remove(force=True)
                except Exception:
                    pass

                # Clean up temp file
                try:
                    os.unlink(temp_file)
                except Exception:
                    pass

            return result

        except Exception as e:
            logger.error(f"Docker execution error: {e}")
            return {
                "status": ExecutionStatus.ERROR,
                "output": "",
                "error": str(e),
                "execution_time": time.time() - start_time,
                "memory_used": 0.0,
            }

    def _get_file_extension(self, language: str) -> str:
        """Get file extension for language."""
        extensions = {
            "python": "py",
            "javascript": "js",
            "ruby": "rb",
            "go": "go",
            "rust": "rs",
        }
        return extensions.get(language.lower(), "txt")

    def _get_run_command(self, language: str, filename: str) -> str:
        """Get command to run code in container."""
        commands = {
            "python": f"python {filename}",
            "javascript": f"node {filename}",
            "ruby": f"ruby {filename}",
            "go": f"go run {filename}",
        }
        return commands.get(language.lower(), f"cat {filename}")

    def cleanup(self):
        """Clean up Docker resources."""
        if self.client:
            # Remove any dangling containers from this sandbox
            try:
                containers = self.client.containers.list(all=True, filters={"status": "exited"})
                for container in containers:
                    try:
                        container.remove()
                    except Exception:
                        pass
            except Exception as e:
                logger.error(f"Cleanup error: {e}")


class InProcessSandbox(SandboxExecutor):
    """
    Lightweight in-process sandbox for testing.
    WARNING: Not as secure as Docker. Use only for development/testing.
    """

    def execute(
        self, code: str, language: str = "python", context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Execute code in-process with restricted globals."""
        if language != "python":
            return {
                "status": ExecutionStatus.ERROR,
                "output": "",
                "error": f"Language {language} not supported in in-process sandbox",
                "execution_time": 0.0,
                "memory_used": 0.0,
            }

        start_time = time.time()

        try:
            # Restricted globals - no imports, no file access, etc.
            safe_globals = {
                "__builtins__": {
                    "print": print,
                    "len": len,
                    "range": range,
                    "str": str,
                    "int": int,
                    "float": float,
                    "bool": bool,
                    "list": list,
                    "dict": dict,
                    "tuple": tuple,
                    "set": set,
                },
                "context": context or {},
            }

            # Capture output
            from io import StringIO
            import sys

            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()

            try:
                exec(code, safe_globals)
                output = captured_output.getvalue()
                status = ExecutionStatus.SUCCESS
                error = None
            finally:
                sys.stdout = old_stdout

            execution_time = time.time() - start_time

            return {
                "status": status,
                "output": output,
                "error": error,
                "execution_time": execution_time,
                "memory_used": 0.0,  # Not measured in in-process
            }

        except Exception as e:
            execution_time = time.time() - start_time
            return {
                "status": ExecutionStatus.ERROR,
                "output": "",
                "error": str(e),
                "execution_time": execution_time,
                "memory_used": 0.0,
            }

    def cleanup(self):
        """No cleanup needed for in-process execution."""
        pass
