#============================================================================
"""
PSML

Python Solid Modeling Library for generating OpenSCAD source

home: https://www.github.com/wovo/psml

ToDo
- simplify shift arguments
- tests??
- readme.md
- manual
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

def draft( n = 10 ):
    """set the accuracy of circles, spheres and fonts
    
    The default is a compromise between speed and accuracy.
    For quick rendering of complex designs 
    the default value of 10 might be a good choice.
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
    
    
#============================================================================
# 
# solid_element: 2d or 3d solid element
#
#============================================================================

class solid_element:
    """2D or 3D solid element
    """
    
    def __init__( self, txt : string ):  
        """a (simple) solid element
        
        This constructor creates a solid element that has a 
        fixed OpenSCAD representation.
        """
        self.txt = txt

    def __str__( self ) -> string:       
        """the OpenSCAD representation
        
        This method returns the OpenSCAD representation of the 
        solid element.
        """
        return self.txt    
        
    def write( self, file_name = "output.scad"):
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
        if rhs == None: return self
        return solid_element( 
            "difference(){\n" + _indent( 
                str( self ) + "\n" + 
                str( rhs ) + "\n" ) +
            "}" )
              
    def __mul__( self, rhs: solid_element ) -> solid_element:
        """intersect two solid elements
        
        This maps directly to an OpenSCAD intersection().        
        """
        if rhs == None: return self
        return solid_element( 
            "intersection(){\n" + _indent( 
                str( self ) + "\n" + 
                str( rhs ) + "\n" ) +
            "}" )        
    

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
       
    def __str__( self ) -> string:    
        """the OpenSCAD representation
        
        This method returns the OpenSCAD representation of the 
        _solid_element_list, which is the union() of all solid elements
        in the list.
        """
        return ( 
            "union(){\n" + 
               _indent( "".join( str( x ) for x in self.list )) +
            "}" )       
       
    
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
            
    def __pow__( self, m : solid_element ) -> solid_element:
        """apply the shift to a solid element
        """        
        return solid_element(
           ( "translate( %s )\n" % str( self ) ) +
               _indent( str( m ) ) )
      
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
        return solid_element( "square( %s );" % str( s ))    
        
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
        return solid_element( "cube( %s );" % str( s ))
        
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
           
class circle( solid_element ): 
    """circle solid element
    
    (This is the OpenSCAD circle.)
    """
    
    def __init__( self, r, f = None ):
        """create a circle from its radius
        
        Optionally, the number of circle facets can be specified.
        The default is the global variable number_of_circle_facets.           
        """    
        
        # number_of_circle_facets can't be the default value because
        # that would not reflect a change of number_of_circle_facets
        if f == None: f = number_of_circle_facets    
        
        solid_element.__init__( self, 
            "circle( r=%f, $fn=%d );" % ( r, f ))          
     
class cylinder( solid_element ): 
    """cylinder solid element
    
    (This is the OpenSCAD cylinder.)
    """
    
    def __init__( self, r, h, f = None ):
        """create a cylinder from its radius and height
        
        Optionally, the number of circle facets can be specified.
        The default is the global variable number_of_circle_facets.
        """   
        
        # see remark in circle
        if f == None: f = number_of_circle_facets  
        
        solid_element.__init__( self, 
            "cylinder( r=%f, h=%f, $fn=%d );" % ( r, h, f ))      

class sphere( solid_element ): 
    """sphere solid element
    
    (This is the OpenSCAD sphere.)
    """
    
    def __init__( self, r, f = None ):
        """create a sphere from its radius and height
        
        Optionally, the number of sphere facets can be specified.
        The default is the global variable number_of_sphere_facets.
        """    
        if f == None: f = number_of_sphere_facets
        solid_element.__init__( self, 
            "sphere( r=%f, $fn=%d );" % ( r, f ))             


#============================================================================
# 
# OpenSCAD operators
#
#============================================================================
      
class extrude:
    """extrude operator: extend a 2d object in the z direction
    
    (This is the OpenSCAD linear_extrude operation.)
    """
    
    def __init__( self, z ):
        self.z = z   
         
    def __pow__( self, minion: solid_element ) -> solid_element:
        return solid_element( 
            ( "linear_extrude( %f )\n" % self.z ) +
                _indent( str( minion ) ) )
        
class rotate:
    """rotate operator: rotate an object around one or more axises
    
    (This is the OpenSCAD rotate operation.)
    """
    
    def __init__( self, x, y = None, z = None ):    
        if y != None:
           x = shift( x, y, z )
        self.angles = x

    def __pow__( self, minion: solid_element ) -> solid_element:   
        return solid_element( 
            ( "rotate( %s )\n" % str( self.angles ) ) +
                _indent( str( minion ) ) )        
                    
     
#============================================================================
# 
# solid element manipulators
#
#============================================================================     
     
class repeat2:
    """"repeat at two positions
    
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
      
      

      