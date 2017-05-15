"""When set to True execution should stop."""
_terminated = False


def terminate_execution():
    """Terminates execution."""
    print('Terminating execution...')
    global _terminated
    _terminated = True


def is_execution_terminated():
    """Returns whether execution must be ended.

    Returns:
        True if execution must be ended; False otherwise.
    """
    return _terminated
