import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

facets( 9 )
m = \
cylinder( radius = 10, height = 20 ) \
   + vector( 25, 0, 10 ) ** sphere( radius = 10 )
m.write()