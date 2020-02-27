import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

m = \
repeat8( 10, 20, 8 ) ** sphere( 3 )

m.write()