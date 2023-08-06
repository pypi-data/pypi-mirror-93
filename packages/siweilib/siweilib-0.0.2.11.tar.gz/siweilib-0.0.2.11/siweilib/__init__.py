import os

fnom = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'VERSION.txt')
if os.path.exists(fnom):
  f = open(fnom)
  s = f.read()
  f.close()
  __version__ = s

import siweilib.general
import siweilib.general as g
import siweilib.filez
import siweilib.filez as f