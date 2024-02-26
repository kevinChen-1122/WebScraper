from module import mongo_module, line_notify_module
from datetime import datetime


def main():
    try:
        line_notify_module.send_line_notify()
    except Exception as error:
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] - {error}")


if __name__ == "__main__":
    main()
