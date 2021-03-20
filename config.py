from os import getenv
from dotenv import load_dotenv
load_dotenv()

SQL_SERVER_LOCATION = getenv('SERVER_LOCATION', 'postgres://localhost:5432')
SQL_DATABASE = getenv('DATABASE', 'mt-trainer')
SQL_USERNAME = getenv('DB_USERNAME', 'mt-trainer')
SQL_PASSWORD = getenv('DB_PASSWORD', 'Secret')
SQL_ECHO_OUTPUT = False
