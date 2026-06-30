# jpdb-review-history

Flattens a [jpdb.io](https://jpdb.io) review history export into a single,
chronologically sorted list of reviews printed to stdout.

## Usage

Export your review history from jpdb.io (Settings -> Reviews -> Export
reviews) to get a `reviews.json` file, then run:

```sh
uv run main.py reviews.json
```

or pipe it in via stdin:

```sh
cat reviews.json | uv run main.py
```

Each line of output has the format:

```
2026-06-30 11:35:31 PDT  助ける  たすける  okay
```

## Install as a command

```sh
uv tool install .
jpdb-review-history reviews.json
```
