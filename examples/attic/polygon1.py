import sys
sys.path.append( "../psml" )

from psml import *

m = polygon( [ 
   [ 0, 0 ], [ 3, 0 ], [ 2, 1 ], [ 2, 2 ], 
   [ 3, 2 ], [ 1, 3 ], [ 0, 3 ], [ 1, 1 ] ] )
   
m.write()