# support for the 3 * LiPo pack

import sys
sys.path.append( "../psml" )

from psml import *

w = 2
m = 1
pcb = shift( 78, 83 )

x = \
   ( extrude( w ) ** rectangle( pcb + 2 * dup2( m + w ), 2 ) ) + \
   ( dup2( w + m ) + shift( 4, 3 ) ) ** repeat4( 71.5, 73.5 ) ** bus( 2, 8 )
   
x.write()   

      