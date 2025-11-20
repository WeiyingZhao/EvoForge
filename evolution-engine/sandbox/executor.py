"""
Base executor interface for sandboxed code execution.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from enum import Enum


class ExecutionStatus(Enum):
    """Execution status codes."""

    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    MEMORY_LIMIT = "memory_limit"
    SECURITY_VIOLATION = "security_violation"


class SandboxExecutor(ABC):
    """
    Abstract base class for sandbox executors.

    Safety features:
    - Resource limits (CPU, memory, time)
    - Network isolation
    - Filesystem restrictions
    - Automatic cleanup
    """

    def __init__(
        self,
        timeout: int = 30,
        memory_limit: str = "512m",
        cpu_limit: float = 1.0,
        network_enabled: bool = False,
    ):
        """
        Initialize sandbox executor.

        Args:
            timeout: Maximum execution time in seconds
            memory_limit: Memory limit (e.g., "512m", "1g")
            cpu_limit: CPU cores (e.g., 1.0 = 1 core)
            network_enabled: Whether to allow network access
        """
        self.timeout = timeout
        self.memory_limit = memory_limit
        self.cpu_limit = cpu_limit
        self.network_enabled = network_enabled

    @abstractmethod
    def execute(
        self, code: str, language: str = "python", context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Execute code in sandbox.

        Args:
            code: Code to execute
            language: Programming language
            context: Optional execution context (variables, imports, etc.)

        Returns:
            {
                "status": ExecutionStatus,
                "output": str,
                "error": str | None,
                "execution_time": float,
                "memory_used": float
            }
        """
        pass

    @abstractmethod
    def cleanup(self):
        """Clean up sandbox resources."""
        pass
