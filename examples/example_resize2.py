import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

s = sphere( 10 )
m = \
s + right( 40 ) ** resize( 40, 0, None ) ** s
m.write()