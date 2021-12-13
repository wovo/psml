import sys
sys.path.append( "../psml" )

from psml import *  

class composite:
   def __init__( self ):
      self.components = []
      
   def add( self, c : component ):
      self.components.add( c )
      
   def write( self, file_name = "output" ):
      self._shape().write( output )

   def stl( self, file_name = "output" ):   
      self._shape().stl( output )
      
def component:
   def __init__( self, bounding_box ):
      self.box = bounding_box

class blue_pill : component

   def _shape( self ):
      
    