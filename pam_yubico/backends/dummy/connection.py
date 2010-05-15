import sqlite3

from methods import DatabaseMethods

class DatabaseConnection():
	
	def __init__(self, settings = None):
		self.settings = settings
		pass
	
	def connect(self):
		self.methods = DatabaseMethods()
		pass
	
	def close(self):
		pass

	def get_methods(self):
		if not self.methods:
			return False

		return self.methods