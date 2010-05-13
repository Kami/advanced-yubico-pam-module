=====================
Installing pam_python
=====================

The pam_yubico module depends on the pam_python_ which should be installed before installing this module.

Here are can find short instructions how to install this module in Linux.

This pages assumes that you are installing it on Ubuntu / Debian, but it should work fine on other distributions as well (just replace APT with your distribution package manager or build the dependencies from source).

1. Install the dependencies
---------------------------
To compile and run this module you need the PAM runtime and development files and Python development files.

On Ubuntu / Debian you can install them using APT::

  sudo apt-get install libpam0g libpam-runtime libpam0g-dev python-dev
  
2. Download and unpack the source code
---------------------------------------

Download the tar ball::

  wget http://ace-host.stuart.id.au/russell/files/pam_python/pam-python-0.1.1.tar.gz
  
Unpack it::

  tar -xzvf pam-python-0.1.1.tar.gz
  
Move to the directory where the files were unpacked::

  cd pam-python-0.1.1
  
3. Build and install the module
-------------------------------

Build it::

  make
  
and then install it::

  sudo make install
  
If the script fails and complains that it cannot create the ``/usr/share/doc/pam_python/html`` directory, you can create it yourself::

  sudo mkdir -p /usr/share/doc/pam_python/html
  
or delete the following line from the ``Makefile`` so that the documentation Makefile is skipped::

  $(MAKE) --directory doc $@
  
and run the install script again::

  sudo make install
  
If everything went well, ``pam_python.so`` should be copied to the ``/lib/security`` directory.
  
.. _pam_python: http://ace-host.stuart.id.au/russell/files/pam_python/