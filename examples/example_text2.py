import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

m = \
text( 
   "Mary had a little lamb", 
   facets = 5, 
   args = "halign='center',valign='center'" 
)
m.write()