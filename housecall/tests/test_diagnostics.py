from housecall.diagnostics import Diagnostic, DiagnosticRunner


def test_runner_starts_empty():
    runner = DiagnosticRunner()

    assert runner.results == []
    assert runner.passed == 0
    assert runner.failed == 0
    assert runner.success is True


def test_add_passing_result():
    runner = DiagnosticRunner()

    runner.add(
        Diagnostic(
            "Configuration",
            True,
            "OK",
        )
    )

    assert runner.passed == 1
    assert runner.failed == 0
    assert runner.success is True


def test_add_failed_result():
    runner = DiagnosticRunner()

    runner.add(
        Diagnostic(
            "Configuration",
            False,
            "Boom",
        )
    )

    assert runner.passed == 0
    assert runner.failed == 1
    assert runner.success is False


def test_runner_counts_multiple():
    runner = DiagnosticRunner()

    runner.add(Diagnostic("A", True, "OK"))
    runner.add(Diagnostic("B", False, "Bad"))
    runner.add(Diagnostic("C", True, "OK"))

    assert len(runner.results) == 3
    assert runner.passed == 2
    assert runner.failed == 1
    assert runner.success is False
