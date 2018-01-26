# Author's notes from forum:
#Forum thread https://openxcom.org/forum/index.php/topic,1292.0.html
# I've made some scripting in Python to build Soldier highscore list. 
# It needs Python and PyYAML installed. Grabs latest save from OpenXcom
#and shows nifty stats. 
# Tested on Linux. Public domain, so feel free to modify for your own purposes.

# -*- coding: utf-8 -*-
"""
Soldier Hiscore for OpenXcom.

Finds directory with saves, takes most recent savegame and
builds hiscore from that data,


Tested on OpenXcom 0.9

@author: anatoly techtonik
@license: public domain
"""

print('OpenXcom Stats: Soldier Highscore')

# --- 01. bootstrap - set up common paths, check requirements ---
import os

import glob
import sys

try:
  import yaml
except ImportError:
  sys.exit('Error: PyYAML is not found')

# we assume that this script is located at the root of OpenXcom directory,
# so we save its absolute path in the ROOT variable
ROOT = os.path.abspath(os.path.dirname(__file__))
print('Running from:\n  %s' % ROOT)

# --- 02. find user and data dir ---
def find_userdir():
  # TODO: detect on Linux, Windows and Mac OS (see wiki)
  path = os.path.expanduser('~/.local/share/openxcom')
  if not os.path.exists(path):
    return None
  else:
    return path

USERDIR = find_userdir()

# --- 03. game checking logic ----

if not USERDIR:
  sys.exit('Error: User directory with saves not found')
  
saves = glob.glob(USERDIR + '/*.sav')
if not saves:
  sys.exit('Error: No save files found')

# get most recent save
save = sorted(saves, key=os.path.getmtime)[-1]
print('Most recent save: %s' % os.path.basename(save))

# parse save, 0.9 version contains two sections
loader = yaml.safe_load_all(open(save))
header = next(loader)
print('Save format version %s' % header['version'])
data = next(loader)

soldiers = []
soldbase = {}  # id to base name mapping
for base in data['bases']:
  for s in base['soldiers']:
    soldbase[s['id']] = base['name']
    soldiers.append(s)

print('\n--===[ HiScore ]===--\n')
placewidth = len(str(len(soldiers)))
maxname = max(soldiers, key=lambda a: len(a['name']))['name']
maxname = len(maxname)

for i, s in enumerate(sorted(soldiers, key=lambda a: a['kills'], reverse=True)):
  line  = str(i+1).rjust(placewidth) + '. '
  line += s['name'].ljust(maxname+1) + str(s['kills'])
  print(line)
