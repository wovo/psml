import sys
sys.path.append( "../psml" )

from psml import *
from functools import reduce
model = reduce( 
   lambda a, b: a + b, (
      ( 25 * shift( x, y )) ** (
         sphere( 15 ) + 
         shift( 0, 0, 30 ) ** sphere( 10 ) + 
         cylinder( 3, 30 )
      ) for x in range( 1, 10 ) for y in range( 0, x )))
model.write( "output.scad" )