import sys
sys.path.append( "../psml" )

from psml import *

rectangle( 20, 30, 3 ).write()
rectangle( shift( 20, 30 ), rounding = 3 ).write()
