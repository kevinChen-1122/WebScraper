from . import get_config_module
import requests
import traceback


def get_key_word():
    try:
        spreadsheet_id = get_config_module.key_word_spreadsheet_id
        table_name = get_config_module.key_word_table_name
        key = get_config_module.spreadsheet_api_key

        if not spreadsheet_id or not table_name or not key:
            raise Exception(f"need parameter:spreadsheet_id({spreadsheet_id}) table_name({table_name}) key({key})")

        result = requests.get(
            f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{table_name}?alt=json&key={key}")
        if result.status_code != 200:
            raise Exception(f"google spreadsheets api request fail:{result}")

        return result.text
    except Exception:
        raise Exception(f"{traceback.format_exc()}")
