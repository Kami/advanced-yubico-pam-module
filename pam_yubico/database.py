import settings

try:
	database_backend = settings.DATABASE_BACKEND
except AttributeError:
	raise AttributeError('Database backend not configured')

try:
	name = 'pam_yubico.backends.%s.connection' % (database_backend)
	module_connection = __import__(name, fromlist = 'DatabaseConnection')
	database_connection = module_connection.DatabaseConnection(settings.DATABASE_SETTINGS)
except ImportError:
	raise ImportError('Invalid database backend specified')

connection = getattr(database_connection, 'connect')()
methods = getattr(database_connection, 'get_methods')()