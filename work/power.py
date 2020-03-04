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
      
      peg = support_screw( self.height, m )
      self.shape = (
          box( size.x, size.y, 1 ) 
          + corner_hole ** up( 1 ) ** repeat4( self.hole_square ) ** peg.shape )
            
   

def pcb_s3( dist = 6 ):

    dist = 10

    return (
        pcb_four(
            size = vector( 78.5, 83 ),
            corner_hole = vector( 3.25, 5 ),
            hole_square = vector( 72, 75 ), 
            height = dist ).shape   
            
        + up( dist ) ** negative ** (
        
            # room for the shrouded 10 pin connector
            vector( 21, -3, 2 ) ** box( 18, 4, 8 )    
    
            # room for the power connector
            + vector( 55, -3, 2 ) ** box( 8, 2, 12 ) 
    
            # room for the screw connector
            + vector( 20, 83, 2 ) ** box( 32, 4, 16 ) 
        )    
    )   
   
def box_s3():
    w = 1
    org = vector( w, w, w ) + vector( 1, 1, 0 )
    return (
       hollow_box( 2 * org + vector( 80, 85, 40 ), w, 1 )
       + org ** pcb_s3()
    )
      

s = split_box( box_s3(), vector( 85, 90, 45 ), 15 )

sz = vector( 10, 20, 5 )
s = split_box( box( sz ), sz, 2 )
   
s.write()   


