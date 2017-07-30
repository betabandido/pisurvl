from pisurvl.exectools.exectools import is_execution_terminated, terminate_execution


def test_exectools():
    assert not is_execution_terminated()
    terminate_execution()
    assert is_execution_terminated()
