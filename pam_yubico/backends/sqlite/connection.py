import sqlite3

from methods import DatabaseMethods

class DatabaseConnection():
	
	def __init__(self, settings = None):
		self.settings = settings

		self.connection = None
		self.cursor = None
		self.methods = None

	def connect(self):
		self.connection = sqlite3.connect(self.settings['path'])
		self.connection.row_factory = sqlite3.Row
		self.cursor = self.connection.cursor()
		self.methods = DatabaseMethods(self.connection, self.cursor)

		self.create_schema()

	def close(self):
		self.connection.close()
		
	def get_methods(self):
		if not self.methods:
			return False
		    
		return self.methods
	
	def create_schema(self, table_name = 'yubikeys'):
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS '%s'
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
	    )""" % (table_name))
