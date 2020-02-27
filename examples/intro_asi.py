import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

m = None

a = down( 10 ) ** cylinder( 5, 20 )
b = rotate( 90, 0, 0 ) ** a 

m = right( 20 ) ** m + ( a * b )
m = right( 20 ) ** m + ( a - b )
m = right( 20 ) ** m + ( a + b )
m = right( 20 ) ** m + b
m = right( 20 ) ** m + a

m.write()