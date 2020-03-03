import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

m = None

m = right( 15 ) ** m + vector( 0, 5, 5 ) ** sphere( radius = 5 )
m = right( 15 ) ** m + vector( 0, 5, 0 ) \
    ** cone( radius1 = 5, radius2 = 2, height = 10 )
m = right( 15 ) ** m + vector( 0, 5, 0 ) \
    ** cylinder( radius = 5, height = 10 )
m = right( 20 ) ** m + vector( 0, 0, 0 ) ** box( 10, 20, 5 )

m.write()