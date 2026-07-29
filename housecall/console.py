"""
Console output helpers.
"""


def header(title):
    print()
    print(title)
    print("=" * len(title))


def section(title):
    print()
    print(title)
    print("-" * len(title))


def success(message):
    print(f"✅ {message}")


def warning(message):
    print(f"⚠ {message}")


def info(message):
    print(f"ℹ {message}")