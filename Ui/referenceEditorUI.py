import os
from typing import Optional

from PySide2.QtWidgets import QMainWindow, QAction, QFileDialog, QListView, QToolBar, QWidget
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtCore import QSize

from pyfbsdk import FBFindObjectByFullName, FBSystem

from ..Ui import qtUtils


class FBXItem(QStandardItem):

    def __init__(self, reference):
        super().__init__(qtUtils.fbx_icon, reference.ReferenceFilePath)
        self.reference = reference


class ReferenceEditorUI(QMainWindow):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(qtUtils.get_main_window() if not parent else parent)

        self.setWindowTitle("Reference Editor")

        self.__add_toolbar()
        self.__add_view()
        self.__update_content()

    def __add_toolbar(self):

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

    def __add_view(self):
        self.list_view = QListView()
        self.list_view.setIconSize(QSize(30, 30))

        self.model = QStandardItemModel()
        self.list_view.setModel(self.model)

        self.setCentralWidget(self.list_view)

    def _import_reference(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import FBX file", ".", "FBX Files (*.fbx)")
        if file_path:
            print(file_path)
            _, file_name = os.path.split(file_path)
            reference_name = file_name.split(".")[0]
            FBSystem().Scene.NamespaceImport(f"_{reference_name}_", file_path, True )
            reference = FBFindObjectByFullName(f"FileReference::_{reference_name}_")
            if not reference:
                raise RuntimeError("Error on import reference !")
            self.__add_reference_itel(reference)

    def _reload_reference(self):
        pass

    def remove_reference(self):
        pass

    def __update_content(self):
        self.model.clear()
        pass

    def __add_reference_itel(self, reference):
        item = FBXItem(reference)
        self.model.appendRow(item)