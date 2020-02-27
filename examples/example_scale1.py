import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

b = box( 10, 20, 40 )
m = (
    b +
    right(  30 ) ** scale( 2, 1, 1 ) ** b +
    right(  70 ) ** scale( 1, 2, 1 ) ** b +
    right( 100 ) ** scale( 1, 1, 2 ) ** b
)
m.write()