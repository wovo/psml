# support for the 3 * LiPo pack

import sys
sys.path.append( "../psml" )

from psml import *

# a support

class support_screw:
    """
    """
    
    def __init__( self, height, m_size = 3, wall = 1 ):
        self.height = height
        self.m_size = m_size
        self.wall = wall
       
        self.shape = (
            cylinder( height = self.height, diameter = self.m_size + 2 * self.wall, ) 
            - negative ** cylinder( height = self.height, diameter = m_size ) )
        
class support_peg:
    """
    """
    
    def __init__( self, height, m_size = 3, wall = 1, peg_height = 2, rounded_top = True ):
        self.height = height
        self.m_size = m_size
        self.wall = wall
        self.peg_height = peg_height
        self.rounded_top = rounded_top
       
        self.shape = (
            cylinder( height = self.height, diameter = self.m_size + 2 * wall  ) 
            + up( self.height ) 
                ** cylinder( 
                    height = peg_height, 
                    diameter = self.m_size, 
                    rounded_top = rounded_top ) )

class pcb_four:

   def __init__( 
      self, 
      size, 
      corner_hole, 
      hole_square, 
      height = 5, 
      m = 3 
   ):
      self.size = size
      self.corner_hole = corner_hole
      self.hole_square = hole_square
      self.height = height
      self.m = m
      
      peg = support_peg( self.height, m )
      self.shape = (
          box( size.x, size.y, 1 ) 
          + corner_hole ** up( 1 ) ** repeat4( self.hole_square ) ** peg.shape )
            
   

pcb_s3 = pcb_four(
   size = vector( 78, 83 ),
   corner_hole = vector( 3, 5 ),
   hole_square = vector( 72, 73 ) )   
   
   

def bus( d, h, w = 2 ):
   return cylinder( d + w, h ) - cylinder( d, h )

#x = \
#   ( extrude( w ) ** rectangle( pcb + 2 * dup2( m + w ), rounding = 2 ) ) + \
#   ( dup2( w + m ) + vector( 4, 3 ) ) ** repeat4( 71.5, 73.5 ) ** bus( 2, 8 )
   
pcb_s3.shape.write()   





      