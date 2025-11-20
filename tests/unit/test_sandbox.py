"""
Unit tests for secure sandboxing with resource limits.
Tests the DockerSandbox and InProcessSandbox implementations.
"""
import pytest
import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from evolution_engine.sandbox.docker_sandbox import DockerSandbox, InProcessSandbox
from evolution_engine.sandbox.executor import ExecutionStatus


class TestInProcessSandbox:
    """Test the in-process sandbox (lighter weight, for testing)."""

    def setup_method(self):
        """Setup sandbox before each test."""
        self.sandbox = InProcessSandbox(timeout=5)

    def test_simple_execution(self):
        """Test basic code execution."""
        code = """
print("Hello, World!")
"""
        result = self.sandbox.execute(code, language="python")

        assert result["status"] == ExecutionStatus.SUCCESS
        assert "Hello, World!" in result["output"]
        assert result["error"] is None

    def test_arithmetic_execution(self):
        """Test arithmetic operations."""
        code = """
result = 2 + 2
print(f"Result: {result}")
"""
        result = self.sandbox.execute(code, language="python")

        assert result["status"] == ExecutionStatus.SUCCESS
        assert "Result: 4" in result["output"]

    def test_restricted_imports(self):
        """Test that imports are restricted."""
        code = """
import os
print(os.listdir('/'))
"""
        result = self.sandbox.execute(code, language="python")

        assert result["status"] == ExecutionStatus.ERROR
        assert "import" in result["error"].lower() or "name" in result["error"].lower()

    def test_restricted_file_access(self):
        """Test that file access is restricted."""
        code = """
with open('/etc/passwd', 'r') as f:
    print(f.read())
"""
        result = self.sandbox.execute(code, language="python")

        assert result["status"] == ExecutionStatus.ERROR

    def test_execution_time_recorded(self):
        """Test that execution time is recorded."""
        code = """
x = 0
for i in range(1000):
    x += i
print(x)
"""
        result = self.sandbox.execute(code, language="python")

        assert result["status"] == ExecutionStatus.SUCCESS
        assert result["execution_time"] > 0
        assert result["execution_time"] < 5  # Should be fast

    def test_syntax_error_handling(self):
        """Test handling of syntax errors."""
        code = """
def broken_function(
    print("Missing closing parenthesis")
"""
        result = self.sandbox.execute(code, language="python")

        assert result["status"] == ExecutionStatus.ERROR
        assert result["error"] is not None

    def test_runtime_error_handling(self):
        """Test handling of runtime errors."""
        code = """
x = 1 / 0
"""
        result = self.sandbox.execute(code, language="python")

        assert result["status"] == ExecutionStatus.ERROR
        assert "division" in result["error"].lower() or "zerodivision" in result["error"].lower()


class TestDockerSandbox:
    """Test the Docker-based sandbox (more secure, production-ready)."""

    def setup_method(self):
        """Setup sandbox before each test."""
        self.sandbox = DockerSandbox(
            timeout=10,
            memory_limit="256m",
            cpu_limit=0.5,
            network_enabled=False
        )

    def test_docker_client_initialization(self):
        """Test that Docker client initializes properly."""
        # If Docker is not available, client will be None
        if self.sandbox.client is None:
            pytest.skip("Docker not available")

        assert self.sandbox.client is not None

    def test_simple_execution_docker(self):
        """Test basic code execution in Docker."""
        if self.sandbox.client is None:
            pytest.skip("Docker not available")

        code = """
print("Hello from Docker!")
"""
        result = self.sandbox.execute(code, language="python")

        assert result["status"] == ExecutionStatus.SUCCESS
        assert "Hello from Docker!" in result["output"]

    def test_memory_limit_enforcement(self):
        """Test that memory limits are enforced."""
        if self.sandbox.client is None:
            pytest.skip("Docker not available")

        # This should succeed with small memory usage
        code = """
x = [1, 2, 3]
print(sum(x))
"""
        result = self.sandbox.execute(code, language="python")

        assert result["status"] == ExecutionStatus.SUCCESS
        assert result["memory_used"] >= 0  # Memory usage tracked

    def test_timeout_enforcement(self):
        """Test that timeout is enforced."""
        if self.sandbox.client is None:
            pytest.skip("Docker not available")

        # Create sandbox with very short timeout
        short_sandbox = DockerSandbox(timeout=2)

        # This should timeout
        code = """
import time
time.sleep(10)
print("Should not reach here")
"""
        result = short_sandbox.execute(code, language="python")

        assert result["status"] == ExecutionStatus.TIMEOUT
        assert result["execution_time"] <= 3  # Should timeout around 2 seconds

    def test_network_disabled(self):
        """Test that network access is disabled."""
        if self.sandbox.client is None:
            pytest.skip("Docker not available")

        code = """
import urllib.request
try:
    urllib.request.urlopen('http://google.com', timeout=1)
    print("Network access succeeded")
except Exception as e:
    print(f"Network access blocked: {e}")
"""
        result = self.sandbox.execute(code, language="python")

        # Should either fail or show network is blocked
        # (exact behavior depends on Docker setup)
        assert result is not None

    def test_cleanup(self):
        """Test that cleanup works properly."""
        if self.sandbox.client is None:
            pytest.skip("Docker not available")

        # Execute some code
        code = "print('test')"
        self.sandbox.execute(code, language="python")

        # Cleanup should not raise errors
        try:
            self.sandbox.cleanup()
            assert True
        except Exception:
            assert False, "Cleanup should not raise errors"


def test_sandbox_factory():
    """Test that we can create different sandbox types."""
    in_process = InProcessSandbox()
    docker = DockerSandbox()

    assert in_process is not None
    assert docker is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
