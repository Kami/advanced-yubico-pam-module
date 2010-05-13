===============
Configuring PAM
===============

PAM configuration is somewhat complex, but a typical use-case is to require both a password and Yubikey to allow access.

This can be achieved by a PAM configuration like this::

  auth required pam_unix.so nullok_secure
  auth required pam_python.so pam_yubico.py
  
Alternatively, if you only want require YubiKey to log in, remove the first line, so your config file now looks like this::

  auth required pam_python.so pam_yubico.py
  
*Note 1: On Ubuntu / Debian, PAM related configuration files are located in  the* ``/etc/pam.d`` *directory.*
  
*Note 2: Be sure to uncomment any other 'auth' lines in your PAM configuration, unless you want does. For example, Ubuntu and Debian contains a '@include common-auth' which would confuse the configuration.*

Module parameters
~~~~~~~~~~~~~~~~~

This module supports the following parameters:

1. debug::

  auth required pam_python.so pam_yubico.py debug

Enables the debug mode which logs all the messages to the ``/var/log/pam_yubico.log`` file.

2. alwaysok::

  auth required pam_python.so pam_yubico.py alwaysok=1

Setting this parameter to ``1`` will enable the presentation mode (all the authentication attempts will succeed)