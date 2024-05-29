import configparser
import json

config = configparser.ConfigParser()
config.read('/app/crawler_service/config/config.ini')

# 旋轉拍賣設定
carousell_url = "https://tw.carousell.com"
query_params_file_path = "/app/crawler_service/config/carousell_query_params.json"

with open(query_params_file_path, 'r') as json_file:
    query_params = json.load(json_file)
