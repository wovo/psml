import sys
sys.path.append( "../psml" )

from psml import *

model = None
def add( m ):
   global x, model
   model += shift( x, y ) ** m
   x += 10
   
x,y = 0, 0   

add( rectangle( 8, 20 ) )
add( rectangle( 8, 20, 2 ) )
add( rectangle( shift( 8, 20 ) ) )
add( rectangle( shift( 8, 20 ), 2 ) )

x,y = 0, 25

add( box( 8, 20, 6 ) )
add( box( 8, 20, 6, 2 ) )
add( box( shift( 8, 20, 6 ) ) )
add( box( shift( 8, 20, 6 ), 2 ) )

model.write()