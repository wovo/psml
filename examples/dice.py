import sys
sys.path.append( "../psml" )

from psml import *

class text( solid_element ):
   def __init__( self, t, s ):
      solid_element.__init__( self, 
         'text( "%s", %f, halign = "center", valign = "center" );'
            % ( t, s ), ""
      )   

def dice_text1( n, t, f, r ):
   return (
      shift( n / 2.0, n / 2.0, 0 ) ** 
         extrude( 1 ) **
            text( t, ( ( n - r ) * f ) / 100 ))

def dice_text2( n, t1, t2, f, r ):
   return (  
      shift( n / 2.0, 7.0 * n / 10.0, 0 ) **
         extrude( 1 ) **
            text( t1, ( ( n - r ) * f ) / 100 ) + 
      shift( n / 2.0, 3.5 * n / 10.0, 0 ) **
         extrude( 1 ) **    
            text( t2, ( ( n - r ) * f ) / 100 )
   )            

def dice( s, r = 0 ):
   return box( dup3( s ), r) - (
      shift( s, 0, 0 ) ** mirror( 1, 0, 0 ) **
         dice_text1( s, "TI", 62, r ) +
      shift( s, s - 1, 0 ) ** rotate( 90, 0, 180 ) **
         dice_text1( s, "CSC", 25, r ) +
      shift( s - 1, 0, s ) ** rotate( 0, 90, 0 ) **
         dice_text1( s, "SD", 38, r ) +
      shift( 1, 0, 0 ) ** rotate( 0, -90, 0 ) **
         dice_text1( s, "BIM", 32, r ) +
      shift( 0, 1, 0 ) ** rotate( [ 90, 0, 0 ] ) **
         dice_text1( s, "AI", 65, r ) +
      shift( 0, 0, s - 1 ) **
         dice_text2( s, "Open", "ICT", 22, r )
   )

dice( 30, 3 ).write()