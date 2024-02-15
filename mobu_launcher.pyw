import logging
import os
import sys
import subprocess
import traceback


module_dir = os.path.dirname(os.path.realpath(__file__))
autodesk_directory = r"C:/Program Files/Autodesk"
mobu_exec_path = r"bin/x64/motionbuilder.exe"
mobu_version = 2022
mobu_path = os.path.normpath(os.path.join(autodesk_directory, f"MotionBuilder {mobu_version}", mobu_exec_path))


## LOGGER
log_file_path = os.path.normpath(os.path.join(module_dir, "mobu_launcher.log"))
if os.path.exists(log_file_path):
    os.remove(log_file_path)

file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)

logger = logging.getLogger("Mobu Launcher")
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)


def main(*args, **kwargs):
    command = list()

    logger.info("Setup subprocess command.")
    command.append(mobu_path)
    command.append(os.path.normpath(os.path.join(module_dir, "usersetup.py")))

    logger.info("Launch subprocess.")
    proc = subprocess.Popen(command, shell=True)
    stdout, stderr = proc.communicate()
    exit_status = proc.returncode

    return stdout, stderr, exit_status
    

if __name__ == "__main__":
    try:
        logger.info("Launch main process.")
        sys.exit(main(sys.argv[1:]))
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
