import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

m = None

x = (
    cylinder( radius = 5, height = 20 ) +
    up( 20 ) ** 
    (
        sphere( radius = 8 ) +
        vector( -5, -8, 4 ) ** box( 3, 5, 3 ) +
        vector(  2, -8, 4 ) ** box( 5, 5, 3 ) +
        vector(  0,  0, 3 ) ** rotate( 90, 0, 0 ) 
           ** cylinder( radius = 1, height = 12 )
    )    
)    

m = right( 20 ) ** m + resize( 15, 15, 15 ) ** x
m = right( 20 ) ** m + scale( 1, 2, 2 ) ** x
m = right( 20 ) ** m + mirror( 1, 0, 0 ) ** x
m = right( 25 ) ** m + rotate( -30, 0, 0 ) ** x
m = right( 15 ) ** m + vector( 0, 0, 10 ) ** x
m = right( 20 ) ** m + x

m.write()