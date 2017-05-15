from mockito import mock, when


class ChainedMockBuilder:
    def __init__(self):
        self.mock = mock(strict=True)
        self.end_mock = self.mock

    def add_call(self, name, *args, **kwargs):
        call_mock = mock(strict=True)
        getattr(when(self.end_mock), name)(*args, **kwargs) \
            .thenReturn(call_mock)
        self.end_mock = call_mock
        return self

    def end_call(self, name, return_value, *args, **kwargs):
        getattr(when(self.end_mock), name)(*args, **kwargs) \
            .thenReturn(return_value)
        return self.mock
