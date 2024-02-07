import traceback

from .Core.logger import mb_logger


def install_output_log():
    try:
        from .Ui.mobuLoggerView import MobuLoggerView
        MobuLoggerView()
    except Exception as e:
        mb_logger.error(e)
        mb_logger.debug(traceback.format_exc())


install_output_log()
mb_logger.info("Start up message !")