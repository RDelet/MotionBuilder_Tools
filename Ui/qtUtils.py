import os
from typing import Optional

from PySide2 import QtWidgets
from PySide2.QtGui import QIcon


main_window = None


__module_path, _ = os.path.split(__file__)
icon_path = os.path.join(__module_path, "icons")

import_icon = QIcon(os.path.join(icon_path, "import.svg"))
reload_icon = QIcon(os.path.join(icon_path, "reload.svg"))
remove_icon = QIcon(os.path.join(icon_path, "remove.svg"))
fbx_icon = QIcon(os.path.join(icon_path, "fbx.svg"))


def get_main_window() -> Optional[QtWidgets.QWidget]:
    if main_window is not None:
        return main_window

    widget = QtWidgets.QApplication.activeWindow()
    if not widget:
        return

    parent = widget.parentWidget()
    if not parent:
        return widget

    while True:
        tmp = parent.parentWidget()
        if not tmp:
            break
        parent = tmp

    return parent


def info_msg(title: str, txt: str, info_txt: str = "",
             parent: Optional[QtWidgets.QWidget] = None) -> QtWidgets.QWidget:
    w = QtWidgets.QMessageBox(parent if parent else get_main_window())
    w.setIcon(QtWidgets.QMessageBox.Information)
    w.setWindowTitle(title)
    w.setText(txt)
    w.setInformativeText(info_txt)

    return w


def error_msg(title: str, txt: str, info_txt: str = "",
              parent: Optional[QtWidgets.QWidget] = None) -> QtWidgets.QWidget:
    w = QtWidgets.QMessageBox(parent if parent else get_main_window())
    w.setIcon(QtWidgets.QMessageBox.Critical)
    w.setWindowTitle(title)
    w.setText(txt)
    w.setInformativeText(info_txt)

    return w
