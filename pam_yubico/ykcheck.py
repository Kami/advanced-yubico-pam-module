import logging
import urllib

from yubico.yubico import Yubico
from yubico.yubico_exceptions import YubicoError

import settings
from database import methods as database

# Constants
CLIENT_ID_LENGTH = 12
TOKEN_MIN_LENGTH = 44 # minimum token length (including user id)

# Setup logging
logging.basicConfig(filename = settings.LOG_PATH, filemode = 'a', level = logging.DEBUG, format = '%(asctime)s %(levelname)-8s %(message)s', datefmt = '%d.%m.%Y %H:%M:%S')

class YubiKeyCheck():
	def __init__(self):
		self.database = database

		self.client_id = None
		self.username = None
		self.user_id = None
		self.aes_key = None
		self.otp = None
		
	def validate_otp(self):
		""" Returns True if OTP is valid, False otherwise. """
		result = self.database.get_user_data(self.username, self.user_id, fields = ['client_id', 'aes_key', 'mode'])
		
		self.client_id = result['client_id']
		self.aes_key = result['aes_key']
		mode = result['mode']
		
		if mode == 'online':
			logging.debug('Validating OTP [online mode]')
			return self.__check_otp_online()
		elif mode == 'failback':
			logging.debug('Validating OTP [failback mode]')
			online_check_status = self.__check_otp_online()
			
			if online_check_status:
				logging.debug('Validating OTP: online mode succeeded')
				return True
			elif online_check_status is None:
				logging.debug('Validating OTP: online mode failed, performing offline validation')
				return self.__check_otp_offline()
			else:
				return False
		elif mode == 'offline':
			logging.debug('Validating OTP [offline mode]')
			return self.__check_otp_offline()
		
		return False

	def __check_otp_online(self):
		""" Returns None if the connection cannot be made, True is the OTP is valid and False otherwise. """
		
		yubico = Yubico(self.client_id)
		
		try:
			status = yubico.verify(self.otp)
		except YubicoError:
			return False
		
		if status is False:
			return False
		elif status is None:
			return None
		
		return True

	def __check_otp_offline(self):
		""" Returns True and updates the counters in the database if the OTP is valid, False otherwise. """
 
		from yubikey import decrypt
		
		try:
			yubikey = decrypt.YubikeyToken(self.otp, self.aes_key)
		except decrypt.InvalidToken:
			logging.debug('Validating OTP: Invalid OTP')
			return False
		except decrypt.InvalidAESKey:
			logging.debug('Validating OTP: Invalid AES key')
			return False
		else:
			if not yubikey.crc_ok:
				logging.debug('Validating OTP: Invalid CRC')
				return False
		
		user = self.database.get_user_data(self.username, self.user_id, fields = ['counter', 'counter_session'])
		user_counter = user['counter']
		user_counter_session = user['counter_session']
		
		if not (yubikey.counter > user_counter) and not (yubikey.counter == user_counter and yubikey.counter_session > user_counter_session):
			# Replayed OTP
			logging.debug('Validating OTP: Replayed OTP')
			return False
		
		# OTP is valid, update counter and session counter
		self.database.update_session_data(self.username, self.user_id, yubikey.counter, yubikey.counter_session)
		
		return True