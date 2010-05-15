import urllib

from yubico.yubico import Yubico
from yubico.yubico_exceptions import YubicoError

from database import methods as database

# Constants
CLIENT_ID_LENGTH = 12
TOKEN_MIN_LENGTH = 44 # minimum token length (including user id)

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
            return self.__check_otp_online()
        elif mode == 'failback':
            online_check_status = self.__check_otp_online()
            
            if online_check_status:
                return True
            elif online_check_status is None:
                return self.__check_otp_offline()
            else:
                return False
        elif mode == 'offline':
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
            return False
        except decrypt.InvalidAESKey:
            return False
        else:
            if not yubikey.crc_ok:
                return False
        
        user = self.database.get_user_data(self.username, self.user_id, fields = ['counter', 'counter_session'])
        user_counter = user['counter']
        user_counter_session = user['counter_session']
        
        if not (yubikey.counter > user_counter) and not (yubikey.counter == user_counter and yubikey.counter_session > user_counter_session):
            # Replayed OTP
            return False
        
        # OTP is valid, update counter and session counter
        self.database.update_session_data(self.username, self.user_id, yubikey.counter, yubikey.counter_session)
        
        return True