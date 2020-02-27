import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

m = \
rectangle( 20, 30, 3 )
# or rectangle( shift( 20, 30 ), rounding = 3 )
m.write()