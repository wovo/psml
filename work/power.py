# support for the 3 * LiPo pack

import sys
sys.path.append( "../psml" )

from psml import *

# a support

class support_screw:
    """
    """
    
    def __init__( self, height, m_size = 3, wall = 2 ):
        self.height = height
        self.m_size = m_size
        self.wall = wall
       
    def shape( self ):
        return (
            cylinder( self.m_size + self.wall, self.height ) 
            - negative ** cylinder( m, h ) )
        
class support_peg:
    """
    """
    
    def __init__( self, height, m _size = 3, wall = 2, peg_height = 2, rounded_top = True ):
        self.height = height
        self.m_size = m_size
        self.wall = wall
        self.peg_height = peg_height
        self.rounded_top = rounded_top
       
    def shape( self ):
        return (
            cylinder( self.m_size + self.wall, self.height ) 
            + up( self.height ) 
                ** cylinder( 
                    self.m_size, 
                    peg_height - self.m_size, 
                    rounded_top = rounded_top ) )
 
# pattern

class pcb:

   def __init__( 
      self, 
      size, 
      screw_corner, 
      screw_distance, 
      hight = 5, 
      m = 3 
   ):
      self.size = size
      self.screws = screws
      self.height = hight
      self.m = m
      
   def shape( self ):      
      return 
            
   

w = 1
m = 1
pcb = vector( 78, 83 )

def bus( d, h, w = 2 ):
   return cylinder( d + w, h ) - cylinder( d, h )

x = \
   ( extrude( w ) ** rectangle( pcb + 2 * dup2( m + w ), rounding = 2 ) ) + \
   ( dup2( w + m ) + vector( 4, 3 ) ) ** repeat4( 71.5, 73.5 ) ** bus( 2, 8 )
   
x.write()   

      