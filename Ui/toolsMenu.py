"""!@Brief ToDo: Refacto to use json file for generate menu"""

import traceback

from pyfbsdk import FBMenuManager

from ..Core.logger import mb_logger


def _show_logger_cb():
    try:
        from .mobuLoggerView import MobuLoggerView
        logger_instance = MobuLoggerView.instance()
        if logger_instance:
            logger_instance.show()
    except Exception as e:
        mb_logger.error(e)
        mb_logger.debug(traceback.format_exc())


def _open_reference_ui():
    try:
        from .referenceEditorUI import ReferenceEditorUI
        ReferenceEditorUI().show()
    except Exception as e:
        mb_logger.error(e)
        mb_logger.debug(traceback.format_exc())


class ToolsMenu:

    def __init__(self):
        self._name = "MB Tools"
        self._manager = FBMenuManager()
        self._menu = None
        self._callbacks = {}

    def _menu_cb(self, control, event):
        func = self._callbacks.get(event.Id)
        if func:
            try:
                func()
            except Exception as e:
                mb_logger.error(e)
                mb_logger.debug(traceback.format_exc()) 

    def _add_item(self, name: str, func):
        menu_id = len(self._callbacks) + 1
        self._menu.InsertLast(name, menu_id)
        self._callbacks[menu_id] = func
    
    def create(self):
        try:
            self._manager.InsertLast(None, self._name)
            self._menu = self._manager.GetMenu(self._name)
            self._menu.OnMenuActivate.Add(self._menu_cb)

            self._add_item("Show Log", _show_logger_cb)
            self._add_item("Reference Editor", _open_reference_ui)
        except Exception as e:
            mb_logger.error(e)
            mb_logger.debug(traceback.format_exc()) 
