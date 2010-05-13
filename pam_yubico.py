# -*- coding: utf-8 -*-
#
# Name: Advanced Yubico PAM module
# Description: Python PAM module which allows you to integrate the Yubikey
# into your existing user authentication infrastructure.
#
# This module supports online, failback and offline mode.
#
# For more information about the original C module visit the documentation at
# http://code.google.com/p/yubico-pam/wiki/ReadMe
#            
# Author: Tomaž Muraus (http://www.tomaz-muraus.info)
# Version: 0.3.0-dev

# Requirements:
# - Python >= 2.6
# - pam
# - python-pam
# - pam-python (http://ace-host.stuart.id.au/russell/files/pam_python/)

import os
import sys
import logging

from pam_yubico import ykcheck

# Setup logging
logging.basicConfig(filename = '/var/log/pam_yubico.log', filemode = 'a', level = logging.DEBUG, format = '%(asctime)s %(levelname)-8s %(message)s', datefmt = '%d.%m.%Y %H:%M:%S')

class MessagePrompt():
    # Dummy Message class
    msg = ''
    msg_style = 0

def pam_sm_authenticate(pamh, flags, argv):
    user = pamh.user
    arguments = _parse_arguments(argv)
    
    ykCheck = ykcheck.YubiKeyCheck()
    ykCheck.username = user

    if not ykCheck.check_user_exists():
        # No user id is set for this username
        logging.debug('No YubiKey is set for user %s' % (user))
        return pamh.PAM_AUTHINFO_UNAVAIL

    prompt = MessagePrompt()
    prompt.msg = 'Yubikey for `%s`: ' % (user)
    prompt.msg_style = pamh.PAM_PROMPT_ECHO_OFF
    
    response = pamh.conversation(prompt).resp
    otp = response
    
    logging.debug('OTP = %s' % (otp))
    
    if arguments['alwaysok'] == 1:
        # Presentation mode is enabled
        logging.debug('Presenation mode is ON')
        return pamh.PAM_SUCCESS
    
    if not otp:
        # No OTP is provided by the user
        logging.debug('No OTP provided')
        return pamh.PAM_AUTH_ERR
    
    if len(otp) < ykcheck.TOKEN_MIN_LENGTH:
        # Invalid OTP length
        logging.debug('Invalid OTP length')
        return pamh.PAM_AUTH_ERR
    
    user_id = otp[:12]
    logging.debug('user ID = %s' % (user_id))
    
    ykCheck.user_id = user_id
    ykCheck.otp = otp
    
    if not ykCheck.check_user_is_enabled():
        logging.debug('YubiKey for user %s is disabled' % (user))
        return pamh.PAM_AUTH_ERR

    if not ykCheck.check_user_id_matches_one_provided():
        # User ID is not matching
        logging.debug('User ID in the database does not match the one provided by the OTP')
        return pamh.PAM_AUTH_ERR

    valid_otp = ykCheck.validate_otp()

    if not valid_otp:
        logging.debug('Error, the provided OTP is invalid')
        return pamh.PAM_AUTH_ERR
    
    # Everything went well and the provided OTP is valid    
    logging.debug('Success, the provided OTP is OK')
    return pamh.PAM_SUCCESS

def pam_sm_setcred(pamh, flags, argv):
    # @todo: not implemented
    return pamh.PAM_CRED_UNAVAIL

def pam_sm_acct_mgmt(pamh, flags, argv):
    # @todo: not implemented
    return pamh.PAM_SUCCESS

def pam_sm_chauthtok(pamh, flags, argv):
    # @todo: not implemented
    return pamh.PAM_SUCCESS

def pam_sm_open_session(pamh, flags, argv):
    # @todo: not implemented
    return pamh.PAM_SUCCESS

def pam_sm_close_session(pamh, flags, argv):
    # @todo: not implemented
    return pamh.PAM_SUCCESS        

def _parse_arguments(args = None):
    """ Parses the provided arguments. """
    
    arguments = {
            'debug': False,
            'alwaysok': 0,
    }
    
    if args:
        if 'debug' in args:
            arguments['debug'] = True
        else:
            logging.disable(logging.FATAL)
        
        logging.debug('Arguments')
        for argument in args:
            if len(argument.split('=')) != 2:
                continue
            
            (key, value) = argument.split('=')
            if key in arguments:
                if key in ['alwaysok']:
                    value = int(value)
                
                logging.debug('%s = %s' % (key, value)) 
                arguments[key] = value
            
    return arguments