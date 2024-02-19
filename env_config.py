from dotenv import load_dotenv
import os

load_dotenv()


DB_NAME = os.environ.get('POSTGRES_DB')
DB_HOST = os.environ.get('POSTGRES_HOST')
DB_PASS = os.environ.get('POSTGRES_PASSWORD')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PORT = os.environ.get('POSTGRES_PORT')
