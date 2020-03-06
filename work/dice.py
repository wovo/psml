# engrave
# make text frame optional
# 2 text functions?
# general frame, with rounding (inner & outer)?
# pass text parameters
# dice: engrave or emboss?
# height as part of the size?
# engrave depth as dice parameter
# dice6
# within modifier? scales?
# no-border seems to work the wrong way round: the text gets smaller

import sys
sys.path.append( "../psml" )

from psml import *

def _select_not_none( list, default ):
   for x in list:
      if x != None:
          return x
   return default       

def frame( 
   size : vector, 
   width: float = 1, 
   rounding  = 0
) -> shape:
    """a 2D or 3D frame
    
    This function returns a 2D or 3D frame.
    
    A 2D frame can have have sharp or rounded corners.
    The rounding can be specified separately 
    for the inside and the outside.
    
    A 3D frame can have either square or circular bars.
    """
    
    if size.z == None:
    
        # 2D frame
        if isinstance( rounding, vector ):
            outer_rounding, inner_rounding = rounding.x, rounding.y
        else:     
            outer_rounding, inner_rounding = rounding, rounding
        
        return (
            rectangle( 
                size, 
                rounding = outer_rounding ) 
            - dup2( width ) ** rectangle( 
                size - 2 * dup2( width ),
                rounding = inner_rounding ) )
    
    else:
    
        # 3D frame
        if rounding:
            corner = sphere( diameter = width )
            bar_x = cylinder( diameter = width +2 , height = size.x - width )
            bar_y = cylinder( diameter = width +2 , height = size.y - width )
            bar_z = cylinder( diameter = width +2, height = size.z - width )
        else:
           corner = vector( dup3( - width / 2.0 ) ) ** box( dup3( width ))
           bar_x = dup2( - width / 2.0 ) ** box( width, width, size.x - width )
           bar_y = dup2( - width / 2.0 ) ** box( width, width, size.y - width )
           bar_z = dup2( - width / 2.0 ) ** box( width, width, size.z - width )
        return (
            repeat8( size - dup3( width ) ) ** corner
            + rotate( 0, 90, 0 ) ** repeat4( - size.z + width, size.y - width,  ) ** bar_x
            + rotate( -90, 0, 0 ) ** repeat4( size.x - width, - size.z + width,  ) ** bar_y
            + repeat4( size.x - width, size.y - width ) ** bar_z
        )    


def formatted_text( txt, size, margin = 3, fr = 1, height = 1 ):

    if height > 0:
       return extrude( height ) ** (
           formatted_text( txt, size, margin, fr, 0 ) )
          
    if fr > 0:
       return frame( size, fr ) + (
           formatted_text( txt, size, margin, 0, 0 ) )

    if margin > 0:
       return dup2( margin ) ** (
           formatted_text( txt, size - 2 * dup2( margin ), 0, 0, 0 ) )
        
    split = txt.split( "\n" )
    n = len( split )
    
    if n > 1:
        r = None
        dist = 2
        for line in split:
           r = ( 
              back( size.y / n + dist ) ** r
              + formatted_text( 
                  line, 
                  vector( size.x, ( size.y / n ) - dist * ( n - 1 ) ), 
                  0, 0, 0 ) )
        return r                  
        
    else:
        return resize( size ) ** text( txt, 10 )
     

def dice( size, text, rounding = 0 ):
    shift = 3
    ts = size - 2 * shift
    ts2 = dup2( ts )
    return (
        box( dup3( size ), rounding = rounding )
        - vector( size - shift, shift, 0 ) ** mirror( 1, 0, 0 ) 
            ** formatted_text( text[ 0 ], ts2 )
        - vector( size - shift, size - 1 , shift ) ** rotate( 90, 0, 180 ) 
            ** formatted_text( text[ 1 ], ts2 )
        - vector( size - 1, shift, size - shift ) ** rotate( 0, 90, 0 ) 
            ** formatted_text( text[ 2 ], ts2 )
        - vector( 1, shift, shift ) ** rotate( 0, -90, 0 ) 
            ** formatted_text( text[ 3 ], ts2 )
        - vector( shift, 1, shift ) ** rotate( 90, 0, 0 ) 
            ** formatted_text( text[ 4 ], ts2 )
        - vector( shift, shift, size - 1 )  
            ** formatted_text( text[ 5 ], ts2 )
    )      
        
s = dice( 
    size = 35, 
    text = [ "TI", "AI", "BIM", "Open\nICT", "SD", "CSC" ],
    rounding = 1 )
s = formatted_text( "Open\nICT", dup2( 20 ))
# s = box( 10, 20, 5 )
# s.stl( "dobbelsteen-35" )   

s = frame( vector( 10, 20, 30 ), 4, 1 )
 
s.write()