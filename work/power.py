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
        ch = 1

        self.shape = (
            cylinder( height = self.height, diameter = self.m_size + 2 * self.wall )
            + cone( 
               diameter1 = self.m_size + 2 * self.wall + 2 * ch,
               diameter2 = self.m_size + 2 * self.wall,
               height = ch )
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
        ch = 1
       
        self.shape = (
            cylinder( height = self.height, diameter = self.m_size + 2 * wall  ) 
           + cone( 
               diameter1 = self.m_size + 2 * self.wall + 2 * ch,
               diameter2 = self.m_size + 2 * self.wall,
               height = ch )            
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
            
            # room for a power connector barrel
            + vector( 59, -3, 8 ) ** rotate( 90, 0, 0 )
                ** cylinder( diameter = 10, height = 20 ) 
    
            # room for the screw connector
            + vector( 20, 83, 2 ) ** box( 32, 4, 16 ) 
        )    
    )   

def repeat4_within( outer, offset ):
    return modifier(
       lambda subject :
           offset ** repeat4( outer - 2 * offset ) ** subject
    )
   
def box_s3():
    wall = 1
    rounding = 1
    height = 35
    pcb_org = vector( wall + 8, wall + 3, 0 )
    pcb = pcb_s3()
    box_size = 2 * pcb_org + vector( 79, 135, height )
    screw = screw_and_nut_column( box_size.z, m3_20 )
    meter = negative ** vector( 15, 100, height + wall ) ** box( 46, 26, wall )
    switch = negative ** vector( 80, 112, height + wall ) ** cylinder( diameter = 21, height = wall )
    return (
       hollow_box( box_size, wall, rounding )
       + repeat4_within( box_size, dup2( 4 + wall ) ) ** screw
       + pcb_org ** pcb
       + meter
       + switch
       - vector( 10, 15, height + wall ) ** box( 70, 75, wall )
       - vector( 20, 12, 0 ) ** box( 56, 120, wall )
       - vector( 20, 12, 0 ) ** box( 70, 30, wall )
    )
      
s = split_box( box_s3(), vector( 110, 150, 37 ), 28 )

#sz = vector( 10, 20, 5 )
#s = split_box( box( sz ), sz, 2 )
# s = pcb_s3()  
# s = screw_and_nut_column( 35, m3_20 ) 
s.write()   


