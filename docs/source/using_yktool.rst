============
Using yktool
============

yktool is a simple script for managing the YubiKey database.

It allows you to add, delete, enable or disable a YubiKey.

Here are is the list of all the available options.

-a, ``--add``
~~~~~~~~~~~~~
Add a new YubiKey to the database.

Example usage::

  sudo yktool -a
  
Example output::

  Add a new Yubikey
  
  Mode [online/failback/offline]: online
  Username: kami
  Client ID: 1234
  OTP: vvmuikselnzitfjudliicnnndudluffffhgcggrrkhbkv
  
  Username		: kami
  Client ID		: 1234
  AES key		: 
  OTP			: vvmuikselnzitfjudliicnnndudluffffhgcggrrkhbkv
  User ID		: vvmuikselnzit
  Mode			: online
  Is this information correct? [y/n]: y
  
  User has been successfully added to the database.

-d, ``--delete``
~~~~~~~~~~~~~~~~
Delete an existing YubiKey from the database:

Example usage::

  sudo yktool -d
  
Example output::

  Delete a YubiKey from the database
  
  Username: kami
  User ID: vvmuikselnzit
  User with ID vvmuikselnzit has been successfully deleted
  
  
``--disable``
~~~~~~~~~~~~~

Disable an existing YubiKey.

Example usage::

  sudo yktool --disable
 
Example output::

  Disable a YubiKey

  Username: kami
  User ID: vvmuikselnzit
  Yubikey for user with username kami and user ID vvmuikselnzit has been successfully disabled
  
``--enable``
~~~~~~~~~~~~

Enable a previously disabled YubiKey.

Example usage::

  sudo yktool --enable
 
Example output::

  Enable a previously disabled YubiKey

  Username: kami
  User ID: vvmuikselnzit
  Yubikey for user with username kami and user ID vvmuikselnzit has been successfully enabled
  
  
-i, ``--info``
~~~~~~~~~~~~~~

Displays the database information.

Example usage::

  sudo yktool -i

Example output::

  YubiKeys in the database:
  
    ID	 	 | Username	 | Client ID	 | Mode	 		 | Status
    1		 | kami	 	 | 1234			 | failback	 	 | enabled

-h, ``--help``
~~~~~~~~~~~~~~

Example usage::

  yktool -h
  
Example output::

  Usage: yktool.py [options]
  
  Options:
    --version     show program's version number and exit
    -h, --help    show this help message and exit
    -a, --add     add a new yubikey to database
    -e, --edit    edit an existing database entry
    -d, --delete  delete an existing key from database
    --disable     disable a yubikey
    --enable      enable a previously disabled yubikey
    -i, --info    displays database information
  
  Shows the available options and exits.