import datetime

class DatabaseMethods():

	def __init__(self, connection, cursor):
		self.connection = connection
		self.cursor = cursor

	def get_user_data(self, username, user_id, fields = None):
		fields = ', ' . join(fields)
		self.cursor.execute("SELECT %s FROM yubikeys WHERE username = :username AND \
							user_id = :user_id" % (fields), {'username': username, 'user_id': user_id})
		result = self.cursor.fetchone()
		
		return result
	
	def get_all_entries(self, fields = None):
		fields = ', ' . join(fields)
		self.cursor.execute("SELECT %s FROM yubikeys" % (fields))
		result = self.cursor.fetchall()
		
		return result
	
	def entry_exists(self, **kwargs):
		where_clause = ['%s = :%s' % (key, key) for key in kwargs]
		where_clause = ' AND ' . join(where_clause)

		self.cursor.execute("SELECT id FROM yubikeys WHERE %s" % (where_clause), kwargs)
		result = self.cursor.fetchone()

		if result:
			return True

		return False
	
	def check_user_exists(self, username):
		self.cursor.execute("SELECT id FROM yubikeys WHERE username = :username", {'username': username})
		result = self.cursor.fetchone()
		
		if result:
			return True
		
		return False
	
	def check_user_is_enabled(self, username, user_id):
		self.cursor.execute("SELECT id FROM yubikeys WHERE enabled = 1 AND username = :username AND user_id = :user_id", \
							{'username': username, 'user_id': user_id})
		result = self.cursor.fetchone()
		
		if result:
			return True
		
		return False
	
	def check_user_id_matches_one_provided(self, username, user_id):
		self.cursor.execute("SELECT id FROM yubikeys WHERE username = :username AND user_id = :user_id", {'username': username, \
																										  'user_id': user_id})
		result = self.cursor.fetchone()
		
		if result:
			return True
		
		return False
	
	def update_session_data(self, username, user_id, counter, \
						counter_session):
		date = datetime.datetime.now()
		self.cursor.execute("UPDATE yubikeys SET counter = :counter, counter_session = :counter_session WHERE \
							username = :username AND user_id = :user_id", {'username': username, 'user_id': user_id, \
																		   'counter': counter, \
																		   'counter_session': counter_session})
		self.connection.commit()

		return True

	def add_yubikey(self, username, client_id, aes_key, \
				user_id, mode):
		date = datetime.datetime.now()
		self.cursor.execute("INSERT INTO yubikeys (username, client_id, aes_key, user_id, mode, date_created) \
                            VALUES (?, ?, ?, ?, ?, ?)", (username, client_id, aes_key, user_id, mode, date))
		self.connection.commit()

		return self.cursor.rowcount

	def enable_yubikey(self, username, user_id):
		self.cursor.execute("UPDATE yubikeys SET enabled = 1 WHERE username = :username AND user_id = :user_id", {'username': username, \
                            'user_id': user_id})
		self.connection.commit()

		return self.cursor.rowcount

	def disable_yubikey(self, username, user_id):
		self.cursor.execute("UPDATE yubikeys SET enabled = 0 WHERE username = :username AND user_id = :user_id", {'username': username, \
                            'user_id': user_id})
		self.connection.commit()

		return self.cursor.rowcount

	def delete_yubikey(self, username, user_id):
		self.cursor.execute("DELETE FROM yubikeys WHERE username = :username AND user_id = :user_id", {'username': username, \
							'user_id': user_id})
		self.connection.commit()

		return self.cursor.rowcount