"""Helper functions."""

from datetime import datetime


def validate_date(date_str):
    """Validates str for format: %Y-%m-%d"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return False

    return True
