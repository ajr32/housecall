from housecall.commands import run_housekeeping


def test_housekeeping_success(capsys):
    run_housekeeping()

    output = capsys.readouterr().out

    assert "HouseCall Housekeeping" in output
    assert "Summary" in output
    assert "Checks run :" in output
    assert "Passed     :" in output
    assert "Failed     :" in output


def test_housekeeping_verbose(capsys):
    run_housekeeping(verbose=True)

    output = capsys.readouterr().out

    assert "Verbose mode enabled." in output
    assert "Running DisabledEntitiesHealthCheck..." in output
    assert "Running OrphanedEntitiesHealthCheck..." in output
