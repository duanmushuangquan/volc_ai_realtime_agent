"""Unit tests for hello module."""

import pytest
from src.python.hello import greet, farewell


class TestGreeter:
    """Test cases for Greeter functions."""

    def test_greet_default(self):
        """Test greet with default name."""
        assert greet() == "Hello, World!"

    def test_greet_custom(self):
        """Test greet with custom name."""
        assert greet("Alice") == "Hello, Alice!"

    def test_farewell_default(self):
        """Test farewell with default name."""
        assert farewell() == "Goodbye, World!"

    def test_farewell_custom(self):
        """Test farewell with custom name."""
        assert farewell("Bob") == "Goodbye, Bob!"
