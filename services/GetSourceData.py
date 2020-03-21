from pathlib import Path
from abc import ABC, abstractmethod

class AbstractGetSourceData(ABC):
    @abstractmethod
    def get_files(self, path, filename):
        pass


class GetSourceDataFiles(AbstractGetSourceData):
    def get_files(self, path, filename):
        certificate_files = Path(path).rglob(filename)
        return certificate_files