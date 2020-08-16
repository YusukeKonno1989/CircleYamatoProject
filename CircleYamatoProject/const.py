import os

SSH_BASTION_ADDRESS = "13.115.127.128"
SSH_PORT = 22
SSH_USER = "ec2-user"
SSH_PKEY_PATH = os.path.expanduser("~/.ssh/FirstKey.pem")
MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_PORT = 3306
MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASS = os.environ.get("MYSQL_PASS")
MYSQL_DB = os.environ.get("MYSQL_DB")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXEC_MODE = os.environ.get("EXEC_MODE")