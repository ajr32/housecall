from housecall.commands import run_triage


def test_triage_success(capsys):
    run_triage()

    output = capsys.readouterr().out

    assert "HouseCall Health Report" in output
    assert "Summary" in output
    assert "Checks run :" in output
    assert "Passed     :" in output
    assert "Failed     :" in output


def test_triage_verbose(capsys):
    run_triage(verbose=True)

    output = capsys.readouterr().out

    assert "Verbose mode enabled." in output
    assert "Running ConfigurationHealthCheck..." in output
    assert "Running ConnectionHealthCheck..." in output


# class FakeHealthCheck:
#    def __init__(self, diagnostic):
#        self.diagnostic = diagnostic

#    def run(self):
#        return self.diagnostic


# checks = [
#    FakeHealthCheck(Diagnostic("One", True, "OK")),
#    FakeHealthCheck(Diagnostic("Two", False, "Boom")),
# ]
