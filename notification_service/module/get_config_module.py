import configparser

config = configparser.ConfigParser()
config.read('/app/notification_service/config/config.ini')

# mongodb 設定
mongo_host = config['mongodb']['host_name']
mongo_port = int(config['mongodb']['port'])
database_name = config['mongodb']['database_name']
username = config['mongodb']['username']
password = config['mongodb']['password']

# line 通知設定
line_notify_token = config['line']['notify_token']
