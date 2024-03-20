import os
from typing import Optional

from PySide2.QtWidgets import QMainWindow, QAction, QFileDialog, QListView, QToolBar, QWidget
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtCore import QSize

from pyfbsdk import FBFileReference

from ..Ui import qtUtils
from ..Core import reference


class FBXItem(QStandardItem):

    def __init__(self, reference: FBFileReference):
        super().__init__(qtUtils.fbx_icon, reference.ReferenceFilePath)
        self.reference = reference


class ReferenceEditorUI(QMainWindow):

    _singleton = None

    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            return super().__new__(cls, *args, **kwargs)
        return cls._singleton

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(qtUtils.get_main_window() if not parent else parent)
        self.setWindowTitle("Reference Editor")
        self._add_toolbar()
        self._add_view()
        self._update_content()

    def _check_singleton(self):
        if self.__singleton is not None:
            self.__singleton.close()
        self.__singleton = self
    
    def _selected_item(self) -> FBXItem:
        selected_index = self.list_view.currentIndex()
        return self.model.itemFromIndex(selected_index) if selected_index.isValid() else None

    def _add_toolbar(self):

        toolbar = QToolBar()

        load_action = QAction(qtUtils.import_icon, "Import reference", self)
        load_action.triggered.connect(self._import_reference)
        toolbar.addAction(load_action)

        update_action = QAction(qtUtils.reload_icon, "Reload reference", self)
        update_action.triggered.connect(self._reload_reference)
        toolbar.addAction(update_action)

        delete_action = QAction(qtUtils.remove_icon, "Remove reference", self)
        delete_action.triggered.connect(self.remove_reference)
        toolbar.addAction(delete_action)
    
        self.addToolBar(toolbar)

    def _add_view(self):
        self.list_view = QListView()
        self.list_view.setIconSize(QSize(30, 30))

        self.model = QStandardItemModel()
        self.list_view.setModel(self.model)

        self.setCentralWidget(self.list_view)

    def _import_reference(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import FBX file", ".", "FBX Files (*.fbx)")
        if not file_path:
            return

        ref = reference.load(file_path)
        self._add_item(ref)

    def _reload_reference(self):
        seleted_item = self._selected_item()
        if seleted_item:
            seleted_item.reference = reference.reload(seleted_item.reference)

    def remove_reference(self):
        seleted_item = self._selected_item()
        if seleted_item:
            reference.remove(seleted_item.reference)
        self.model.removeRow(seleted_item.index().row())

    def _update_content(self):
        self.model.clear()
        for ref in reference.get_all():
            self._add_item(ref)

    def _add_item(self, ref: FBFileReference):
        item = FBXItem(ref)
        self.model.appendRow(item)
