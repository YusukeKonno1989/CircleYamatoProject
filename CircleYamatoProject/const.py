import os
from dotenv import load_dotenv

MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_PORT = 3306
MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASS = os.environ.get("MYSQL_PASS")
MYSQL_DB = os.environ.get("MYSQL_DB")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXEC_MODE = os.environ.get("EXEC_MODE")