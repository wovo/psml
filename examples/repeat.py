import sys
sys.path.append( "../psml" )

from psml import *

model = None
def add( m ):
   global x, model
   model += shift( x, y ) ** m
   x += 10
   
x,y = 0, 0   

add( repeat2( 5, 7 ) ** cylinder( 1, 5 ) )
add( repeat2( shift( 5, 7 )) ** cylinder( 2, 10 ) )
add( repeat2( 5, 7, 3 ) ** cylinder( 1, 5 ) )
add( repeat2( shift( 5, 7, 3 )) ** cylinder( 2, 10 ) )

x,y = 0, 15

add( repeat4( 5, 7 ) ** box( 2, 3, 5 ) )
add( repeat4( shift( 5, 7 )) ** box( 2, 3, 5 ) )

model.write()