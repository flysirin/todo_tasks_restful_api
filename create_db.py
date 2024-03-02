from pymysql.connections import Connection
from app import app, db
from config import DB_NAME, DB_HOST, DB_PORT, DB_LOGIN, DB_PASS


with app.app_context(), Connection(host=DB_HOST,
                                   port=int(DB_PORT),
                                   user=DB_LOGIN,
                                   password=DB_PASS) as con:
    cur = con.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cur.execute("SHOW DATABASES")
    for databases in cur:
        print(databases)
    db.create_all()
