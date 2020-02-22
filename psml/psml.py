#============================================================================
"""
PSML

Python Solid Modeling Library:
a library for generating OpenSCAD source

home: https://www.github.com/wovo/psml

"""
#============================================================================

from __future__ import annotations
#from functools import reduce


#============================================================================
# 
# miscellaneous
#
#============================================================================

# the default number of facets for a circle and a sphere
number_of_circle_facets = 32
number_of_sphere_facets = 32

def facets( n ):
    """set the accuracy (number of facets) of circles, spheres and fonts
    
    The default setting (32) is a compromise between speed and accuracy.
    
    For quick rendering of complex designs 
    a lower value (10, or even 5) might be appropriate.
    
    This function has effect on solid elements that are created
    after its call, so better call it before you create any elements.
    """
    
    global number_of_circle_facets
    global number_of_sphere_facets
    number_of_circle_facets = n
    number_of_sphere_facets = n

def _indent( txt: string ) -> string:
    """return the text with all lines indented one indent step
    """
    return "".join( map(
        lambda s: "" if s.strip() == "" else "   " + s + "\n",
            txt.split( "\n" )
        ))

def _apply( 
    a : solid_element, 
    b : solid_element, 
    s1 : string,
    s2 : string
) -> solid_element:
    if b == None: 
       b = solid_element( "", "" )
       if a == None:
          a = b
    if s2 == None:
       s2 = s1    
    return solid_element(
        s1 + "{\n" + _indent( 
            a._positive() + "\n" + 
            b._positive() + "\n" ) +
        "}",
        s2 + "{\n" + _indent( 
            a._negative() + "\n" + 
            b._negative() + "\n" ) +
        "}",
    )             
    
    
#============================================================================
# 
# solid_element: 2d or 3d solid element
#
#============================================================================

class solid_element:
    """2D or 3D solid element
    """
    
    def __init__( self, positive : string, negative : string ):  
        """a simple solid element
        
        This constructor creates a solid element that has a 
        fixed textual representation.
        """
        self._positive_text = positive
        self._negative_text = negative
        
    def _positive( self ):
        """the OpenSCAD representation of the positive parts
        
        This method returns the OpenSCAD representation of the 
        positive parts of the solid element.
        """
        return self._merge()._positive_text

    def _negative( self ):
        """the OpenSCAD representation of the negative parts
        
        This method returns the OpenSCAD representation of the 
        negative parts of the solid element.
        """
        return self._merge()._negative_text
        
    def _merge( self ) -> element_list:
       return self    

    def __str__( self ) -> string:       
        """the OpenSCAD representation
        
        This method returns the OpenSCAD representation of the 
        solid element.
        """
        return ( self - solid_element( self._negative(), "" ))._positive()
        
    def write( self, file_name = "output.scad" ):
        """write the OpenSCAD representation to the specified file
        
        This function prints the OpenSCAD representation of the 
        solid element to the indicated file (default: output.scad).        
        That file can be opened in OpenSCAD
        for visualization or export as to a .stl file.
        
        If the file_name does not contain a "." 
        the suffix ".scad" is appended.
        """
        
        if not "." in file_name: file_name = file_name+ ".scad"
        f = open( file_name, "w" )
        f.write( str( self ) )
        f.close()       
        
    def __add__( self, rhs: solid_element ) -> solid_element:
        """add two solid elements
        
        This could be mapped directly to an OpenSCAD union(),
        but to avoid deeply nested union()s an _solid_element_list is used.
        """
        if rhs == None: return self
        return _solid_element_list( self, rhs )
            
    __radd__ = __add__            

    def __sub__( self, rhs: solid_element ) -> solid_element:
        """subtract two solid elements
        
        This maps directly to an OpenSCAD difference().
        """
        return _apply( self, rhs, "difference()", "union()" )
              
    def __mul__( self, rhs: solid_element ) -> solid_element:
        """intersect two solid elements
        
        This maps directly to an OpenSCAD intersection().        
        """
        return _apply( self, rhs, "intersection()", "union()" )       
    

class _solid_element_list( solid_element ):
    """list of solid elements
    
    This is an implementation detail.
    
    Solid elements are often constructed by adding 
    a large number of solid sub-elements.
    Using the same approach used for solid element subtraction would 
    generate deeply nested OpenSCAD unions, which makes the generated 
    OpenSCAD file difficult to read. This class 'gathers' solid elements 
    that are added, in order to generate a flattened union.
    """

    def __init__( self, a, b ):
       """create a solid element list
       
       A solid element list is created from two parts.
       Both can be either an solid_element, or an _solid_element_list.
       """
       self.list = []
       self._add( a )
       self._add( b )
       
    def _add( self, x ):
       if isinstance( x, _solid_element_list ): 
          self.list = self.list + x.list
       else:   
          self.list.append( x )       
       
    def _merge( self ) -> solid_element:    
        return solid_element( 
            "union(){\n" + 
               _indent( "".join( x._positive() for x in self.list )) +
            "}",       
            "union(){\n" + 
               _indent( "".join( x._negative() for x in self.list )) +
            "}"   
        )
       
    
#============================================================================
# 
# shift: 2d / 3d vector for shift operations
#
#============================================================================

class shift:
    """2d or 3d vector
   
    This is a 2d (x,y) or 3d (x, y, z) vector.
    A shift is used to denote a displacement (hence its name), 
    or sometimes to denote a size (for which the name is less appropriate).
    
    A shift has members x, y and z. 
    For a 2d shift, the z value is None.
    """
    
    def __init__( self, x, y = None, z = None ):
        """create from x and y, and an optional z value
        
        Create a 2d shift from x and y values, or a 
        3d shift from x, y and z values.
        
        When x is a shift, that shift is simply copied.
        """      
        if isinstance( x, shift ):
           if ( y != None ) or ( z != None ):
              raise Exception( 
                 "shift constructor called with a shift as first parameter "
                 "and some more parameters. " )
           self.x, self.y, self.z = x.x, x.y, x.z
        else:
           if y == None:
              raise "called shift with one parameter which is not a shift"
           self.x, self.y, self.z = x, y, z
        
    def _add( self, a, b ):
        """add two values, where either (but not both) could be None
        """
        if a == None: return b
        if b == None: return a      
        return a + b       
   
    def __add__( self, rhs: xyz ):
        """add two shift values (member-wise addition)
        
        Adding two 2d shifts yields a 2d shift,
        adding two 3d shifts yields a 3d shift.
        
        When a 2d shift and a 3d shift are added, the
        z value of the 2d shift is assumed to be 0.
        """   
        return shift( 
           self.x + rhs.x, 
           self.y + rhs.y, 
           self._add( self.z, rhs.z ) )
           
    def _sub( self, a, b ):
        """subtract two values, where either (but not both) could be None
        """
        if a == None: 
           if b == None: return None
           return - b
        if b == None: return a      
        return a - b               
      
    def __sub__( self, rhs: xyz ):
        """subtract two shift values (member-wise subtraction)
        
        Subtracting two 2d shifts yields a 2d shift,
        subtracting two 3d shifts yields a 3d shift.
        
        When a 2d shift and a 3d shift are subtracted, the
        z value of the 2d shift is assumed to be 0.
        """   
        return shift( 
           self.x - rhs.x, 
           self.y - rhs.y, 
           self._sub( self.z, rhs.z ) )
      
    def _mul( self, a, b ):
        """multiply two values, where either (but not both) could be None
        """
        if a == None: return None
        if b == None: return None   
        return a * b       
   
    def __mul__( self, v ):
        """multiply a shift by a scalar (member-wise multiplication)
        """   
        return shift( 
            self.x * v, 
            self.y * v, 
            self._mul( self.z, v ) )
      
    __rmul__ = __mul__      

    def __str__( self ):
        """convert to [ x, y ] or [ x, y, z ] string format
        """      
        if self.z == None:
            return "[ %f, %f ]" % ( self.x, self.y)
        else:
            return "[ %f, %f, %f ]" % ( self.x, self.y, self.z )
            
    def __pow__( self, minion : solid_element ) -> solid_element:
        """apply the shift to a solid element
        """        
        return _apply( 
           minion, None,
           "translate( %s )" % str( self ), None )
      
def dup2( v ):
   return shift( v, v )

def dup3( v ):
   return shift( v, v, v )   
   
def x2( v ):
   return shift( v, 0 )

def x3( v ):
   return shift( v, 0, 0 )

def y2( v ):
   return shift( 0, v )

def y3( v ):
   return shift( 0, v, 0 )

def z3( v ):
   return shift( 0, 0, v )
   
def right( v ):
   return shift( v, 0, 0 ) 
   
def left( v ):
   return shift( -v, 0, 0 )   
      
def back( v ):
   return shift( 0, v, 0 ) 
   
def front( v ):
   return shift( 0, -v, 0 )   
      
def up( v ):
   return shift( 0, 0, v ) 
   
def down( v ):
   return shift( 0, 0, -v )   
      
   
#============================================================================
# 
# basic 2D and 3D shapes
#
#============================================================================ 

def rectangle( x, y = 0, rounding = 0 ):
    """rectangle with either plain or rounded corners
    
    The size of the rectangle can be specified either by
    two values x and y, or by a 2d shift.
    The rounding specifies the radius of the quarter-circles
    at the corners. The default rounding is 0, which yields sharp
    corners.
    
    (OpenSCAD calls this (without the rounding) a square, 
    which is not the correct name.)
    """
    
    if isinstance( x, shift ):
       s = x
       rounding = y
    else:
       s = shift( x, y )
    
    if rounding == 0:
        return solid_element( "square( %s );" % str( s ), "" )    
        
    else:
        x, y, r = s.x, s.y, rounding
        return (
           dup2( r ) ** repeat4( s - 2 * dup2( r ) ) ** circle( r ) +
           shift( 0, r ) ** rectangle( x,         y - 2 * r ) +
           shift( r, 0 ) ** rectangle( x - 2 * r, y         ) ) 
      
def box( x, y = 0, z = 0, rounding = 0 ):
    """a box with either plain or rounded corners
        
    The size of the box can be specified either by
    three values x, y and z, or by a 3d shift.
    The rounding specifies the radius of the sphere-parts
    at the corners and the circle-shape at the edges. 
    The default rounding is 0, which yields sharp corners.
    
    (OpenSCAD calls this (without the rounding) a cube, 
    which is not the correct name.)
    """    
        
    if isinstance( x, shift ):
       s = x
       rounding = y
    else:
       s = shift( x, y, z )
    
    if rounding == 0:
        return solid_element( "cube( %s );" % str( s ), "" )
        
    else:     
        x, y, z, r = s.x, s.y, s.z, rounding
        return (
            dup3( r ) ** repeat8( s - 2 * dup3( r ) ) ** sphere( r ) +
            
            shift( 0, 0, r ) ** 
                extrude( z - 2 * r ) ** rectangle ( x, y, r ) +
                
            shift( 0, y - r, 0 ) ** rotate( 90, 0, 0 ) ** 
                extrude( y - 2 * r ) ** rectangle ( x, z, r ) + 
                
            shift( x - r, 0, 0 ) ** rotate(  0, -90, 0 ) ** 
                extrude( x - 2 * r ) ** rectangle ( z, y, r )
        )       
           
def circle( r, f = None ):
    """circle solid element
    
    Create a circle from its radius.
        
    Optionally, the number of circle facets can be specified.
    The default is the global variable number_of_circle_facets.           
    """    
        
    # number_of_circle_facets can't be the default value because
    # that would not reflect a change of number_of_circle_facets
    if f == None: f = number_of_circle_facets    
        
    return solid_element( 
        "circle( r=%f, $fn=%d );" % ( r, f ), "" ) 
     
def cylinder( r, h, f = None ):
    """cylinder solid element
    
    Create a cylinder from its radius and height
        
    Optionally, the number of circle facets can be specified.
    The default is the global variable number_of_circle_facets.
    """   
        
    # see remark in circle
    if f == None: f = number_of_circle_facets  
        
    return solid_element( 
        "cylinder( r=%f, h=%f, $fn=%d );" % ( r, h, f ), "" )

def sphere( r, f = None ):
    """sphere solid element
    
    Create a sphere from its radius and height
        
    Optionally, the number of sphere facets can be specified.
    The default is the global variable number_of_sphere_facets.
    """    
    
    # see remark in circle    
    if f == None: f = number_of_sphere_facets
    
    return solid_element(
        "sphere( r=%f, $fn=%d );" % ( r, f ), "" )             


#============================================================================
# 
# OpenSCAD modifier
#
#============================================================================
      
class extrude:
    """extrude operator: extend a 2d object in the z direction
    
    (This is the OpenSCAD linear_extrude operation.)
    """
    
    def __init__( self, z ):
        self.z = z   
         
    def __pow__( self, minion: solid_element ) -> solid_element:
        return _apply( 
           minion, None, 
           "linear_extrude( %f )\n" % self.z, None )
        
class rotate:
    """rotate operator: rotate an object around one or more axises
    
    (This is the OpenSCAD rotate operation.)
    """
    
    def __init__( self, x, y = None, z = None ):    
        if y != None:
           x = shift( x, y, z )
        self.angles = x

    def __pow__( self, minion: solid_element ) -> solid_element:   
        return _apply( 
            minion, None,
            "rotate( %s )" % str( self.angles ), None )     

class mirror:
    """mirror operator: mirror an object in one or more planes
    
    (This is the OpenSCAD mirror operation.)
    """
    
    def __init__( self, x, y = None, z = None ):    
        if y != None:
           x = shift( x, y, z )
        self.angles = x

    def __pow__( self, minion: solid_element ) -> solid_element:   
        return _apply( 
           minion, None,
           "mirror( %s )" % str( self.angles ), None )              
                    
     
#============================================================================
# 
# solid element manipulators
#
#============================================================================     
     
class _negative:
    """makes its subject a dominant negative
    
    This manipulator makes its subject a dominant negative:
    something that will not be filled.
    """

    def __pow__( self, subject: solid_element ) -> solid_element:   
       return solid_element( "", str( subject ) )
       
negative = _negative()       
           
class _positive:
    """makes its subject a dominant negative
    
    This manipulator makes its subject a dominant negative:
    something that will not be filled.
    """

    def __pow__( self, subject: solid_element ) -> solid_element:   
       return solid_element( str( subject ), "" )
       
positive = _positive()   

identity = shift( 0, 0, 0 )
           
class repeat2:
    """repeat at two positions
    
    This manipulator repeats its minion twice: once at its original
    location, and once at the indicated shift.
    """

    def __init__( self, x, y = None, z = None ):
       self.shift= shift( x, y, z )

    def __pow__( self, minion: solid_element ) -> solid_element:   
       return minion + ( self.shift ** minion )
           
class repeat4:

    def __init__( self, x, y = None ):
       if y == None:
          self.x, self.y = x.x, x.y
       else:
          self.x, self.y = x, y

    def __pow__( self, minion: solid_element ) -> solid_element:   
       return (
           shift(      0,      0 ) ** minion +
           shift( self.x,      0 ) ** minion +
           shift(      0, self.y ) ** minion +
           shift( self.x, self.y ) ** minion
       )
           
class repeat8:

    def __init__( self, x, y = None, z = None ):
       if y == None:
          self.x, self.y, self.z = x.x, x.y, x.z
       else:
          self.x, self.y, self.z, = x, y, z

    def __pow__( self, minion: solid_element ) -> solid_element:   
       return (
           shift(      0,      0,      0 ) ** minion +
           shift( self.x,      0,      0 ) ** minion +
           shift(      0, self.y,      0 ) ** minion +
           shift( self.x, self.y,      0 ) ** minion +
           shift(      0,      0, self.z ) ** minion +
           shift( self.x,      0, self.z ) ** minion +
           shift(      0, self.y, self.z ) ** minion +
           shift( self.x, self.y, self.z ) ** minion
       )
           
           
#============================================================================
# 
# derived shapes
#
#============================================================================     
     
def chisel_2d( size ) -> solid_element:
   return rectangle( size ) - dup2( size) ** circle( size )         
        
def bus( m, h, w = 1.5 ):
   return cylinder( m + 2 * w, h ) - cylinder( m, h )   
      
      

      