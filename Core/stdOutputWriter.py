import os

from ..Core.signal import Signal


class STDOutputWriter:

    textAdded: Signal = Signal()

    def __init__(self, file_path: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._file_path = file_path
        self.__check_path()

    def __check_path(self):
        if "." not in self._file_path:
            raise RuntimeError("Path must be a file !")

        file_directory, _ = os.path.split(self._file_path)
        if not os.path.exists(file_directory):
            os.mkdir(file_directory)

    def write(self, txt: str):
        with open(self._file_path, "a") as file_handler:
            file_handler.write(txt)
        self.textAdded.emit(txt)

    def flush(self):
        with open(self._file_path, "a") as file_handler:
            file_handler.flush()
