from housecall.commands import run_doctor


def test_doctor_success(capsys):
    run_doctor()

    output = capsys.readouterr().out

    assert "HouseCall Health Report" in output
    assert "Summary" in output
    assert "Checks run :" in output
    assert "Passed     :" in output
    assert "Failed     :" in output


def test_doctor_verbose(capsys):
    run_doctor(verbose=True)

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
