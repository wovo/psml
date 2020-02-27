import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

m = None

x = extrude( 4 ) ** text( "Hello", height = 10 )

m = (\
x +
right(  70 ) ** mirror( 1, 0, 0 ) ** x +
right(  80 ) ** mirror( 0, 1, 0 ) ** x +
right( 120 ) ** mirror( 0, 0, 1 ) ** x 
)

m.write()