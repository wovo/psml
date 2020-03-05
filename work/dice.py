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

import sys
sys.path.append( "../psml" )

from psml import *

def frame( size, width = 1, rounding = 0, outer_rounting = 0, inner_rounding = 0 ):
   return (
      rectangle( size ) 
      - dup2( width ) ** rectangle( size - 2 * dup2( width ) ) )      

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
        + box( dup3( 1 ))
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
    text = [ "TI", "AI", "BIM", "Open\nICT", "SD", "CnC" ],
    rounding = 2 )
# s = formatted_text( "Open\nICT", dup2( 20 ))
s.write()   