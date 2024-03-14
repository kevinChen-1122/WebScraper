import configparser
import json

config = configparser.ConfigParser()
config.read('/app/crawler_service/config/config.ini')

# mongodb 設定
mongo_host = config['mongodb']['host_name']
mongo_port = int(config['mongodb']['port'])
database_name = config['mongodb']['database_name']
username = config['mongodb']['username']
password = config['mongodb']['password']

# thread workers 設定
max_workers = int(config["workers"]["max_workers"])
browser_pool_size = int(config["workers"]["browser_pool_size"])

# 旋轉拍賣設定
carousell_url = "https://tw.carousell.com"
query_params_file_path = "/app/crawler_service/config/carousell_query_params.json"

with open(query_params_file_path, 'r') as json_file:
    query_params = json.load(json_file)
