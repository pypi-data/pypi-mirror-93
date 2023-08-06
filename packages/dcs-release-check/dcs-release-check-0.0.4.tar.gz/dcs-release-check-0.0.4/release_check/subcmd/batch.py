import argparse
import re
import toml
import json
from collections import namedtuple
from tabulate import tabulate

from ..utils import fetch_releases

Row = namedtuple("Row", ["repository", "latest_version", "updated", "host"])


def configure_parser(parser: argparse.ArgumentParser):
    parser.add_argument("--config", "-c", required=True, help="Configuration file")
    parser.add_argument(
        "--format", default="print", choices=["print", "json"], help="Output format"
    )


def main(args):
    cfg = toml.load(open(args.config))
    repos = cfg["repos"]["github"]
    latest_versions = []
    for repo, pattern in repos.items():
        gh_user, gh_project = repo.split("/")
        regex = None if pattern == "default" else re.compile(pattern)
        latest = fetch_releases(gh_user, gh_project, version_pattern=regex, n_min=1)[0]
        latest_versions.append(
            Row(
                host="github.com",
                repository=repo,
                latest_version=latest["version"],
                updated=latest["updated"].date().isoformat(),
            )
        )

    latest_versions.sort(key=lambda row: row.repository)
    if args.format == "print":
        print(tabulate(latest_versions, headers="keys"))
    elif args.format == "json":
        print(json.dumps([item._asdict() for item in latest_versions]))