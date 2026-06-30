#!/usr/bin/env python3
import argparse
import csv
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, TextIO

from rich.console import Console
from rich.table import Table


@dataclass
class Review:
    timestamp: int
    spelling: str
    reading: str
    grade: str


def parse_reviews(data: dict[str, Any]) -> list[Review]:
    rows: list[Review] = []
    for card in data["cards_vocabulary_jp_en"]:
        spelling = card["spelling"]
        reading = card["reading"]
        for review in card["reviews"]:
            rows.append(
                Review(
                    timestamp=review["timestamp"],
                    spelling=spelling,
                    reading=reading,
                    grade=review["grade"],
                )
            )
    return rows


def print_reviews(reviews: list[Review], out: TextIO = sys.stdout) -> None:
    table = Table()
    table.add_column("Timestamp")
    table.add_column("Spelling")
    table.add_column("Reading")
    table.add_column("Grade")

    for review in reviews:
        dt = datetime.fromtimestamp(review.timestamp, tz=timezone.utc).astimezone()
        table.add_row(
            dt.strftime("%Y-%m-%d %H:%M:%S %Z"),
            review.spelling,
            review.reading,
            review.grade,
        )

    Console(file=out).print(table)


def print_reviews_csv(reviews: list[Review], out: TextIO = sys.stdout) -> None:
    writer = csv.writer(out)
    writer.writerow(["Timestamp", "Spelling", "Reading", "Grade"])

    for review in reviews:
        dt = datetime.fromtimestamp(review.timestamp, tz=timezone.utc).astimezone()
        writer.writerow(
            [
                dt.strftime("%Y-%m-%d %H:%M:%S %Z"),
                review.spelling,
                review.reading,
                review.grade,
            ]
        )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print jpdb review history.")
    parser.add_argument(
        "file",
        nargs="?",
        default=None,
        help="reviews.json file to process (defaults to stdin)",
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        help="print output as CSV instead of a table",
    )
    limit_group = parser.add_mutually_exclusive_group()
    limit_group.add_argument(
        "--head",
        type=int,
        metavar="N",
        help="show only the N oldest reviews",
    )
    limit_group.add_argument(
        "--tail",
        type=int,
        metavar="N",
        help="show only the N most recent reviews",
    )
    args = parser.parse_args(argv)
    if args.file is None and sys.stdin.isatty():
        parser.error("no file given and no input piped on stdin")
    return args


def main() -> None:
    args = parse_args()

    if args.file is None:
        data = json.load(sys.stdin)
    else:
        with open(args.file) as f:
            data = json.load(f)

    reviews = sorted(parse_reviews(data), key=lambda r: r.timestamp)
    if args.head is not None:
        reviews = reviews[: args.head]
    elif args.tail is not None:
        reviews = reviews[-args.tail :] if args.tail > 0 else []

    if args.csv:
        print_reviews_csv(reviews)
    else:
        print_reviews(reviews)


if __name__ == "__main__":
    main()
