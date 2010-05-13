---
FAQ
---

Why have you created this module?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
I have created this module, because the `original Yubico PAM module`_ written in C was not working on my computer (it was segfaulting).

I have spent a few hours debugging it, but I could not locate the problem so I have just decided to write a new module which performs the same task in Python.

P.S. Apparently that is known problem on 64 bit systems (`forum thread #1`_, `my forum thread`_).

Why Python?
~~~~~~~~~~~
I know that using Python for a PAM module is not really the best and most efficient way, but since my C knowledge is pretty basic, I decided to stick to Python.

It currently works fine for me and should also work for other users who have problems with the original C extension or want extra features (for example offline validation).

What is the difference between this (sometimes referred to as pam_yubico_advanced) and the other pam_yubico package?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
pam_yubico_ module is a first module which I have created after having problems with the original module written in C.

It is basically just a quick working solution which only supports online validation.

This development of pam_yubico module is now discarded in favor of this package.

How can I protect my GNOME screensaver with a YubiKey?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can protect your screensaver by putting the appropriate line into your ``gnome-screensaver`` PAM config file.

In Ubuntu this can be achieved by putting the following line to the ``/etc/pam.d/gnome-screensaver`` file::

  auth required pam_python.so pam_yubico.py

.. _original Yubico PAM module: http://code.google.com/p/yubico-pam/
.. _forum thread #1: http://forum.yubico.com/viewtopic.php?f=3&t=254&st=0&sk=t&sd=a&hilit=segfault&start=0
.. _my forum thread: http://forum.yubico.com/viewtopic.php?f=3&t=507&start=0&st=0&sk=t&sd=a&hilit=segfault
.. _pam_yubico: http://github.com/Kami/yubico-pam-module