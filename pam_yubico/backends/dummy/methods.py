import datetime

class DatabaseMethods():

	def __init__(self):
		pass

	def get_user_data(self, username, user_id, fields = None):
		""" Returns user data as a dictionary. """
		pass
	
	def get_all_entries(self, fields = None):
		""" Returns a list of all entries in the database. """
		pass
	
	def entry_exists(self, **kwargs):
		""" Returns True if a database entry with provided values exist, False otherwise. """
		pass
	
	def check_user_exists(self, username):
		""" Returns True if a user with this username exists, False otherwise. """
		pass
	
	def check_user_is_enabled(self, username, user_id):
		""" Returns True if a YubiKey for this user is enabled, False otherwise. """
		pass
	
	def check_user_id_matches_one_provided(self, username, user_id):
		""" Returns True if the user ID matches the one in the database, False otherwise. """
		pass
	
	def update_session_data(self, username, user_id, counter, \
						counter_session):
		""" Updates a YubiKey session data. """
		pass

	def add_yubikey(self, username, client_id, aes_key, \
				user_id, mode):
		""" Adds a new YubiKey to the database. """
		pass

	def enable_yubikey(self, username, user_id):
		""" Enables a disabled YubiKey in the database. """
		pass

	def disable_yubikey(self, username, user_id):
		""" Re-enables a previously disabled YubiKey in the database. """
		pass

	def delete_yubikey(self, username, user_id):
		""" Deletes an existing YubiKey from the database. """
		pass