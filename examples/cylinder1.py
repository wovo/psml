import sys
sys.path.append( "../psml" )

from psml import *

m = cylinder( 10, 20 ) + right( 35 ) ** cylinder( vector( 20, 10 ))
m.write()