import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

c = cylinder( radius = 10, height = 30 ) + vector( -10, -20, 0 ) \
   ** box( 20, 20, 5 )
m = (
    c + 
    right(  30 ) ** rotate( 45, 0,  0 ) ** c +
    right(  60 ) ** rotate( 0, 45,  0 ) ** c +
    right( 100 ) ** rotate( 0,  0, 45 ) ** c 
)
m.write()