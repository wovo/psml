import sys
sys.path.append( "../psml" )

from psml import *

s = cylinder( 10, 20 ) + vector( 25, 0, 10 ) ** sphere( 10 )
s.write()