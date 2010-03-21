import sqlite3

DATABASE_PATH = '/etc/yubikey_database'

connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()

def create_schema():
    """ Creates the database schema if does not already exist. """
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS 'yubikeys'
    (
    "id" INTEGER PRIMARY KEY,
    "username" VARCHAR(100),
    "client_id" INTEGER,
    "aes_key" VARCHAR(32),
    "user_id" VARCHAR(12),
    "enabled" BOOLEAN DEFAULT (1),
    "counter" INTEGER DEFAULT (0),
    "counter_session" INTEGER DEFAULT (0),
    "date_created" TEXT,
    "mode" TEXT DEFAULT ('online')
    )""")