import argparse
from packaging import version as pversion
from tabulate import tabulate
import argparse
import logging
import docker
import re

from ..log import logger
from ..utils import fetch_releases


def configure_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--all",
        action="store_true",
        help="Query all known containers from Docker daemon. By default only running containers are queried.",
    )
    parser.add_argument(
        "--label-prefix",
        default="me.dotcs.monitor",
        help="Container label prefix",
    )
    parser.add_argument(
        "--label-app-name", default="app.name", help="Container label app name"
    )
    parser.add_argument(
        "--label-app-version", default="app.version", help="Container label app version"
    )
    parser.add_argument(
        "--label-app-version-pattern",
        default="app.version-pattern",
        help="Container label app version pattern",
    )
    parser.add_argument(
        "--label-app-repo-uri",
        default="app.repo-uri",
        help="Container label app repository URI",
    )


def _check_container_version(container, label_cfg):
    """
    Extract pre-defined label information from a given container and use
    release-check to retrieve latest version from upstream.
    """
    container_name = container.attrs["Name"][1:]
    name = container.attrs["Config"]["Labels"][label_cfg["app_name"]]
    uri = container.attrs["Config"]["Labels"][label_cfg["app_repo_uri"]]
    version = container.attrs["Config"]["Labels"][label_cfg["app_version"]]

    host, repo = uri.split(":")
    user, project = repo.split("/")

    try:
        version_pattern = container.attrs["Config"]["Labels"][
            label_cfg["app_version_pattern"]
        ]
    except KeyError:
        version_pattern = None

    logger.info(
        f"Container under test: {container_name} (app.name={name}, app.version={version}, app.repo-uri={uri}, app.version-pattern={version_pattern or 'default'})"
    )
    try:
        upstream_latest = fetch_releases(
            user, project, version_pattern=version_pattern
        )[0]["version"]
    except IndexError:
        upstream_latest = None

    if version is None or upstream_latest is None:
        update_available = None
    else:
        update_available = pversion.parse(version) < pversion.parse(upstream_latest)

    return {
        "app_name": name,
        "app_version": version,
        "container_name": container_name,
        "upstream_latest_version": upstream_latest,
        "update_available": update_available,
    }


def main(args: argparse.Namespace):
    client = docker.from_env()

    label_cfg = {
        "app_name": f"{args.label_prefix}/{args.label_app_name}",
        "app_version": f"{args.label_prefix}/{args.label_app_version}",
        "app_version_pattern": f"{args.label_prefix}/{args.label_app_version_pattern}",
        "app_repo_uri": f"{args.label_prefix}/{args.label_app_repo_uri}",
    }

    containers = client.containers.list(
        filters={"label": label_cfg["app_repo_uri"]},
        all=args.all,
    )
    results = []
    for container in containers:
        res = _check_container_version(container, label_cfg)
        results.append(
            [
                res["app_name"],
                res["container_name"],
                res["app_version"],
                res["upstream_latest_version"],
                "x" if res["update_available"] else None,
            ]
        )

    # Sort results
    results.sort(key=lambda row: row[0])

    print(
        tabulate(
            results,
            headers=[
                "Application",
                "Container name",
                "Installed version",
                "Available version",
                "Update available",
            ],
        )
    )