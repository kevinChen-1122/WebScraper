import configparser
import json

config = configparser.ConfigParser()
config.read('config/config.ini')

# mongodb 設定
mongo_host = config['mongodb']['host_name']
mongo_port = int(config['mongodb']['port'])
database_name = config['mongodb']['database_name']
username = config['mongodb']['username']
password = config['mongodb']['password']

# 旋轉拍賣設定
carousell_url = config['carousell']['home_page']
keyword_file_path = config['carousell']['search_keyword_file_path']
query_params_file_path = config['carousell']['query_params']

with open(query_params_file_path, 'r') as json_file:
    query_params = json.load(json_file)

with open(keyword_file_path, 'r') as json_file:
    keyword = json.load(json_file)
