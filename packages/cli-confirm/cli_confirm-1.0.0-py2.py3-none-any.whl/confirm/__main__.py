"""Entry point."""

import click


@click.command()
@click.argument("text")
def main(text):
    # type: (str) -> None
    """Entry point."""
    if not click.confirm(text):
        exit(1)


if __name__ == "__main__":
    main()
