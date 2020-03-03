import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

m = \
cone( radius1 = 10, radius2 = 0, height = 20 ) \
   + right( 35 ) ** cone( vector( 20, 20, 10 ))
m.write()