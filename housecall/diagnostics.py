"""
Diagnostic framework for HouseCall.
"""


class Diagnostic:
    def __init__(
            self,
            name: str,
            passed: bool,
            message: str = "",
            details: list[str] | None = None,
    ):
        self.name = name
        self.passed = passed
        self.message = message
        self.details = details or []


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

    @property
    def passed(self) -> int:
        """Number of successful diagnostics."""
        return sum(result.passed for result in self.results)

    @property
    def failed(self) -> int:
        """Number of failed diagnostics."""
        return sum(not result.passed for result in self.results)
