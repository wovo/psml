import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *
from functools import reduce

model = reduce( 
   lambda a, b: a + b, (
      ( 25 * vector( x, y )) ** (
         sphere( 15 ) + 
         vector( 0, 0, 30 ) ** sphere( 10 ) + 
         cylinder( 3, 30 )
      ) for x in range( 1, 10 ) for y in range( 0, x )))
model.write( "output.scad" )