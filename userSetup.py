import os
import sys
import traceback


module_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.split(module_dir)[0])


from MotionBuilder_Tools.Core.logger import mb_logger


def install_output_log():
    try:
        from MotionBuilder_Tools.Ui.mobuLoggerView import MobuLoggerView
        MobuLoggerView()
    except Exception as e:
        mb_logger.error(e)
        mb_logger.debug(traceback.format_exc())


def startup_log():
    mb_logger.info("Start up message !")


install_output_log()
startup_log()