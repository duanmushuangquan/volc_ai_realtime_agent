"""Hello World Python Module."""

__version__ = "0.1.0"


def greet(name: str = "World") -> str:
    """Return a greeting message."""
    return f"Hello, {name}!"


def farewell(name: str = "World") -> str:
    """Return a farewell message."""
    return f"Goodbye, {name}!"


if __name__ == "__main__":
    print(greet())
    print(farewell())
