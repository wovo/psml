import sys
sys.path.append( "../psml" )

from psml import *
#facets( 10 )   

box_size = shift( 10, 20, 5 )
rounding = 1
clearing = 1
radius = 0.5
walls = 0.5

d = clearing + radius

def screw_and_nut_column( h, s, m = 3, w = 1 ):
    """a screw and nut column
    
    :param h: height of the column
    :param s: screw thread length (15 for an m3x15)    
    :param m: screw diameter (default: 3 for m3)
    :param 2: wall thickness (default 1mm)   
    
    This is a vertical screw-and-nut column for keeping two parts 
    of an enclosure together. 
    It is assumed to be spliced into the top and bottom parts.
    """

    r = None
    
    # 4/5'th of the m size seems to be a good estimate
    # of the size of the screw recess  diameter
    sh = ( 4.0 / 5.0 ) * m
    nh = m

    # recess for the crew head   
    r += up( h ) ** rotate( 180, 0, 0 ) ** \
        ( cylinder( w + 2 * m / 2, sh + w ) - 
            negative ** cylinder( 2 * m / 2, sh ))

    # cylinder for the screw shaft
    r += cylinder( w + m / 2, h ) - negative ** cylinder( m / 2, h )
   
    # recess for the nut
    r+= ( cylinder( w + 2 * m / 2, nh + w ) - 
         negative ** cylinder( 2 * m / 2, sh, f = 6 ))
   
   return r

b = box( box_size, rounding ) - shift( dup3( walls )) ** box( box_size - 2 * dup3( walls ))
b -= dup2( d ) ** repeat4( box_size - 2 * dup2( d )) ** screw_and_nut_column( 3, 1, box_size.z )

def splice( b, s, h ):
   r = None
   r = ( shift( s.x + 5, 0, 0 ) ** r ) + \
       ( b - ( shift( 0, 0, h ) ** box( s )))
   r = ( shift( s.x + 5, 0, 0 ) ** r ) + \
       shift( s.x, 0, s.z ) ** rotate( 0, 180, 0 ) ** ( b - box( s.x, s.y, h ))
   return r
   
splice( b, box_size, 3 ).write()
screw_and_nut_column( 3, 1, 20 ).write()