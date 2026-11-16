"""Small pure helpers shared by the Ekinly AI application."""

from html import escape


def escape_html_text(value: object) -> str:
    """Escape untrusted values before inserting them into HTML text nodes."""
    return escape(str(value), quote=True)
