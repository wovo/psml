import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

m = \
box( vector( 20, 30, 10 ), rounding = 2 )
m.write()