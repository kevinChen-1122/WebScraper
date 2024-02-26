import requests
import traceback
from . import mongo_module, get_config_module
from datetime import datetime


def send_line_notify():
    try:
        db = mongo_module.connect_to_mongodb()
        collection = db['line_notify_log']
        data_list = mongo_module.find_documents(collection, {"status": "PENDING"})

        if data_list:
            token = get_config_module.line_notify_token
            if not token:
                raise ValueError("Line Notify token is empty.")

            headers = {
                "Authorization": "Bearer " + token,
                "Content-Type": "application/x-www-form-urlencoded"
            }

            for data in data_list:
                payload = {
                    'message': data["content"],
                    'stickerPackageId': "",  # 加入貼圖
                    'stickerId': ""
                    # 可用的貼圖清單：https://developers.line.biz/en/docs/messaging-api/sticker-list/#sticker-definitions
                }
                response = requests.post("https://notify-api.line.me/api/notify?", headers=headers, params=payload)

                now = datetime.now()

                data["status"] = "REQUESTED"
                data["res_status_code"] = response.status_code
                data["res_headers"] = dict(response.headers)
                data["res_text"] = response.text
                data["res_json"] = response.json() if "application/json" in response.headers.get("content-type",
                                                                                                 "").lower() else None
                data["updated_at"] = now.strftime("%Y-%m-%d %H:%M:%S")
                mongo_module.update_documents(collection, [data])
    except Exception:
        raise Exception(f"{traceback.format_exc()}")
