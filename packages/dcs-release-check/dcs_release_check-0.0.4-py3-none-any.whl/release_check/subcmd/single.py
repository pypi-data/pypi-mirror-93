import argparse
import re

from ..constants import DEFAULT_VERSION_PATTERN
from ..utils import fetch_releases


def configure_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "uri", help="Resource identifier, e.g. github.com:nextcloud/server"
    )
    parser.add_argument(
        "--pattern", default=DEFAULT_VERSION_PATTERN, help="Version regex pattern"
    )


def main(args):
    host, repo = args.uri.split(":")
    user, project = repo.split("/")
    versions = fetch_releases(user, project, version_pattern=args.pattern)
    latest_version = versions[0]
    print(latest_version["version"])