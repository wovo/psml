import sys
sys.path.append( "../psml" )

from psml import *

def frame( size, width ):
   return (
      rectangle( size ) 
      - dup2( width ) ** rectangle( size - 2 * dup2( width ) ) )      

def formatted_text( txt, size, margin = 4 ):
    split = txt.split( "\n" )
    n = len( split )
    if n > 1:
        r = None
        for t in split:
           r = ( 
              back( size.y / n ) ** r
              + formatted_text( t, vector( size.x, size.y / n ) ) )
        return r
    else:
        fs = 1
        return (
            extrude( 1 ) ** (
                dup2( margin ) 
                    ** resize( size - 2 * dup2( margin ))) 
                        ** text( txt, 10 )
            + frame( size, fs ) )

def dice( size, text, rounding = 0 ):
    shift = 2
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
        
# s = dice( 35, [ "TI", "AI", "BIM", "Open\nICT", "SD", "CnC" ] )
s = formatted_text( "Open\nICT", dup2( 20 ))
s.write()   