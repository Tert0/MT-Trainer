from os import getenv
from dotenv import load_dotenv
load_dotenv('.env')
env_file = getenv('ENV_FILE')
if env_file:
    load_dotenv(env_file)
SQL_SERVER_LOCATION = getenv('SERVER_LOCATION', 'postgres://localhost:5432')
SQLITE_DATABASE = bool(getenv('SQLITE_DATABASE', False))
SQL_DATABASE = getenv('DATABASE', 'mt-trainer')
SQL_USERNAME = getenv('DB_USERNAME', 'mt-trainer')
SQL_PASSWORD = getenv('DB_PASSWORD', 'Secret')
SQL_ECHO_OUTPUT = False
