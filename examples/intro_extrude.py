import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

cross = vector( -5, -15 ) ** rectangle( 10, 30 )
cross = cross + rotate( 0, 0, 90 ) ** cross     

m = (
   right(   0 ) ** extrude( 50 ) ** cross +
   right(  50 ) ** extrude( 50, 90 ) ** cross +
   right(  90 ) ** extrude( 50 ) ** circle( radius = 5 ) +
   right( 120 ) ** extrude( 50, 720 ) ** right( 5 ) ** circle( radius = 5 )
)   
   
m.write()