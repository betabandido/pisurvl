import signal

from pisurvl.app import Application
from pisurvl.exectools.exectools import terminate_execution


def signal_handler(signal_number, stack_frame):
    """Handles termination signal by daemon runner.

    Args:
        signal_number: The signal number.
        stack_frame: The stack frame.
    """
    if signal_number in [signal.SIGTERM, signal.SIGINT]:
        terminate_execution()


def main():
    signal.signal(signal.SIGINT, signal_handler)
    Application().start()

if __name__ == '__main__':
    main()
