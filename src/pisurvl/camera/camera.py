from abc import ABCMeta, abstractmethod


class Camera(metaclass=ABCMeta):
    @abstractmethod
    def __enter__(self):
        return self

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    def get_frame(self):
        """Returns a frame."""

    @abstractmethod
    def warm_up(self):
        """Waits for camera warmup."""
