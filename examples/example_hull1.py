import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

m = None

x = sphere( 10 ) + vector( -3, -3, 15 ) ** box( 6, 6, 6 )

m = (\
x + 
right( 30 ) ** hull ** x
)

m.write()