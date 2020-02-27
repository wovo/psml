import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

m = \
repeat4( 10, 20 ) ** box( 5, 5, 5 )

m.write()