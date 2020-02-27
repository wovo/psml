import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

m = None

p = polygon( [ 
   [ 0, 0 ], [ 3, 0 ], [ 2, 1 ], [ 2, 2 ], 
   [ 3, 2 ], [ 1, 3 ], [ 0, 3 ], [ 1, 1 ] ] )

m = right(  0 ) ** m + back( 4 ) ** text( "psml", 8 )
m = right( 20 ) ** m + scale( dup3( 5 )) ** p
m = right( 12 ) ** m + back( 5 ) ** circle( 5 )
m = right( 20 ) ** m + rectangle( 10, 20 )

m.write()