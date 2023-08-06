"""Console script for fluffy_id."""
import sys
import click

from fluffy_id import gen_guid


@click.command()
@click.argument("num", default=1, required=False, )
@click.option("--shard-id", default=1, required=False)
def main(num, shard_id):
    """Console script for fluffy_id."""
    for _ in range(num):
        click.echo(gen_guid(shard_id))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
