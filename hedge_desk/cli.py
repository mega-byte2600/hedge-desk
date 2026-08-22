"""Command-line entry point for the frozen paper-only vertical slice."""

import argparse
import json

from hedge_desk.demo import run_reference_demo


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--approve",
        action="store_true",
        help="simulate an explicit human approval for this frozen paper fixture",
    )
    parser.add_argument(
        "--human-id",
        default="",
        help="required human identity when --approve is supplied",
    )
    args = parser.parse_args()
    if args.approve and not args.human_id.strip():
        parser.error("--human-id is required with --approve")
    print(json.dumps(run_reference_demo(args.approve, args.human_id), indent=2))


if __name__ == "__main__":
    main()
