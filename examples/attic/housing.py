import sys
sys.path.append( "../psml" )

from psml import *
facets( 10 )   

box_size = shift( 40, 80, 20 )
rounding = 0
clearing = 4
walls    = 1

d = clearing + rounding

b = project_enclosure( box_size, walls, rounding )
#b += dup2( d ) ** repeat4( box_size - 2 * dup2( d )) ** screw_and_nut_column( box_size.z, 10, 3, walls )

   
#split_box( b, box_size, 12 ).write()
(shift( 5, 0, 0 ) **screw_and_nut_column( 20, m_screw( 3, 17 ), 1 )).write()