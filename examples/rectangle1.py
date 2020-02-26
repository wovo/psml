import sys
sys.path.append( "../psml" )

from psml import *

rectangle( shift( 20, 30 ), rounding = 0 ).write()
rectangle( 20, 30 ).write()