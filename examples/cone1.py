import sys
sys.path.append( "../psml" )

from psml import *

m = cone( 10, 0, 20 ) + right( 35 ) ** cone( vector( 20, 10, 10 ))
m.write()