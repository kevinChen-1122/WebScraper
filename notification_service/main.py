from module import logger_module, mongo_module, line_notify_module
from datetime import datetime
import json
import pymongo


def main():
    try:
        line_notify_module.send_line_notify()
    except Exception as e:
        new_log = logger_module.get_logger()
        new_log.error(f"Error processing : {e}")


if __name__ == "__main__":
    main()
