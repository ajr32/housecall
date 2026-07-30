"""
Diagnostic framework for HouseCall.
"""


class Diagnostic:
    """Represents the result of a single diagnostic check."""

    def __init__(self, name: str, passed: bool, message: str = ""):
        self.name = name
        self.passed = passed
        self.message = message


class DiagnosticRunner:
    """Collects diagnostic results."""

    def __init__(self):
        self.results = []

    def add(self, diagnostic: Diagnostic):
        """Add a completed diagnostic."""
        self.results.append(diagnostic)

    @property
    def success(self) -> bool:
        """Return True if every diagnostic passed."""
        return all(result.passed for result in self.results)