import sys
from typing import Optional

from PySide2.QtCore import Qt
from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget

from ..Core.stdOutputWriter import STDOutputWriter
from ..Core.logger import mb_logger, log_file_path
from ..Ui import qtUtils
from ..Ui.loggerHighLigther import LoggerHighLigther


class MobuLoggerView(QMainWindow):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(qtUtils.get_main_window() if not parent else parent)

        self._std_out_writer = STDOutputWriter(sys.stdout, log_file_path)
        self._std_out_writer.textAdded.register(self.append)
        self._std_err_writer = STDOutputWriter(sys.stderr, log_file_path)
        self._std_err_writer.textAdded.register(self.append)
        mb_logger.new_log.register(self.append)

        self._populate()
        self._redirect_std()
    
    @classmethod
    def instance(cls):
        return cls._instance

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
    
    def _redirect_std(self):
        sys.stdout = self._std_out_writer
        sys.stderr = self._std_err_writer

    def append(self, txt: str):
        current_text = self.bloc_text.toPlainText()
        self.bloc_text.setPlainText(f"{current_text}{txt}" if current_text else txt)

    def closeEvent(self, event: QCloseEvent):
        self.hide()
        event.ignore()
