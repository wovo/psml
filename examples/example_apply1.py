import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

m = \
apply( "translate([10,0,0]) color('red')", box( 5, 10, 3 ) )
m.write()