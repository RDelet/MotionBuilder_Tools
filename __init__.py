import traceback

from .Core.logger import mb_logger


try:
    from .Ui.mobuLoggerView import MobuLoggerView
    MobuLoggerView()
except Exception as e:
    mb_logger.error(e)
    mb_logger.debug(traceback.format_exc())


try:
    from .Ui.toolsMenu import ToolsMenu
    ToolsMenu().create()
except Exception as e:
    mb_logger.error(e)
    mb_logger.debug(traceback.format_exc())
