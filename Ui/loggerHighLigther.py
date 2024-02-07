import re

from PySide2.QtGui import QColor, QSyntaxHighlighter, QTextDocument, QTextCharFormat


class LoggerHighLigther(QSyntaxHighlighter):

    __kColorWhite = QColor(200, 200, 200)
    __kColorError = QColor(255, 125, 160)
    __kColorCritical = QColor(255, 75, 160)
    __kColorWarning = QColor(255, 130, 20)
    __kColorDebug = QColor(35, 170, 30)
    __kColorInfo = QColor(180, 180, 225)

    __kRegError = re.compile(r'[Ee][Rr][Rr][Oo][Rr]')
    __kRegCritical = re.compile(r'[Cc][Rr][Ii][Tt][Ii][Cc][Aa][Ll]')
    __kRegWarning = re.compile(r'[Ww][Aa][Rr][Nn][Ii][Nn][Gg]')
    __kRegDebug = re.compile(r'[De][Ee][Bb][Uu][Gg]')
    __kRegInfo = re.compile(r'[Ii][Nn][Fo][Oo]')

    def __init__(self, parent: QTextDocument):
        super().__init__(parent)
        self.parent = parent

    def highlightBlock(self, txt: str):
        keyword = QTextCharFormat()

        if self.__kRegError.findall(txt):
            keyword.setForeground(self.__kColorError)
        elif self.__kRegCritical.findall(txt):
            keyword.setForeground(self.__kColorCritical)
        elif self.__kRegWarning.findall(txt):
            keyword.setForeground(self.__kColorWarning)
        elif self.__kRegDebug.findall(txt):
            keyword.setForeground(self.__kColorDebug)
        elif self.__kRegInfo.findall(txt):
            keyword.setForeground(self.__kColorInfo)
        else:
            keyword.setForeground(self.__kColorWhite)

        self.setFormat(0, len(txt), keyword)
        self.setCurrentBlockState(0)
