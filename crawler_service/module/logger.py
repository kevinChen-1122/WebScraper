import logging
import os
from logging.handlers import RotatingFileHandler

# 設置日誌目錄和文件
log_directory = "log"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)
log_file = os.path.join(log_directory, "system.log")

# 創建一個日誌記錄器
logger = logging.getLogger("Crawler-Service")
# 設置日誌記錄級別，例如 DEBUG, INFO, WARNING, ERROR, CRITICAL
logger.setLevel(logging.INFO)

# 創建日誌紀錄格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 創建一個日誌處理器，用於寫入日誌文件
file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024 * 5, backupCount=5)
file_handler.setFormatter(formatter)

# 輸出到控制台
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# 將日誌處理器新增至記錄器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def get_logger():
    return logger