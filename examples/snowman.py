import sys
sys.path.append( "../psml" )

from psml import *
( sphere( 15 ) + 
  shift( 0, 0, 18 ) ** (
      sphere( 10 ) +
      rotate( 90, 0, 0 ) ** cylinder( 2, 15 ))).write()