import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

( sphere( radius = 15 ) + 
  vector( 0, 0, 18 ) ** (
      sphere( radius = 10 ) +
      rotate( 90, 0, 0 ) ** cylinder( radius = 2, height = 15 ))).write()