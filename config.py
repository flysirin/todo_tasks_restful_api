import os

from environs import Env

env = Env()
env.read_env()
# Credentials for app flask and user connection
LOGIN = env("LOGIN")
PASSWORD = env("PASSWORD")
HOST = env("HOST")
PORT = env("PORT")

# Credentials for database
DB_NAME = env("DB_NAME")
DB_LOGIN = env("DB_LOGIN")
DB_PASS = env("DB_PASS")
DB_HOST = env("DB_HOST")
DB_PORT = env("DB_PORT")

