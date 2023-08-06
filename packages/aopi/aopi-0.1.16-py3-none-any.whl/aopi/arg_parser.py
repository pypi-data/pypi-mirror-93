import argparse
from enum import Enum
from pathlib import Path

from argparse_utils import enum_action


class LogLevel(str, Enum):
    info = "INFO"
    debug = "DEBUG"
    error = "ERROR"
    notset = "NOTSET"
    warning = "WARNING"
    critical = "CRITICAL"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, dest="host", help="Application host")
    parser.add_argument("--port", type=int, dest="port", help="Application port")
    parser.add_argument(
        "-r",
        "--reload",
        action="store_true",
        dest="reload",
        help="Reload application on change (Development only)",
    )
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        dest="workers_count",
        help="Number of application processes. (Only for Gunicorn workers)",
    )
    parser.add_argument(
        "--pid-file",
        type=str,
        dest="pid_file",
        help="Path to file where to store "
        "server application ID. (Only for Gunicorn workers)",
    )
    parser.add_argument(
        "-d", "--database", type=str, dest="aopi_db_url", help="Database file"
    )
    parser.add_argument(
        "-p",
        "--packages-dir",
        type=str,
        dest="packages_dir",
        help="Path to folder where to store actual simple",
    )
    parser.add_argument(
        "--log-level",
        action=enum_action(LogLevel, str.lower),
        dest="log_level",
        help="Logging level for application",
    )
    parser.add_argument(
        "-n",
        "--no-ui",
        action="store_true",
        dest="no_ui",
        help="Turn off aopi web-interface",
    )
    parser.add_argument(
        "-u" "--users",
        action="store_true",
        dest="enable_users",
        help="Enable user system",
    )
    parser.add_argument(
        "--secret-file",
        type=Path,
        dest="secret_file",
        help="Path to file where secret stored",
    )
    return parser.parse_args()
