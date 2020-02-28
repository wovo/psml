import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

x = sphere( 2 ) + box( 10, 20, 5 )

m = \
x = x + right( 20 ) ** minkowski ** x
m.write()