from datetime import datetime
import logging
import os

from ..Core.signal import Signal


class Logger(logging.Logger):

    new_log: Signal = Signal()
    new_debug: Signal = Signal()
    new_info: Signal = Signal()
    new_warning: Signal = Signal()
    new_error: Signal = Signal()
    new_critical: Signal = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._file_path = []
        self._stream_handler = None
        self._formatter = None

    def _get_record(self, txt, level):
        return logging.LogRecord(name=self.name, level=level, pathname=__file__,
                                 lineno=42, msg=txt, args=(), exc_info=None)
    
    def _format(self, record):
        return f"{self._formatter.format(record)}\n"

    def debug(self, txt):
        record = self._get_record(txt, logging.DEBUG)
        formated_txt = self._format(record)

        self.new_log.emit(formated_txt)
        self.new_debug.emit(formated_txt)

        return super().debug(txt)
    
    def info(self, txt):
        record = self._get_record(txt, logging.INFO)
        formated_txt = self._format(record)

        self.new_log.emit(formated_txt)
        self.new_info.emit(formated_txt)

        return super().info(txt)
    
    def warning(self, txt):
        record = self._get_record(txt, logging.WARNING)
        formated_txt = self._format(record)

        self.new_log.emit(formated_txt)
        self.new_warning.emit(formated_txt)

        return super().warning(txt)
    
    def error(self, txt):
        record = self._get_record(txt, logging.ERROR)
        formated_txt = self._format(record)
    
        self.new_log.emit(formated_txt)
        self.new_error.emit(formated_txt)

        return super().error(txt)
    
    def critical(self, txt):
        record = self._get_record(txt, logging.CRITICAL)
        formated_txt = self._format(record)

        self.new_log.emit(formated_txt)
        self.new_critical.emit(formated_txt)

        return super().critical(txt)
    
    def add_log_file(self, file_path):
        file_handler = logging.FileHandler(log_file_path)
        if self._formatter:
            file_handler.setFormatter(self._formatter)
        file_handler.setLevel(logging.DEBUG)

        self.addHandler(file_handler)
        self._file_path.append(file_path)

    def set_formater(self, formatter_str: str):
        self._formatter = logging.Formatter(formatter_str)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        self.addHandler(stream_handler)

        for handler in self.handlers:
            handler.setFormatter(self._formatter)
    
    def setLevel(self, level: int):
        for handler in self.handlers:
            handler.setLevel(level)

        return super().setLevel(level)


_logger_name = "MotionBuilder"
mb_logger = Logger(_logger_name)

# formatter
_formatter_str = f"[{mb_logger.name} %(levelname)s] - "
_formatter_str += "[%(asctime)s] - [%(module)s.%(funcName)s, ln.%(lineno)d] -> %(message)s"

# log file
module_dir = os.path.dirname(os.path.realpath(__file__))
_log_directory = os.path.normpath(os.path.join(module_dir, "../logs"))
if not os.path.exists(_log_directory):
    os.mkdir(_log_directory)
_date = datetime.now().strftime("%d_%m_%Y_%Hh_%Mmin")
log_file_path = os.path.normpath(os.path.join(_log_directory, f"{_logger_name}_{_date}.log"))

# Set logger
mb_logger.set_formater(_formatter_str)
mb_logger.add_log_file(log_file_path)
mb_logger.setLevel(logging.DEBUG)
