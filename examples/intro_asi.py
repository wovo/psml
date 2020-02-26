import sys
sys.path.append( "../psml" )

from psml import *

m = None

a = down( 10 ) ** cylinder( 5, 20 )
b = rotate( 90, 0, 0 ) ** a 

#m = right( 15 ) ** m + vector( 0, 0, 5 ) ** sphere( 5 )
#m = right( 15 ) ** m + cone( 5, 2, 10 )
#m = right( 15 ) ** m + cylinder( 5, 10 )
m = right( 20 ) ** m + ( a * b )
m = right( 20 ) ** m + ( a - b )
m = right( 20 ) ** m + ( a + b )
m = right( 20 ) ** m + b
m = right( 20 ) ** m + a

m.write()