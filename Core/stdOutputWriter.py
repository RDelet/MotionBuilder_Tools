import os

from ..Core.signal import Signal


class STDOutputWriter:

    textAdded: Signal = Signal()

    def __init__(self, std, file_path: str):
        self._old_std = std
        self._file_path = file_path
        self.__check_path()
    
    def __check_path(self):
        if "." not in self._file_path:
            raise RuntimeError("Path must be a file !")

        file_directory, _ = os.path.split(self._file_path)
        if not os.path.exists(file_directory):
            os.mkdir(file_directory)

    @property
    def old_std(self):
        return self._old_std

    def write(self, txt: str):
        self.textAdded.emit(txt)
        self._old_std.write(txt)

    def flush(self):
        with open(self._file_path, "a") as file_handler:
            file_handler.flush()
