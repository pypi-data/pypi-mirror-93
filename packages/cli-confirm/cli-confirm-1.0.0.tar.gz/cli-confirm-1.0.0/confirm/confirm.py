"""Function to confirm yes/no."""

import click


def confirm(text):
    # type: (str) -> bool
    """Confirm yes/no."""
    return click.confirm(text)
