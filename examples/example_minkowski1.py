import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

x = circle( 5 ) + rectangle( 10, 20 ) + rectangle( 2, 40 )
m = \
x + right( 20 ) ** minkowski ** x
m.write()