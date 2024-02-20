import requests
from . import mongo_module, get_config_module
from datetime import datetime


def send_line_notify(msg, sticker_package_id="", sticker_id=""):
    try:
        token = get_config_module.line_notify_token
        if not token:
            raise ValueError("Line Notify token is empty.")

        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        payload = {
            'message': msg,
            'stickerPackageId': sticker_package_id,  # 加入貼圖
            'stickerId': sticker_id
            # 可用的貼圖清單：https://developers.line.biz/en/docs/messaging-api/sticker-list/#sticker-definitions
        }
        response = requests.post("https://notify-api.line.me/api/notify?", headers=headers, params=payload)

        db = mongo_module.connect_to_mongodb()
        now = datetime.now()
        collection = db['line_notify_log']

        query = {
            "msg": msg,
            "res_status_code": response.status_code,
            "res_headers": dict(response.headers),
            "res_text": response.text,
            "res_json": response.json() if "application/json" in response.headers.get("content-type",
                                                                                      "").lower() else None,
            "created_at": now.strftime("%Y-%m-%d %H:%M:%S")
        }
        mongo_module.insert_document(collection, query)
    except Exception as e:
        print(f"Failed to send line notify message: {e}")
