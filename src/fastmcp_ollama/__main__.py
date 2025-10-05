"""Main entry point for fastmcp-ollama."""

import sys
from .server import run_server


def main() -> None:
    """Main entry point."""
    try:
        run_server()
    except KeyboardInterrupt:
        print("\nShutting down fastmcp-ollama...")
        sys.exit(0)
    except Exception as e:
        print(f"Error running fastmcp-ollama: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
