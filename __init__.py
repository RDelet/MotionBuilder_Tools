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


def show_logger_cb(control, event):
    try:
        logger_instance = MobuLoggerView.instance()
        if logger_instance:
            logger_instance.show()
    except Exception as e:
        mb_logger.error(e)
        mb_logger.debug(traceback.format_exc())


try:
    menu_name = "Python Log"
    menu_mgr = FBMenuManager()

    menu_mgr.InsertLast(None, menu_name)
    pythonLogMenu = menu_mgr.GetMenu(menu_name)
    pythonLogMenu.InsertFirst("Show Console", 1)
    pythonLogMenu.OnMenuActivate.Add(show_logger_cb)
except Exception as e:
    mb_logger.error(e)
    mb_logger.debug(traceback.format_exc()) 

mb_logger.info("Start up message !")