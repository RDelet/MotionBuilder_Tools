from datetime import datetime
import logging
import os
import sys


module_dir = os.path.dirname(os.path.realpath(__file__))

_logger_name = "MotionBuilder"
_log_directory = os.path.normpath(os.path.join(module_dir, "../logs"))
if not os.path.exists(_log_directory):
    os.mkdir(_log_directory)
_date = datetime.now().strftime("%d_%m_%Y_%Hh_%Mmin")
_log_file_path = os.path.normpath(os.path.join(_log_directory, f"{_logger_name}_{_date}.log"))

_log_formatter_str = f"[{_logger_name} %(levelname)s] - "
_log_formatter_str += "[%(asctime)s] - [%(module)s.%(funcName)s, ln.%(lineno)d] -> %(message)s"
log_formatter = logging.Formatter(_log_formatter_str)

_stream_handler = logging.StreamHandler(stream=sys.stdout)
_stream_handler.setFormatter(log_formatter)
_stream_handler.setLevel(logging.DEBUG)

_file_handler = logging.FileHandler(_log_file_path)
_file_handler.setFormatter(log_formatter)
_file_handler.setLevel(logging.DEBUG)

mb_logger = logging.getLogger(_logger_name)
mb_logger.setLevel(logging.DEBUG)
mb_logger.addHandler(_file_handler)
mb_logger.addHandler(_stream_handler)
