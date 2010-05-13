.. pam_yubico_advanced documentation master file, created by
   sphinx-quickstart on Tue May 11 08:49:05 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

:mod:`pam_yubico` - Yubico Pluggable Authentication Module (PAM)
================================================================

.. module:: pam_yubico
		 :synopsis: Yubico Pluggable Authentication Module (PAM)

:Author: Tomaž Muraus <kamiREMOVE@k5-storitve.net>
:Maintainer: Tomaž Muraus <kamiREMOVE@k5-storitve.net>
:Version: |release|
:Source: github.org_
:Bug tracker: `http://github.com/issues <http://github.com/Kami/advanced-yubico-pam-module/issues>`_

The Yubico authentication device Yubikey_ generates one-time passwords that can be used for authentication. This module allows you to use the Yubikey device to authenticate to the PAM system.

The PAM system is used primarily for Unix-like system login, but also in external systems like MyProxy, pGina and so on.

To get started, visit the :doc:`installation` page.

Contents:

.. toctree::
   :maxdepth: 2

   requirements
   installation
   installing_pam_python
   configuring_pam
   using_yktool
   faq
   links_and_references

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _github.org: http://github.com/Kami/advanced-yubico-pam-module
.. _Yubikey: http://www.yubico.com/products/yubikey/