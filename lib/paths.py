from pathlib import Path
from os import environ

BASE = Path(environ["ELPCD_ROOT"])
CWD = Path('.')

LIB = BASE / 'lib'
ASSETS = BASE / 'assets'

KV = LIB / 'kv'
ICONS = ASSETS / 'icons'

ICON = str((ICONS / 'elpcd192x.png').resolve())
LOGO = str((ASSETS / 'gedalogo2020.png').resolve())