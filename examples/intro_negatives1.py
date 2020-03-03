import sys
sys.path.append( "../psml" )

from typeguard.importhook import install_import_hook
install_import_hook('psml')

from psml import *

def pipe( r, l, f ):
   return (
      cylinder( radius = r, height = l ) 
      - f ** cylinder ( radius = r - 1, height = l ) )

def cross( f1 = identity, f2 = identity ):
   p = vector( 0, 0, -15 ) ** pipe( 10, 30, f1 )
   c = p + rotate( 90, 0, 0 ) ** p 
   m = f2 ** c + vector( 0, -12, -15 ) ** cylinder( radius = 2, height = 30 )
   return m
      
m = cross() 
m += vector( 30, 0, 0 ) ** cross( negative )
m += vector( 60, 0, 0 ) ** cross( negative, positive )
   
m.write()