import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

m = (
MediumVioletRed ** sphere( radius = 10 ) +
right( 30 ) ** blue ** sphere( radius = 10 ) +
right( 60 ) ** mediumspringgreen ** sphere( radius = 10 )
)
m.write()