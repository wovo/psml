difference(){
   union(){
      linear_extrude( height=3.000000, twist=0.000000, scale=1.000000, $fn=200 )
      {
         difference(){
            union(){
               translate( [ 10.000000, 0.000000 ] ){
                  square( [ 0.500000, 90.000000 ] );
               }translate( [ 20.000000, 0.000000 ] ){
                  square( [ 0.500000, 90.000000 ] );
               }translate( [ 30.000000, 0.000000 ] ){
                  square( [ 0.500000, 90.000000 ] );
               }translate( [ 40.000000, 0.000000 ] ){
                  square( [ 0.500000, 90.000000 ] );
               }translate( [ 50.000000, 0.000000 ] ){
                  square( [ 0.500000, 90.000000 ] );
               }translate( [ 60.000000, 0.000000 ] ){
                  square( [ 0.500000, 90.000000 ] );
               }translate( [ 70.000000, 0.000000 ] ){
                  square( [ 0.500000, 90.000000 ] );
               }translate( [ 80.000000, 0.000000 ] ){
                  square( [ 0.500000, 90.000000 ] );
               }translate( [ 0.000000, 10.000000 ] ){
                  square( [ 90.000000, 0.500000 ] );
               }translate( [ 0.000000, 20.000000 ] ){
                  square( [ 90.000000, 0.500000 ] );
               }translate( [ 0.000000, 30.000000 ] ){
                  square( [ 90.000000, 0.500000 ] );
               }translate( [ 0.000000, 40.000000 ] ){
                  square( [ 90.000000, 0.500000 ] );
               }translate( [ 0.000000, 50.000000 ] ){
                  square( [ 90.000000, 0.500000 ] );
               }translate( [ 0.000000, 60.000000 ] ){
                  square( [ 90.000000, 0.500000 ] );
               }translate( [ 0.000000, 70.000000 ] ){
                  square( [ 90.000000, 0.500000 ] );
               }translate( [ 0.000000, 80.000000 ] ){
                  square( [ 90.000000, 0.500000 ] );
               }
            }
            difference(){
               square( [ 90.000000, 90.000000 ] );
               translate( [ 45.000000, 45.000000 ] ){
                  circle( r=44.500000, $fn=200 );
               }
            }
         }
      }translate( [ 45.000000, 45.000000 ] ){
         rotate_extrude( angle=360.000000, convexity=2, $fn=200 )
         {
            translate( [ -45.000000, 0.000000 ] ){
               union(){
                  polygon( [ [0.000000,0.000000],[1.000000,0.000000],[1.000000,0.500000],[2.000000,1.500000],[2.000000,2.500000],[1.000000,3.500000],[1.000000,4.000000],[0.000000,4.000000], ] );
               }
            }
         }
      }
   }
   union(){
      linear_extrude( height=3.000000, twist=0.000000, scale=1.000000, $fn=200 )
      {
         union(){
            union(){
               translate( [ 10.000000, 0.000000 ] ){
               }translate( [ 20.000000, 0.000000 ] ){
               }translate( [ 30.000000, 0.000000 ] ){
               }translate( [ 40.000000, 0.000000 ] ){
               }translate( [ 50.000000, 0.000000 ] ){
               }translate( [ 60.000000, 0.000000 ] ){
               }translate( [ 70.000000, 0.000000 ] ){
               }translate( [ 80.000000, 0.000000 ] ){
               }translate( [ 0.000000, 10.000000 ] ){
               }translate( [ 0.000000, 20.000000 ] ){
               }translate( [ 0.000000, 30.000000 ] ){
               }translate( [ 0.000000, 40.000000 ] ){
               }translate( [ 0.000000, 50.000000 ] ){
               }translate( [ 0.000000, 60.000000 ] ){
               }translate( [ 0.000000, 70.000000 ] ){
               }translate( [ 0.000000, 80.000000 ] ){
               }
            }
            union(){
               translate( [ 45.000000, 45.000000 ] ){
               }
            }
         }
      }translate( [ 45.000000, 45.000000 ] ){
         rotate_extrude( angle=360.000000, convexity=2, $fn=200 )
         {
            translate( [ -45.000000, 0.000000 ] ){
               union(){
                  difference(){
                     polygon( [ [0.000000,3.500000],[1.000000,2.500000],[1.000000,1.500000],[0.000000,0.500000], ] );
                  }
               }
            }
         }
      }
   }
}