"""
Top-level module of easyDL. By convention, we refer to this module as
`easyDL` instead of `py-easyDL`, following the common practice of importing
py-easyDL via the command `import easyDL`.

The primary function of this module is to import all of the public easyDL
interfaces into a single place. The interfaces themselves are located in
sub-modules.

Note that: you can check our source code easily from the following link
(https://www.github.com/thisisAEmam/easyDL)
"""

import sys
import os
path = os.getcwd()
parent_path = os.path.abspath(os.path.join(path, os.pardir))

if parent_path not in sys.path:
    sys.path.append(parent_path)

del path, parent_path

print('\nWelcome to EasyDL.')
print('Where Deep learning is meant to be easy.')
