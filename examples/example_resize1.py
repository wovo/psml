import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

t = text( "hello world" )
m = \
t + back( 10 ) ** resize( 30, 10 ) ** t
m.write()