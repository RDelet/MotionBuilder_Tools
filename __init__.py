from functools import partial
import traceback

from pyfbsdk import FBMenuManager

from .Core.logger import mb_logger


try:
    from .Ui.mobuLoggerView import MobuLoggerView
    MobuLoggerView()
except Exception as e:
    mb_logger.error(e)
    mb_logger.debug(traceback.format_exc())


def _show_logger_cb(control, event):
    try:
        logger_instance = MobuLoggerView.instance()
        if logger_instance:
            logger_instance.show()
    except Exception as e:
        mb_logger.error(e)
        mb_logger.debug(traceback.format_exc())


def _open_reference_ui(control, event):
    try:
        from .Ui.referenceEditorUI import ReferenceEditorUI
        ReferenceEditorUI().show()
    except Exception as e:
        mb_logger.error(e)
        mb_logger.debug(traceback.format_exc())


try:
    menu_name = "MB Tools"

    menu_mgr = FBMenuManager()
    menu_mgr.InsertLast(None, menu_name)
    new_menu = menu_mgr.GetMenu(menu_name)

    new_menu.InsertFirst("Show Log", 1)
    new_menu.OnMenuActivate.Add(_show_logger_cb)

    new_menu.InsertLast("Reference Editor", 2)
    new_menu.OnMenuActivate.Add(_open_reference_ui)
except Exception as e:
    mb_logger.error(e)
    mb_logger.debug(traceback.format_exc()) 


mb_logger.info("Start up message !")