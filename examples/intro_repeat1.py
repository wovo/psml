import sys
sys.path.append( "../psml" )

from psml import *

m = None
   
m = right( 12 ) ** m + repeat8( 5, 12, 9 ) ** sphere( 2 )
m = right( 20 ) ** m + repeat4( 5, 7 ) ** box( 2, 3, 1 )
m = right( 20 ) ** m + repeat2( 5, 7 ) ** cylinder( 1, 5 )

m.write()