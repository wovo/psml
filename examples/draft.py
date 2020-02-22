import sys
sys.path.append( "../psml" )

from psml import *

def snowman():
   return ( sphere( 15 ) + 
       shift( 0, 0, 18 ) ** (
           sphere( 10 ) +
           rotate( 90, 0, 0 ) ** cylinder( 2, 15 )))

m = snowman()
      
facets( 10 )      
      
m = shift( 40, 0, 0 ) ** m + snowman()   

facets( 5 )      
      
m = shift( 40, 0, 0 ) ** m + snowman()     

m.write()      