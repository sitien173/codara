"""Allow ``python -m codara_mcp`` to start the stdio MCP server."""

from codara_mcp.launch import server


def main() -> None:
    server()


if __name__ == "__main__":
    main()
