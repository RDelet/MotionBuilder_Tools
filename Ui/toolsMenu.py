import traceback

from pyfbsdk import FBMenuManager

from ..Core.logger import mb_logger


def _show_logger_cb(*args, **kwargs):
    try:
        from .mobuLoggerView import MobuLoggerView
        logger_instance = MobuLoggerView.instance()
        if logger_instance:
            logger_instance.show()
    except Exception as e:
        mb_logger.error(e)
        mb_logger.debug(traceback.format_exc())


def _open_reference_ui(*args, **kwargs):
    try:
        from .referenceEditorUI import ReferenceEditorUI
        ReferenceEditorUI().show()
    except Exception as e:
        mb_logger.error(e)
        mb_logger.debug(traceback.format_exc())


def create():
    try:
        menu_name = "MB Tools"

        menu_mgr = FBMenuManager()
        menu_mgr.InsertLast(None, menu_name)
        new_menu = menu_mgr.GetMenu(menu_name)

        new_menu.InsertFirst("Show Log", 1)
        new_menu.OnMenuActivate.Add(_show_logger_cb)

        new_menu.InsertFirst("Reference Editor", 2)
        new_menu.OnMenuActivate.Add(_open_reference_ui)
    except Exception as e:
        mb_logger.error(e)
        mb_logger.debug(traceback.format_exc()) 
