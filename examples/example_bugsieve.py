import sys
sys.path.append( "../psml" )

try:
   from typeguard.importhook import install_import_hook
except:
   print( "missing dependency, please install typeguard:" )
   print( "   (linux) sudo pip install typeguard" )
   print( "   (windows) python -m pip install typeguard" )
   exit( -1 )
   
install_import_hook( 'psml' )

import psml

def square_grid( size, spacing, thickness ):
   m = None 
   for x in range( spacing, size.x, spacing ):
      m += psml.vector( x, 0 ) ** psml.rectangle( thickness, size.y )
   for y in range( spacing, size.y, spacing ):
      m += psml.vector( 0, y ) ** psml.rectangle( size.x, thickness )
   return m      
   
def hexagonal_grid( size, spacing, thickness ):
   s = 10
   psml.rectangle( x, size.y )
   return m      
   
psml.facets( 200 )
   
def bug_sieve(
   sieve_height    = 3,
   sieve_diameter  = 90,
   wall_thickness  = 1,
   groove_depth    = 1,
   grid_gap        = 10,
   grid_thickness  = 0.5
):
   # the sieve grid   
   m = square_grid( psml.vector( sieve_diameter, sieve_diameter ), grid_gap, grid_thickness )
   
   # remove what is outside the rim
   m -= psml.rectangle( psml.dup2( sieve_diameter )) - \
      psml.dup2( sieve_diameter / 2 ) ** psml.circle( diameter = sieve_diameter - wall_thickness )
      
   # make grid 3D      
   m = psml.extrude( sieve_height ) ** m   
   
   # wall with groove 2D
   h = ( sieve_height - 2 * groove_depth ) / 2
   g = groove_depth
   w = wall_thickness
   wall_2d = psml.polygon( [
      psml.vector( 0, 0 ), psml.vector( w, 0 ), 
      psml.vector( w, h ), psml.vector( w + g, h + g ), 
      psml.vector( w + g, h + 2 * g ), psml.vector( w, h + 3 * g ), 
      psml.vector( w, 2 * h + 3 * g ), psml.vector( 0, 2 * h + 3 * g ) ] )
   wall_2d += psml.negative ** psml.polygon( [
      psml.vector( 0, h + 3 * g ), psml.vector( g, h + 2 * g ), 
      psml.vector( g, h + g ), psml.vector( 0, h ) ] )          
   
   # rotate wall to 3D and add to sieve
   m += psml.dup2( sieve_diameter / 2 ) ** \
      psml.rotate_extrude() ** psml.vector( - sieve_diameter / 2, 0 ) ** wall_2d
      
   return m
   
   
      
m = bug_sieve()
m.write()