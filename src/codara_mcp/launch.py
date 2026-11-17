"""Console-script launchers that apply ``~/.codara/config.toml`` before ``codara`` loads."""

import sys

from codara_mcp import config


def _load_config():
    try:
        return config.load()
    except config.ConfigError as exc:
        print(f"codara: {exc}", file=sys.stderr)
        sys.exit(2)


def server() -> None:
    cfg = _load_config()
    from codara_mcp.server import run

    run(cfg)


def cli() -> int:
    cfg = _load_config()
    from codara_mcp.cli import main

    return main(config=cfg)
