import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

m = (
color( 0, 255, 255 ) ** sphere( 10 ) +
right( 30 ) ** color( 0, 255, 255, 0.5 ) ** sphere( 10 ) +
back( 20 ) ** color( vector( 255, 0, 255 ), alpha = 1 ) ** box( 50, 10, 10 )
)
m.write()