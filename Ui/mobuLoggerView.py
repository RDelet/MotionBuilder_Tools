from datetime import datetime
import os
import logging
import sys
import tempfile
from typing import Optional

from PySide2.QtCore import Qt
from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget

from ..Core.logger import mb_logger, log_formatter
from ..Core.stdOutputWriter import STDOutputWriter
from ..Core.signal import Signal
from ..Ui import qtUtils
from ..Ui.loggerHighLigther import LoggerHighLigther


class RequestsHandler(logging.Handler):

    newLog: Signal = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def emit(self, record):
        self.newLog.emit(f"{log_formatter.format(record)}\n")


class MobuLoggerView(QMainWindow):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(qtUtils.get_main_window() if not parent else parent)

        self._populate()
        self._writer = self._create_writer()
        self._writer.textAdded.register(self.append)

        request_handler = RequestsHandler()
        mb_logger.addHandler(request_handler)
        request_handler.newLog.register(self.append)

        self.show()

    def _populate(self):
        self.setWindowTitle("MotionBuilder Logger View")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.bloc_text = QTextEdit()
        self.bloc_text.setLineWrapMode(QTextEdit.NoWrap)
        self.bloc_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.bloc_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.bloc_text.setReadOnly(True)

        self.layout.addWidget(self.bloc_text)
        self.high_ligther = LoggerHighLigther(self.bloc_text.document())

    def _create_writer(self) -> STDOutputWriter:
        writer = STDOutputWriter(self._get_log_file_path())
        sys.stdout = writer
        sys.stderr = writer

        return writer

    @staticmethod
    def _get_log_file_path() -> str:
        tmp_dir = tempfile.gettempdir()
        date = datetime.now().strftime("%d_%m_%Y_%Hh_%Mmin")

        return os.path.join(tmp_dir, "QD_MOBU_LOG", f"MobuLogs_{date}.rde")

    def append(self, txt: str):
        current_text = self.bloc_text.toPlainText()
        self.bloc_text.setPlainText(f"{current_text}{txt}" if current_text else txt)

    def closeEvent(self, event: QCloseEvent):
        event.ignore()
