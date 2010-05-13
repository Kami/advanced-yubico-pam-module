=====================
Installation
=====================

1. Installing the dependencies
------------------------------
For this module to work, you need the sqlite3_ package and the pam_python_ module and it's dependencies.

If you are using Python >= 2.5 you should already have the sqlite3 module installed so you can skip the step bellow.

Alternatively, if you don't and you are using Ubuntu / Debian you can install the ``python-sqlite`` package using APT::

  sudo apt-get install python-sqlite

For the instructions how to do install the pam_python_ module, visit the :doc:`installing_pam_python` page.

2. Installing this module
-------------------------
You can install the latest stable version from PyPi::

  sudo pip install pam_yubico
  
or the latest development version from the git repository::

  sudo pip -e install git://github.com/Kami/advanced-yubico-pam-module.git#egg=pam_yubico

3. Create an empty log file
---------------------------
After the module has been successfully installed you need to create an empty file where the module log messages will be saved::

  sudo touch /var/log/pam_yubico.log
  
You also need to give it the appropriate permissions else the module won't work::

  sudo chmod go+w /var/log/pam_yubico.log
  
4. Add one or more YubiKeys
---------------------------
Before enabling this PAM module you need to add at least one YubiKey to the database.

You can do this by running the ``yktool`` with the -a argument and following the on screen instructions::

  sudo yktool -a
  
Fore more information about the ``yktool`` and the available arguments visit the :doc:`using_yktool` page.
  
5. Add appropriate line to your pam config file(s)
--------------------------------------------------
Add the following line to your PAM config file and you are good to go::

  auth required pam_python.so pam_yubico.py
  
For more information about configuring PAM file, visit the :doc:`configuring_pam` page.

.. _pam_python: http://ace-host.stuart.id.au/russell/files/pam_python/
.. _sqlite3: http://docs.python.org/library/sqlite3.html