import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

right10 = modifier( lambda s: s + vector( 0, 0, 10 ) ** s )

m = \
right10 ** sphere( radius = 6 )

m.write()