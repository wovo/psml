import sys
sys.path.append( "../psml" )

from psml import *

def pipe( r, l, f ):
   return cylinder( r, l ) - f ** cylinder ( r - 1, l )

def cross( f1 = identity, f2 = identity):
   p = shift( 0, 0, -15 ) ** pipe( 10, 30, f1 )
   c = p + rotate( 90, 0, 0 ) ** p 
   m = f2 ** c + shift( 0, -12, -15 ) ** cylinder( 2, 30 )
   return m
      
m = cross() 
m += shift( 30, 0, 0 ) ** cross( negative )
m += shift( 60, 0, 0 ) ** cross( negative, positive )
   
m.write()