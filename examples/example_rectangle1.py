import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

m = \
rectangle( vector( 20, 30 ), rounding = 0 )
# or rectangle( 20, 30 )
m.write()