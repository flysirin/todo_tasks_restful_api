from environs import Env

env = Env()
env.read_env()

LOGIN = env("LOGIN")
PASSWORD = env("PASSWORD")
DATABASE = env("DATABASE")
HOST = env("HOST")
PORT = env("PORT")
