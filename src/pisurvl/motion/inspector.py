from abc import ABCMeta, abstractmethod
from PIL import Image


class Inspector(metaclass=ABCMeta):
    @abstractmethod
    def dump(self, frame, step):
        pass


class DummyInspector(Inspector):
    def dump(self, frame, step):
        pass


class BasicInspector(Inspector):
    generators = {}

    def generate_filename(self, step):
        if step not in self.generators:
            self.generators[step] = self._index_generator()
        gen = self.generators[step]
        return 'img-{}-{}.jpg'.format(step, next(gen))

    def dump(self, frame, step):
        img = Image.fromarray(frame, 'L')
        img.save(self.generate_filename(step))

    @staticmethod
    def _index_generator():
        i = 0
        while True:
            yield i
            i += 1
