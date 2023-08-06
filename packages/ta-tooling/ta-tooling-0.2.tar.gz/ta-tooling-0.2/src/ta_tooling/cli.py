"""Command line interface for ta-tooling."""
import click

import ta_tooling


@click.group()
def main():
    pass


@click.command(help="Group files from the same student together in a folder")
@click.argument(
    "source",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, readable=True, writable=True
    ),
    required=True,
)
@click.argument(
    "destination",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, readable=True, writable=True
    ),
    required=True,
)
def categorize(source, destination):
    click.echo("Categorizing files ...")
    ta_tooling.categorize(source, destination)


main.add_command(categorize)

if __name__ == "__main__":
    main()
