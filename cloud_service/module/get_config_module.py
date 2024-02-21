import configparser

config = configparser.ConfigParser()
config.read('/app/cloud_service/config/config.ini')

# mongodb 設定
mongo_host = config['mongodb']['host_name']
mongo_port = int(config['mongodb']['port'])
database_name = config['mongodb']['database_name']
username = config['mongodb']['username']
password = config['mongodb']['password']

# google api key
spreadsheet_api_key = config['google']['spreadsheet_api_key']
# 關鍵字表單ID
key_word_spreadsheet_id = config['google']['key_word_spreadsheet_id']
# 關鍵字表單名稱
key_word_table_name = config['google']['key_word_table_name']
