   
      
"""
c = repeat4( 10, 30 ) ( cylinder( 5, 15 ) - cylinder( 2, 15 ) )
cx = xy( 0, 0 ) ( cylinder( 5, 15 ) - cylinder( 2, 15 ) )
extrude( 15 )( circle( 3 ) ).print( "f2.scad" )
      

pcb = xy( 78, 83 )
margin = 1
wall = 8
plate = pcb + 2 * dup2( margin ) * 2 + 2* dup2( wall )
bottom = box( set_z( plate, wall ))
bottom.print( "fx.scad" )
"""

x = rotate( 0, 90, 90 ) ** ( circle( 15 ) * rectangle( 15, 15 ) )
x = repeat4( 30, 30 ) ** ( cylinder( 5, 15 ) - cylinder( 2, 15 ) )
x = rectangle( shift( 10, 20 ), 3 )

w = 2
m = 1
pcb = shift( 78, 83 )

x = \
   ( extrude( w ) ** rectangle( pcb + 2 * dup2( m + w ), 2 ) ) + \
   ( dup2( w + m ) + shift( 4, 3 ) ) ** repeat4( 71.5, 73.5 ) ** bus( 2, 8 )

      