import urllib

from yubico.yubico import Yubico
from yubico.yubico_exceptions import YubicoError

from database import connection, cursor, create_schema

# Constants
CLIENT_ID_LENGTH = 12
TOKEN_MIN_LENGTH = 44 # minimum token length (including user id)

class YubiKeyCheck():
    def __init__(self):
        self.connection = connection
        self.cursor = cursor
        
        create_schema()

        self.client_id = None
        self.username = None
        self.user_id = None
        self.aes_key = None
        self.otp = None
        
    def validate_otp(self):
        """ Returns True if OTP is valid, False otherwise. """
        
        self.cursor.execute("SELECT client_id, aes_key, mode FROM yubikeys WHERE username = :username", {'username': self.username})
        result = self.cursor.fetchone()
        
        self.client_id = result[0]
        self.aes_key = result[1]
        mode = result[2]
        
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
    
    def check_user_exists(self):
        """ Returns True if a user with this username exists, False otherwise. """
        
        self.cursor.execute("SELECT id FROM yubikeys WHERE username = :username", {'username': self.username})
        result = self.cursor.fetchone()
        
        if result:
            return True
        
        return False
    
    def check_user_is_enabled(self):
        """ Returns True is a YubiKey for this user is enabled, False otherwise. """
        
        self.cursor.execute("SELECT id FROM yubikeys WHERE enabled = 1 AND username = :username AND user_id = :user_id", \
                            {'username': self.username, 'user_id': self.user_id})
        result = self.cursor.fetchone()
        
        if result:
            return True
        
        return False
    
    def check_user_id_matches_one_provided(self):
        """ Returns True if the user ID matches the one in the database, False otherwise. """
        
        self.cursor.execute("SELECT id FROM yubikeys WHERE username = :username AND user_id = :user_id", {'username': self.username, \
                                                                                                          'user_id': self.user_id})
        result = self.cursor.fetchone()
        
        if result:
            return True
        
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
        
        user = self.__get_user_data()
        user_counter = user[2]
        user_counter_session = user[3]
        
        if not (yubikey.counter > user_counter) and not (yubikey.counter == user_counter and yubikey.counter_session > user_counter_session):
            # Replayed OTP
            return False
        
        # OTP is valid, update counter and session counter
        self.cursor.execute("UPDATE yubikeys SET counter = :counter, counter_session = :counter_session WHERE \
                            username = :username AND user_id = :user_id", {'username': self.username, 'user_id': self.user_id, \
                                                                           'counter': yubikey.counter, \
                                                                           'counter_session': yubikey.counter_session})
        self.connection.commit()
        
        return True
    
    def __get_user_data(self):
        """ Returns user data as a tuple. """

        self.cursor.execute("SELECT username, user_id, counter, counter_session, mode FROM yubikeys WHERE username = :username AND \
                            user_id = :user_id", {'username': self.username, 'user_id': self.user_id})
        result = self.cursor.fetchone()
        
        return result