import argparse

from .subcmd import single, batch, docker
from .log import logger, configure_logger


def configure_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--verbose",
        "-v",
        dest="verbosity",
        action="count",
        default=0,
        help="Verbosity level",
    )


def run():
    parser = argparse.ArgumentParser(
        "release-check",
        description="Check releases on Github",
    )
    configure_parser(parser)

    subparsers = parser.add_subparsers(dest="mode", required=True)

    single_parser = subparsers.add_parser(
        "single",
        help="Fetch information about most recent version of a single repository.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    single.configure_parser(single_parser)

    batch_parser = subparsers.add_parser(
        "batch",
        help="Fetch information about most recent versions of multiple repositories.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    batch.configure_parser(batch_parser)

    docker_parser = subparsers.add_parser(
        "docker",
        help="Fetch information about docker containers and compare their versions with latest versions received from upstream.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    docker.configure_parser(docker_parser)

    args = parser.parse_args()
    configure_logger(logger, args.verbosity)

    if args.mode == "single":
        single.main(args)
    elif args.mode == "batch":
        batch.main(args)
    elif args.mode == "docker":
        docker.main(args)


if __name__ == "__main__":
    run()