# -*- coding: utf-8 -*-
import os
import re
from distutils.core import setup

version_re = re.compile(
    r'__version__ = (\(.*?\))')

cwd = os.path.dirname(os.path.abspath(__file__))
fp = open(os.path.join(cwd, 'pam_yubico', '__init__.py'))

version = None
for line in fp:
    match = version_re.search(line)
    if match:
        version = eval(match.group(1))
        break
else:
    raise Exception('Cannot find version in __init__.py')
fp.close()

setup(name = 'pam_yubico',
	  version = '.' . join(map(str, version)),
	  description = 'Python PAM module which allows you to integrate the Yubikey into your existing user authentication infrastructure (supports online, failback and offline mode)',
	  author = 'Tomaž Muraus',
	  author_email = 'kami@k5-storitve.net',
	  license = 'GPL',
	  url = 'http://github.com/Kami/advanced-yubico-pam-module/',
	  download_url = 'http://github.com/Kami/advanced-yubico-pam-module/',
	  packages = ['pam_yubico', 'pam_yubico.yubikey'],
	  requires = ['pam_python'],
	  provides = ['pam_yubico'],
	  package_data = {'pam_yubico.yubikey': ['COPYING']},
	  scripts = ['scripts/yktool'],
	  data_files = [('/lib/security/', ['pam_yubico.py'])],
	  
	  classifiers = [
		  'Development Status :: 3 - Alpha',
		  'Environment :: Console',
		  'Intended Audience :: Developers',
		  'Intended Audience :: End Users/Desktop',
		  'License :: OSI Approved :: GNU General Public License (GPL)',
		  'Operating System :: POSIX :: BSD',
		  'Operating System :: POSIX :: Linux',
		  'Programming Language :: Python',
		  'Topic :: Internet :: WWW/HTTP',
		  'Topic :: Security',
		  'Topic :: Software Development :: Libraries',
	],
)