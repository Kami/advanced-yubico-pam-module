Advanced Yubico PAM module
===

Python PAM module which allows you to integrate the Yubikey into your existing user authentication infrastructure.

This module supports online, failback and offline mode.

For more information about the original C module visit the documentation at [http://code.google.com/p/yubico-pam/wiki/ReadMe](http://code.google.com/p/yubico-pam/wiki/ReadMe).

##Available validation modes

- online - validate OTP against the Yubico or your own validation server
- failback - first try to validate the token against the Yubico validation server and if the connection cannot be made (for example Yubico server is offline or your computer has no connectivity) try the offline validation
- offline - offline validation (AES key must be specified)