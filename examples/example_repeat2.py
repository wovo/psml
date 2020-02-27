import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

m = \
repeat2( 10, 20, 10 ) ** cylinder( 5, 10 )
m.write()