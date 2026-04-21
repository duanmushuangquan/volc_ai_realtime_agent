"""Integration tests for hello module."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "python"))

from hello import greet, farewell


def test_integration_greet():
    """Integration test for greet."""
    result = greet("IntegrationTest")
    assert "Hello" in result
    assert "IntegrationTest" in result


def test_integration_farewell():
    """Integration test for farewell."""
    result = farewell("IntegrationTest")
    assert "Goodbye" in result
    assert "IntegrationTest" in result
