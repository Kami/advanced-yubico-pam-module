import os
import sys
import optparse
import datetime
import ykcheck

from database import connection, cursor, create_schema
from yubikey import decrypt

class YubiKeyTool():
    def __init__(self):
        self.__check_uid()
        self.yubikey = None
        
        self.connection = connection
        self.cursor = cursor
        
        create_schema()

    def add_yubikey(self):
        print 'Add a new Yubikey\n'
        
        try:
            mode = self.__prompt('Mode [online/failback/offline]: ', valid_options = ['online', 'failback', 'offline'])
            username = self.__prompt('Username: ')
            client_id = self.__prompt('Client ID: ')
            
            if mode != 'online':
                aes_key = self.__prompt('AES key: ', validate_function = self.__check_aes_key, error_msg = 'Invalid AES key')
                otp = self.__prompt('OTP: ', validate_function = self.__check_otp, validate_function_kwargs = {'aes_key': aes_key}, \
                                    error_msg = 'Invalid OTP length')
            else:
                aes_key = ''
                otp = self.__prompt('OTP: ', validate_function = self.__check_otp_length, error_msg = 'Invalid OTP length')
                
            user_id = otp[:12]
        except KeyboardInterrupt:
            sys.exit(0)
            
        print ''
        print 'Username\t: %s' % (username)
        print 'Client ID\t: %s' % (client_id)
        print 'AES key\t\t: %s' % (aes_key)
        print 'OTP\t\t: %s' % (otp)
        print 'User ID\t\t: %s' % (user_id)
        print 'Mode\t\t: %s' % (mode)
        
        confirmation = self.__prompt('Is this information correct? [y/n]: ', valid_options = ['y', 'n']).lower()
        
        if confirmation == 'n':
            return
        
        print ''
        if self.__database_entry_exists(username = username, user_id =  user_id):
            print 'User with this username and user ID already exists.'
            return
        
        if self.__add_yubikey_to_database(username, client_id, aes_key, user_id, mode):
            print 'User has been successfully added to the database.'
        else:
            print 'Error occurred - user could not be added to the database.'
    
    # @todo: to implement        
    def edit_yubikey(self):
        pass
    
    def delete_yubikey(self):
        print 'Delete a YubiKey from the database\n'
        
        username = self.__prompt('Username: ')
        user_id = self.__prompt('User ID: ')
        
        if self.__database_entry_exists(username = username, user_id = user_id):
            self.__delete_yubikey_from_database(username, user_id)
            print 'User with ID %s has been successfully deleted' % (user_id)
        else:
            print 'User with this username and user ID is not in the database'
            
    def disable_yubikey(self):
        print 'Disable a YubiKey\n'
        
        username = self.__prompt('Username: ')
        user_id = self.__prompt('User ID: ')
        
        if not self.__database_entry_exists(username = username, user_id =  user_id):
            print 'User with this username and user ID is not in the database'
        elif self.__database_entry_exists(enabled = 0, username = username, user_id = user_id):
            print 'Yubikey for this user is already disabled'
        else:
            self.__disable_yubikey_in_database(username, user_id)
            print 'Yubikey for user with username %s and user ID %s has been successfully disabled' % (username, user_id)
            
    def enable_yubikey(self):
        print 'Enabled a previously disabled YubiKey\n'
        
        username = self.__prompt('Username: ')
        user_id = self.__prompt('User ID: ')
        
        if not self.__database_entry_exists(username = username, user_id =  user_id):
            print 'User with this username and user ID is not in the database'
        elif self.__database_entry_exists(enabled = 1, username = username, user_id = user_id):
            print 'Yubikey for this user is already enabled'
        else:
            self.__enable_yubikey_in_database(username, user_id)
            print 'Yubikey for user with username %s and user ID %s has been successfully re-enabled' % (username, user_id)
    
    def display_database_info(self):
        self.cursor.execute("SELECT id, username, client_id, mode, enabled FROM yubikeys")
        result = self.cursor.fetchall()
    
        print 'YubiKeys in the database:\n'
    
        count = len(result)
        if count > 0:
            print 'ID\t | Username\t | Client ID\t | Mode\t | Status'
            for row in result:
                print '%d\t | %s\t | %d\t | %s\t | %s' % (row[0], row[1], row[2], row[3], 'enabled' if row[4] == 1 else 'disabled')
        
            print '\nTotal: %d' % (count)
        else:
            print 'The database is empty'
            
    def __add_yubikey_to_database(self, username, client_id, aes_key, user_id, mode):
        date = datetime.datetime.now()
        self.cursor.execute("INSERT INTO yubikeys (username, client_id, aes_key, user_id, mode, date_created) \
                            VALUES (?, ?, ?, ?, ?, ?)", (username, client_id, aes_key, user_id, mode, date))
        self.connection.commit()
        
        return self.cursor.rowcount
    
    def __disable_yubikey_in_database(self, username, user_id):
        self.cursor.execute("UPDATE yubikeys SET enabled = 0 WHERE username = :username AND user_id = :user_id", {'username': username, \
                            'user_id': user_id})
        self.connection.commit()
        
        return self.cursor.rowcount
    
    def __enable_yubikey_in_database(self, username, user_id):
        self.cursor.execute("UPDATE yubikeys SET enabled = 1 WHERE username = :username AND user_id = :user_id", {'username': username, \
                            'user_id': user_id})
        self.connection.commit()
        
        return self.cursor.rowcount
    
    def __delete_yubikey_from_database(self, username, user_id):
        self.cursor.execute("DELETE FROM yubikeys WHERE username = :username AND user_id = :user_id", {'username': username, \
                            'user_id': user_id})
        self.connection.commit()
        
        return self.cursor.rowcount
        
    def __prompt(self, message, required = True, validate_function = None, validate_function_kwarg_name = 'input', validate_function_kwargs = None, error_msg = '', valid_options = None):
        input = None
        
        while not input:
            input = raw_input(message)
            
            if not required:
                return input
            
            if validate_function and input:
                kwargs = {'%s' % (validate_function_kwarg_name): input}
                
                if validate_function_kwargs:
                    kwargs.update(validate_function_kwargs)
                
                valid = validate_function(**kwargs)
                
                if not valid:
                    print error_msg
                    input = None
    
            if valid_options and (input.lower() not in valid_options):
                print 'Valid options are: %s' % ('/' . join(valid_options))
                input = None
            
        return input
    
    def __check_aes_key(self, input):
        if len(input) != 32:
            return False
        
        if not decrypt.RE_AES_KEY.match(input):
            return False
    
        return True
    
    def __check_otp_length(self, input):
        """ Returns True is token length is valid, False otherwise. """
        
        if len(input) >= ykcheck.TOKEN_MIN_LENGTH:
            return True
        
        return False
    
    def __check_otp(self, input, aes_key):
        """ Returns True if OTP is valid, False otherwise. """
        
        try:
            yubikey = decrypt.YubikeyToken(input, aes_key)
        except decrypt.InvalidToken:
            return False
        except decrypt.InvalidAESKey:
            return False
        else:
            if not yubikey.crc_ok:
                return False

        self.yubikey = yubikey
        return True
    
    def __database_entry_exists(self, **kwargs):
        """ Returns True if a database entry with provided values exist, False otherwise. """
        
        where_clause = ['%s = :%s' % (key, key) for key in kwargs]
        where_clause = ' AND ' . join(where_clause)
        
        self.cursor.execute("SELECT id FROM yubikeys WHERE %s" % (where_clause), kwargs)
        result = self.cursor.fetchone()
        
        if result:
            return True
        
        return False
    
    def __check_uid(self):
        """ Only root can run this program. """
        
        uid = os.getuid()
        
        if uid != 0:
            print 'This tool can only be run as root'
            sys.exit(0)

if __name__ == '__main__':
    available_actions = {'add': 'add_yubikey',
                         'edit': 'edit_yubikey',
                         'delete': 'delete_yubikey',
                         'disable': 'disable_yubikey',
                         'enable': 'enable_yubikey',
                         'info': 'display_database_info'
    }
    
    parser = optparse.OptionParser(version = '%prog')
    parser.add_option('-a', '--add', action = 'store_true', default = False, dest = 'add', help = 'add a new yubikey to database')
    parser.add_option('-e', '--edit', action = 'store_true', default = False, dest = 'edit', help = 'edit an existing database entry')
    parser.add_option('-d', '--delete', action = 'store_true', default = False, dest = 'delete', help = 'delete an existing key from database')
    parser.add_option('--disable', action = 'store_true', default = False, dest = 'disable', help = 'disable a yubikey')
    parser.add_option('--enable', action = 'store_true', default = False, dest = 'enable', help = 'enable a previously disabled yubikey')
    
    parser.add_option('-i', '--info', action = 'store_true', default = False, dest = 'info', help = 'displays database information')

    (options, args) = parser.parse_args()
    options = vars(options)

    selected_option = [available_actions[key] for key, value in options.iteritems() if value == True]
    
    if not selected_option:
        parser.error('you must supply an action')
        
    if len(selected_option) > 1:
        parser.error('you can only choose one action')
    
    yubiKeyTool = YubiKeyTool()
    getattr(yubiKeyTool, selected_option[0])()