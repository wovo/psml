#============================================================================
"""
a library for generating OpenSCAD_ 3D models

https://www.github.com/wovo/psml

\(c) Wouter van Ooijen (wouter.vanooijen@hu.nl)

Distributed under the Boost Software License, Version 1.0.

.. _OpenSCAD: https://www.openscad.org/
.. _typeguard: https://pypi.org/project/typeguard/

-----------------------------------------------------------------------------

This is a Python library (Python 3 required) for writing
3D model code that can be rendered and processed by OpenSCAD_.

The library has a vector class.
A vector holds x, y and (optional) z numeric values.
A vector is used to specify (in 2D or 3D) a size, 
a location, or a displacement, or sometimes just to hold 2 or 3 values.
A vector can be created from two or three values.
Two vectors can be added or subtracted.
A vector can multiplied with or divided by a numeric value.
When a function requires a vector, it can in most
cases be specified either by a vector value, or as 2 or 3
individual numeric parameters.

This library creates and manipulates 3D solid objects. 
The image below shows the basic solid objects:
box, cylinder, cone, and sphere.

.. figure::  ../examples/images/intro_bccs_128.png

Basic flat (2D) objects are rectangle, circle, polygon, and text,
as shown in the next image.

.. figure::  ../examples/images/intro_rcpt_128.png
    :target: ../examples/images/intro_rcpt_512.png

A flat object can be extended into a solid object
by extruding it (in the z direction), while
optionally twisting it around the z axis in the process.
The cross shown below was extruded and twisted while
it was at the origin. The right circle was extruded and twisted
while it was just to the right of the origin.

.. figure::  ../examples/images/intro_extrude_128.png
    :target: ../examples/images/intro_extrude_512.png
    
Objects and be added, subtracted and intersected 
with the operators +, - and \*.
The image below shows two separate cylinders, the addition of
these two cylinders, the second cylinder subtracted from the
first one, and the intersection of the two. 

.. figure::  ../examples/images/intro_asi_128.png
    :target: ../examples/images/intro_asi_512.png

Manipulators can be applied to an object with the ** (power) operator.
Basic manipulators are vector, rotate, mirror, scale and resize.
The example below show an object unchanged, , shifted up, 
rotated along the x axis, mirrored in the y-z plane (note the eyes), 
scaled (by 2 in the y and z directions), and resized
(to fit in a cube).


.. figure::  ../examples/images/intro_vrmsr_128.png
    :target: ../examples/images/intro_vrmsr_512.png

The repeat2, repeat4 and repeat8 manipulators repeat their subject.
Repeat2 does this at the original location, 
and shifted by the specified vector.
Repeat4 does this at the 4 corners of the rectangle
specified by the vector.
Repeat8 does this at the 8 corners of the box
specified by the vector.

.. figure::  ../examples/images/intro_repeat1_128.png
    :target: ../examples/images/intro_repeat1_512.png

The negative manipulator creates a dominant emptiness from its subject.
The image below shows at the left the addition of two normal pipes.
The result is not a usable pipe crossing because the walls of each 
pipe will block the other pipe.
In the middle it shows the addition of two pipes of which the empty
interior is dominant. This produces a 'successful' pipe crossing.
But this also removes part of the vertical axle.
At the right the crossing was first made positive, which
reduces the dominant emptiness to an normal, and then the
vertical axle was added.

.. figure::  ../examples/images/intro_negatives1_128.png
    :target: ../examples/images/intro_negatives1_512.png

In the code examples solid objects are created.
What is not show is that such an object must be written to a 
file to be processed by OpenSCAD, using a write() call.

This documentation is meant to be usable on its own, 
without having to read the OpenSCAD documentation,
hence it is worded as if the library provides all the 
functionality, while in fact it is in most cases just a thin layer 
on top of the OpenSCAD language.

Some OpenSCAD features are not directly available in the library.
To compensate, a solid can be created from a string, which
is passed directly to OpenSCAD. 
Likewise, a manipulator can be constructed from a lambda, which
gets the string representation of its subject as parameter.

The library has type hints. 
The examples use typeguard_ to check these hints.

-----------------------------------------------------------------------------

"""
#============================================================================

from __future__ import annotations
from typing import Union, Tuple, Iterable

# specifiers used in the type annotations
_shape_or_shape_list = Union[ "shape", "_shape_list" ]
_shape_or_none = Union[ "shape", None ]
_str_or_none = Union[ str, None ]
_float_or_vector = Union[ float, "vector" ]
_float_or_none = Union[ float, None ]
_vector_or_pair = Union[ "vector", Tuple[float,float]]
           

#============================================================================
# 
# miscellaneous
#
#============================================================================

# the default number of facets for a circle and a sphere
number_of_circle_facets   = 32
number_of_sphere_facets   = 32
number_of_text_facets     = 32
number_of_extrude_facets  = 32

def facets( numer_of_facets: int ) -> None:
    """accuracy (number of facets) of circles, spheres and fonts
    
    The default setting (32) is a compromise between speed and accuracy.
    
    For quick rendering of complex designs 
    a lower value (10, or even 5) might be appropriate.
    
    This function has effect on shapes that are created
    after its call, so better call it before you create any elements.
    
    .. figure::  ../examples/images/example_facets1_128.png    
        :target: ../examples/images/example_facets1_512.png  
    .. literalinclude:: ../examples/example_facets1.py
        :lines: 10
    
    .. figure::  ../examples/images/example_facets2_128.png 
        :target: ../examples/images/example_facets2_512.png  
    .. literalinclude:: ../examples/example_facets2.py
        :lines: 9,11 
    """
    
    global number_of_circle_facets
    number_of_circle_facets = numer_of_facets
    
    global number_of_sphere_facets
    number_of_sphere_facets = numer_of_facets
    
    global number_of_text_facets
    number_of_text_facets = numer_of_facets

    global number_of_extrude_facets
    number_of_extrude_facets = numer_of_facets

def _indent( txt: str ) -> str:
    """return the text with all lines indented one indent step
    """
    return "".join( map(
        lambda s: "" if s.strip() == "" else "   " + s + "\n",
            txt.split( "\n" )
        ))

def _apply( 
    a : _shape_or_none, 
    b : _shape_or_none, 
    s1 : str,
    s2 : _str_or_none
) -> shape:
    """
    apply an OpenSCAD operation to one or two shapes
    """
    if b == None: 
       b = shape( "", "" )
       if a == None:
          a = b
    if s2 == None:
       s2 = s1    
    return shape(
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
# shape
#
#============================================================================

class shape:
    """2D or 3D shape
    
    Shapes can be added, subtracted or intersected by using the
    +, - or * operators.
    """
    
    def __init__( self, 
       positive : str, 
       negative : str = "" 
    ):  
        """a simple shape
        
        :param positive: the OpenSCAD text representation 
                         of the positive parts
        :param negative: (optional) the OpenSCAD text representation 
                         of the dominant negative parts
        
        This constructor creates a shape that has a 
        fixed textual representation.
        """
        self._positive_text = positive
        self._negative_text = negative
        
    def _merge( self ) -> shape:
       """hook for shape_list
       """
       return self    

    def _positive( self ):
        """the OpenSCAD text representation of the positive parts
        
        This method returns the OpenSCAD representation of the 
        positive parts of the shape.
        """
        return self._merge()._positive_text

    def _negative( self ):
        """the OpenSCAD text representation of the dominant negative parts
        
        This method returns the OpenSCAD representation of the 
        dominant negative parts of the shape.
        """
        return self._merge()._negative_text
        
    def __str__( self ) -> str:       
        """the OpenSCAD text representation of the shape
        
        This method returns the OpenSCAD representation of the 
        shape.
        """
        return ( self - shape( self._negative(), "" ))._positive()
        
    def write( self, file_name = "output.scad" ):
        """write the shape to the specified file
        
        :param file_name: name of the file        
        
        This function prints the OpenSCAD representation of the 
        shape to the indicated file (default: output.scad).        
        That file can be opened in OpenSCAD
        for visualization or export as to a .stl file.
        
        If the file_name does not contain a "." 
        the suffix ".scad" is appended.
        
        .. code-block:: 
    
            # these lines have the same effect
            sphere( 10 ).write()
            sphere( 10 ).write( "output" )
            sphere( 10 ).write( "output.scad" )
        """
        
        if not "." in file_name: file_name = file_name+ ".scad"
        f = open( file_name, "w" )
        f.write( str( self ) )
        f.close()       
        
    def __add__( self, rhs: _shape_or_none ) -> shape:
        """add two shapes
        
        This could be mapped directly to an OpenSCAD union(),
        but to avoid deeply nested union()s an _shape_list is used.
        """
        if rhs == None: return self
        return _shape_list( self, rhs )
            
    __radd__ = __add__            

    def __sub__( self, rhs: _shape_or_none ) -> shape:
        """subtract two shapes
        """
        if rhs == None: return self        
        return _apply( self, rhs, "difference()", "union()" )
              
    def __mul__( self, rhs: shape ) -> shape:
        """intersect two shapes  
        """
        return _apply( self, rhs, "intersection()", "union()" )       
    
class _shape_list( shape ):
    """list of shapes
    
    This is an implementation detail.
    
    Shapes are often constructed by adding 
    a large number of solid sub-elements.
    Using the same approach used for shape subtraction would 
    generate deeply nested OpenSCAD unions, which makes the generated 
    OpenSCAD file difficult to read. This class 'gathers' shapes 
    that are added, in order to generate a flattened union.
    """

    def __init__( self, 
        a: _shape_or_shape_list, 
        b: _shape_or_shape_list 
    ):
       """create a shape list
       
       A shape list is created from two parts.
       Both can be either an shape, or an _shape_list.
       """
       self.list = []
       self._add( a )
       self._add( b )
       
    def _add( self, x: _shape_or_shape_list ):
       if isinstance( x, _shape_list ): 
          self.list = self.list + x.list
       else:   
          self.list.append( x )       
       
    def _merge( self ) -> shape:    
        return shape( 
            "union(){\n" + 
               _indent( "".join( x._positive() for x in self.list )) +
            "}",       
            "union(){\n" + 
               _indent( "".join( x._negative() for x in self.list )) +
            "}"   
        )
       
    
#============================================================================
# 
# vector
#
#============================================================================

class vector:
    """2d or 3d vector
   
    This is a 2d (x,y) or 3d (x, y, z) vector.
    
    A vector is used to denote a location, a displacement (shift)
    a size, or sometimes just 2 or 3 numeric values.
    
    A vector has members x, y and z. 
    For a 2d vector, the z value is None.
    
    Vectors can be added or subtracted using the + or - operators.
    Vectors can be multiplied or divided 
    by a scalar using the * and / operators.
    """
    
    x = None
    """x (first) value of the vector"""
    
    y = None
    """y (second) value of the vector"""
    
    z = None
    """z (third) value of the vector"""
    
    def __init__( self, 
        x: _float_or_vector, 
        y: _float_or_none = None, 
        z: _float_or_none = None 
    ):
        """create from x and y, and an optional z value
        
        Create a 2d vector from x and y values, or a 
        3d vector from x, y and z values.
        
        When x is a vector, that vector is simply copied.
        """      
        if isinstance( x, vector ):
           if ( y != None ) or ( z != None ):
              raise Exception( 
                 "vector constructor called with a vector as"
                 " first parameter but also some more parameters." )
                 
           self.x, self.y, self.z = x.x, x.y, x.z
           
        else:
           if y == None:
              raise Exception( 
                 "called vector with one parameter"
                 " which is not a vector" )
                 
           self.x, self.y, self.z = x, y, z
        
    def _list( self ):
       return [ self.x, self.y, self.z ]    
        
    def _add( self, 
        a: _float_or_none, 
        b: _float_or_none 
    ) -> _float_or_none:
        """add two values, where either (but not both) could be None
        """
        if a == None: return b
        if b == None: return a      
        return a + b       
   
    def __add__( self, rhs: vector ) -> vector:
        """add two vector values (member-wise addition)
        
        Adding two 2d vectors yields a 2d vector,
        adding two 3d vectors yields a 3d vector.
        
        When a 2d vector and a 3d vector are added, the
        z value of the 2d vector is assumed to be 0.
        """   
        return vector( 
           self.x + rhs.x, 
           self.y + rhs.y, 
           self._add( self.z, rhs.z ) )
           
    def _sub( self, 
        a: _float_or_none, 
        b: _float_or_none 
    ) -> _float_or_none:
        """subtract two values, where either (but not both) could be None
        """
        if a == None: 
           if b == None: return None
           return - b
        if b == None: return a      
        return a - b               
      
    def __sub__( self, rhs: vector ) -> vector:
        """subtract two vector values (member-wise subtraction)
        
        Subtracting two 2d vectors yields a 2d vector,
        subtracting two 3d vectors yields a 3d vector.
        
        When a 2d vector and a 3d vector are subtracted, the
        z value of the 2d vector is assumed to be 0.
        """   
        return vector( 
           self.x - rhs.x, 
           self.y - rhs.y, 
           self._sub( self.z, rhs.z ) )
      
    def _mul( self, 
        a: _float_or_none, 
        b: _float_or_none 
    ) -> _float_or_none:
        """multiply two values, where either (but not both) could be None
        """
        if a == None: return None
        if b == None: return None   
        return a * b       
   
    def __mul__( self, v: float ) -> vector:
        """multiply a vector by a scalar (member-wise multiplication)
        """   
        return vector( 
            self.x * v, 
            self.y * v, 
            self._mul( self.z, v ) )
      
    __rmul__ = __mul__      

    def _div( self, 
        a: _float_or_none, 
        b: float 
    ) -> _float_or_none:
        """divide two values, where the first could be None
        """
        if a == None: return None
        if b == None: return None   
        return a * b       
   
    def __div__( self, v: float ):
        """divide a vector by a scalar (member-wise division)
        """   
        return vector( 
            self.x / v, 
            self.y / v, 
            self._div( self.z, v ) )

    def __str__( self ) -> str:
        """convert to [ x, y ] or [ x, y, z ] string format
        """      
        if self.z == None:
            return "[ %f, %f ]" % ( self.x, self.y)
        else:
            return "[ %f, %f, %f ]" % ( self.x, self.y, self.z )
            
    def __pow__( self, subject : _shape_or_none ) -> _shape_or_none:
        """apply the vector to a shape
        
        :param subject: the shape that is to be displaced (shifted)
        
        A vector can be applied to a shape using the ** operator.
        This will displace (shift) the shape.      

        The subject can be None instead of a shape,
        in which case the result will also be None.        
        """        
        return _apply( 
           subject, None,
           "translate( %s )" % str( self ), None )
           
identity = vector( 0, 0, 0 )
"""modifier that doesn't change its subject
"""           
      
def dup2( v: float ) -> vector:
    """vector( v, v )
    
    :param v: the value for x and y   
    
    Return a vector with both x and y set to v.
    """
    return vector( v, v )

def dup3( v: float ) -> vector:
    """vector( v, v, v )

    :param v: the value for x, y and z
    
    Return a vector with x, y and z set to v.
    """
    return vector( v, v, v )   
     
def right( v: float ) -> vector:
    """vector that shifts right (along the x axis) by v
    
    :param v: the shift distance
    
    Return the vector( v, 0, 0 ): 
    a vector with x set to v, and y and z to 0.
    """   
    return vector( v, 0, 0 ) 
   
def left( v: float ) -> vector:
    """vector that shifts left (along the x axis) by v
    
    :param v: the shift distance    
    
    Return vector( -v, 0, 0 ): 
    a vector with x set to -v, and y and z to 0.
    """   
    return vector( -v, 0, 0 )   
      
def back( v: float ) -> vector:
    """vector that shifts back (away from you along the y axis) by v 
    
    :param v: the shift distance    
    
    Return vector( 0, v, 0 ): 
    a vector with y set to v, and x and z to 0.
    """   
    return vector( 0, v, 0 ) 
   
def front( v: float ) -> vector:
    """vector that shifts to the front (towards you along the y axis) by v
    
    :param v: the shift distance    
    
    Return vector( 0, -v, 0 ): 
    a vector with y set to -v, and x and z to 0.
    """   
    return vector( 0, -v, 0 )   
      
def up( v: float ) -> vector:
    """vector that shifts up (along the z axis) by v
    
    :param v: the shift distance    
    
    Return vector( 0, 0, v ): 
    a vector with z set to v, and x and y to 0.
    """      
    return vector( 0, 0, v ) 
   
def down( v: float ) -> vector:
    """vector that shifts down (along the z axis) by v
    
    :param v: the shift distance    
    
    Return vector( 0, 0, -v ): 
    a vector with z set to v, and x and y to 0.
    """
    return vector( 0, 0, -v )   
      
   
#============================================================================
# 
# basic shapes
#
#============================================================================ 

def rectangle( 
    x: _float_or_vector, 
    y: _float_or_none = None, 
    rounding: float = 0 
) -> shape:
    """rectangle shape
    
    :param x: x size, or a vector which specifies both sizes
    :param y: y size (omit when x is a vector)
    :param rounding: rounding radius (default: no rounding)
        
    The size of the rectangle can be specified either by
    two values x and y, or by a vector.
    The rectangle has its lower-left corner at the origin.    
    The rounding specifies the radius of the rounding 
    at the corners and edges.     
    The default rounding is 0, which yields sharp boundaries.  
    
    .. figure::  ../examples/images/example_rectangle1_128.png   
        :target: ../examples/images/example_rectangle1_512.png 
    .. literalinclude:: ../examples/example_rectangle1.py
        :lines: 10-11        
    
    .. figure::  ../examples/images/example_rectangle2_128.png   
        :target: ../examples/images/example_rectangle2_512.png 
    .. literalinclude:: ../examples/example_rectangle2.py
        :lines: 10-11  
    """
    
    s = vector( x, y )
    
    if rounding == 0:
        return shape( "square( %s );" % str( s ) )    
        
    else:
        x, y, r = s.x, s.y, rounding
        return (
           dup2( r ) ** repeat4( s - 2 * dup2( r ) ) ** circle( r ) +
           vector( 0, r ) ** rectangle( x,         y - 2 * r ) +
           vector( r, 0 ) ** rectangle( x - 2 * r, y         ) ) 
      
def box( 
    x: _float_or_vector, 
    y: _float_or_none = None, 
    z: _float_or_none = None, 
    rounding: float = 0
) -> shape:
    """box shape
    
    :param x: x size, or a vector which specifies all 3 sizes
    :param y: y size (omit when x is a vector)
    :param z: z size (omit when x is a vector)
    :param rounding: rounding radius (default: no rounding)
        
    The size of the box can be specified either by
    three values x, y and z, or by a vector.
    The box has its lower-left corner at the origin.
    The rounding specifies the radius of the rounding 
    at the corners and edges.     
    The default rounding is 0, which yields sharp boundaries.
    
    .. figure::  ../examples/images/example_box1_128.png   
        :target: ../examples/images/example_box1_512.png 
    .. literalinclude:: ../examples/example_box1.py
        :lines: 10
        
    .. figure::  ../examples/images/example_box2_128.png   
        :target: ../examples/images/example_box2_512.png 
    .. literalinclude:: ../examples/example_box2.py
        :lines: 10
    """
    
    s = vector( x, y, z )
    
    if rounding == 0:
        return shape( "cube( %s );" % str( s ) )
        
    else:     
        x, y, z, r = s.x, s.y, s.z, rounding
        return (
            dup3( r ) ** repeat8( s - 2 * dup3( r ) ) ** sphere( r ) +
            
            vector( 0, 0, r ) ** 
                extrude( z - 2 * r ) ** rectangle( x, y, r ) +
                
            vector( 0, y - r, 0 ) ** rotate( 90, 0, 0 ) ** 
                extrude( y - 2 * r ) ** rectangle( x, z, r ) + 
                
            vector( x - r, 0, 0 ) ** rotate(  0, -90, 0 ) ** 
                extrude( x - 2 * r ) ** 
                rectangle( z, y, r )
        )       
           
def circle( 
    radius: float, 
    facets: _float_or_none = None 
) -> shape:
    """circle shape
    
    :param radius: the radius of the circle
    :param facets: number of circle facets
    
    The size of the circle is specified by its radius.
    The circle is in the x-y plane, with its center at the origin.   
    Optionally, the number of circle facets can be specified.
    The default is the global variable number_of_circle_facets.   
    
    .. figure::  ../examples/images/example_circle1_128.png   
        :target: ../examples/images/example_circle1_512.png 
    .. literalinclude:: ../examples/example_circle1.py
        :lines: 10
        
    .. figure::  ../examples/images/example_circle2_128.png   
        :target: ../examples/images/example_circle2_512.png 
    .. literalinclude:: ../examples/example_circle2.py
        :lines: 10
    """    
        
    # number_of_circle_facets can't be the default value because
    # that would not reflect a change of number_of_circle_facets
    if facets == None: facets = number_of_circle_facets    
        
    return shape( 
        "circle( r=%f, $fn=%d );" % ( radius, facets ) ) 
     
def cylinder( 
    radius: _float_or_vector, 
    height: _float_or_none = None, 
    facets: _float_or_none = None 
) -> shape:
    """cylinder shape
    
    :param radius: the radius of the cylinder, 
       or a vector that specifies the radius and the height
    :param height: the height of the cylinder
    :param facets: number of circle facets    
    
    The size of the cylinder is specified by its the radius
    at its base, and its height.
        
    Optionally, the number of circle facets can be specified.
    The default is the global variable number_of_circle_facets.
    
    .. figure::  ../examples/images/example_cylinder1_128.png   
        :target: ../examples/images/example_cylinder1_512.png 
    .. literalinclude:: ../examples/example_cylinder1.py
        :lines: 10
    """   
    
    sizes = vector( radius, height )
        
    # see remark in circle
    if facets == None: facets = number_of_circle_facets  
        
    return shape( 
       "cylinder( r=%f, h=%f, $fn=%d );" 
           % ( sizes.x, sizes.y, facets ) )

def cone( 
   radius1: _float_or_vector, 
   radius2: _float_or_none = None, 
   height: _float_or_none = None,  
   facets: _float_or_none = None 
) -> shape:
    """cone shape
    
    :param radius1: the radius of the cone at its bottom,
       or a vector that specifies the two radiuses and the height    
    :param radius2: the radius of the cone at its top
    :param height: the height of the cone
    :param facets: number of circle facets    
    
    The size of the cone is specified by its the radius
    at its base, its radius at its top, and its height.
        
    Optionally, the number of circle facets can be specified.
    The default is the global variable number_of_circle_facets.
    
    .. figure::  ../examples/images/example_cone1_128.png   
        :target: ../examples/images/example_cone1_512.png 
    .. literalinclude:: ../examples/example_cone1.py
        :lines: 10            
    """   
    
    sizes = vector( radius1, radius2, height )    
        
    # see remark in circle
    if facets == None: facets = number_of_circle_facets  
        
    return shape( 
        "cylinder( r1=%f, r2=%f, h=%f, $fn=%d );"
            % ( sizes.x, sizes.y, sizes.z, facets ) )
    
def sphere( 
    r: float, 
    facets: _float_or_none = None 
) -> shape:
    """sphere shape
    
    :param radius: the radius of the sphere
    :param facets: number of sphere facets    
    
    The size of the sphere is specified by its radius.
        
    Optionally, the number of sphere facets can be specified.
    The default is the global variable number_of_sphere_facets.
    
    .. figure::  ../examples/images/example_sphere1_128.png   
        :target: ../examples/images/example_sphere1_512.png 
    .. literalinclude:: ../examples/example_sphere1.py
        :lines: 10-12
    """    
    
    # see remark in circle    
    if facets == None: facets = number_of_sphere_facets
    
    return shape( 
        "sphere( r=%f, $fn=%d );" % ( r, facets ) )
          
def text( 
    txt: str, 
    height: float = 5, 
    facets: int = None,
    args = "" 
) -> shape:
    """text shape
    
    :param txt: the text
    :param height: the letter height
    :param facets: number of facets used to draw the letters
    :param args: extra arguments
            
    Optionally, the number of facets can be specified.
    The default is the global variable number_of_text_facets.
    
    .. figure::  ../examples/images/example_text1_128.png   
        :target: ../examples/images/example_text1_512.png 
    .. literalinclude:: ../examples/example_text1.py
        :lines: 10  
        
    Optionally, a string of extra arguments can be specified.
    Check the OpenSCAD_ documentation for the possible arguments.
    For your convenience, single quotes in the arg string are
    replaced by double quotes (OpenSCAD requires double quotes).
    
    .. figure::  ../examples/images/example_text2_128.png   
        :target: ../examples/images/example_text2_512.png 
    .. literalinclude:: ../examples/example_text2.py
        :lines: 10-14
        
    The horizontal size of a text depends on the specified height
    the text itself, and on the font. This makes it difficult to
    predict the size of a text. The resize operator can be 
    useful to scale a text to a know size.
    """    
    
    # see remark in circle
    if facets == None: facets = number_of_circle_facets     

    if args != "":
       args = ", " + args.replace( "'", '"' )
       
    return shape( 
        'text( "%s", %f, $fn=%d %s );'
            % ( txt, height, facets, args ) )   

def polygon( points: Iterable[ _vector_or_pair ] ) -> shape:
    """polygon shape
    
    :param points: a list of 2d vectors or value pairs
    
    A polygon is defined by the list of its edge points.
    Each edge point can be specified by either a 
    vector or a pair of values.
    
    .. figure::  ../examples/images/example_polygon1_128.png     
        :target: ../examples/images/example_polygon1_512.png 
    .. literalinclude:: ../examples/example_polygon1.py
        :lines: 10-12 
    """    
    
    def _2d_point_str( p: _vector_or_pair ):
        if isinstance( p, vector ):
            return "[%f,%f]" % ( p.x, p.y )
        else:
            return "[%f,%f]" % ( p[ 0 ], p[ 1 ] )    

    return shape( 
        'polygon( [ %s ] );' % ( 
           "".join( _2d_point_str( p ) + "," for p in points ) ) )   
   
   
#============================================================================
# 
# modifiers
#
#============================================================================  

class modifier:
    """modifier that can be applied by **
    
    A modifier is an object that can be applied to its 
    subject, a shape, using the ** operator. 
    A modifier is constructed by providing the function that
    is to be applied.
    
    The subject can be None instead of a shape,
    in which case the result will also be None.    
    
    .. figure::  ../examples/images/example_modifier1_128.png    
    .. literalinclude:: ../examples/example_modifier1.py
        :lines: 10
    """

    def __init__( self, function ):
        self.function = function
      
    def __pow__( self, subject: _shape_or_none ) -> _shape_or_none:
        if subject == None:
           return None
        else:   
           return self.function( subject )
           
def extrude( 
    height: float,
    twist: float = 0,
    scale: float = 1,
    facets: int = None,
):     
    """extrude operator: extend a 2d object in the z direction

    :param height: the height over which the object will be extruded    
    :param twist: the degrees over which the object is rotated along
                  the z axis over its extrusion height (default: 0)
    :param scale: the scaling determines the relative size of the object 
                  at its maximum extrusion height
    :param facets: number of steps used in the extrusion    
    
    Optionally, the number of steps can be specified.
    The default is the global variable number_of_extrude_facets.
    """
    
    # see remark in circle
    if facets == None: facets = number_of_extrude_facets  
     
    return modifier( 
        lambda subject : 
            _apply( 
            subject, None,
            "linear_extrude( height=%f, twist=%f, scale=%f, $fn=%d )\n" % 
               ( height, twist, scale, facets ), None ) )         

def mirror(
    x: _float_or_vector, 
    y: float = None, 
    z: float = None 
):    
    """mirror operator: mirror an object in a planes
    
    :param x: the x of the vector, or the full vector
    :param y: (optional) the y of the vector     
    :param z: (optional) the z of the vector    
    
    This modifier mirrors its subject in a plane through the origin. 
    The plane is specified by its normal vector (the vector
    that is perpendicular to the mirror plane).
    
    The vector is either specified as a single vector
    parameter, or as separate x, y and z values.  

    The example shows a text, the same text mirrored in the 
    y-z plane, mirrored in the x-z plane, and mirrored in the x-y plane.    

    .. figure::  ../examples/images/example_mirror1_128.png    
    .. literalinclude:: ../examples/example_mirror1.py
        :lines: 11,14-17    
    """
    
    normal_vector = vector( x, y, z )

    return modifier( 
        lambda subject : 
            _apply( 
           subject, None,
           "mirror( %s )" % str( normal_vector ), None ) )
           
def rotate( 
    x: _float_or_vector, 
    y: float = None, 
    z: float = None 
):
    """rotate operator: rotate an object around one or more axises
    
    :param x: the x of the vector, or the full vector
    :param y: (optional) the y of the vector     
    :param z: (optional) the z of the vector     
    
    The vector is either specified as a single vector
    parameter, or as separate x, y and z values.
    
    This manipulator rotates its object along one or more axises,
    by the specified amount in degrees.
    
    The example below shows an object, and the same objects
    rotated 45 degrees, first along the x axis, then along
    the y axis, and lastly along the z axis.
    
    .. figure::  ../examples/images/example_rotate1_128.png    
    .. literalinclude:: ../examples/example_rotate1.py
        :lines: 9-15
    """
    
    angles = vector( x, y, z )

    return modifier( 
        lambda subject : 
            _apply( 
                subject, None,
                "rotate( %s )" % str( angles ), None ) )    

def scale( 
    x: _float_or_vector, 
    y: float = None, 
    z: float = None 
):  
    """scale operator: scale an object in one or more directions
    
    :param x: the x of the vector, or the full vector
    :param y: (optional) the y of the vector     
    :param z: (optional) the z of the vector     
    
    The vector is either specified as a single vector
    parameter, or as separate x, y and z values.
    
    This manipulator scales its subject by the factors
    indicated for the x, y and z direction.
    A factor of 1 retains the original size,
    2 makes it twice at large, etc.
    
    The example below shows a box, and the same box 
    scaled by 2 in the x direction, scaled by 2 in the y direction,
    and scaled by 2 in the z direction.
    
    .. figure::  ../examples/images/example_scale1_128.png    
    .. literalinclude:: ../examples/example_scale1.py
        :lines: 9-15    
    """
    
    directions = vector( x, y, z )

    return modifier( 
        lambda subject :
            _apply( 
                subject, None,
                "scale( %s )" % str( directions ), None ) )      

def _hull():  
    return modifier( 
        lambda subject :
            _apply( 
                subject, None,
                "hull()", None ) ) 
                
hull = _hull()
"""convex hull
    
This manipulator creates the convex hull around its subject,
which can be 2D or 3D.

.. figure::  ../examples/images/example_hull1_128.png    
.. literalinclude:: ../examples/example_hull1.py
    :lines: 11, 14-15    
"""
   
def resize( 
    x: _float_or_vector,
    y: float = None, 
    z: float = None 
):  
    """resize operator: resize an object
    
    :param x: the x of the vector, or the full vector
    :param y: (optional) the y of the vector     
    :param z: (optional) the z of the vector     
    
    The vector is either specified as a single vector
    parameter, or as separate x, y and z values.
    
    This manipulator resizes its subject to the sizes
    indicated for the x, y and z direction.
    A size of 0 keeps the size (in that direction) unchanged.
    A size of None scales the size in that direction
    with another non-0 non-None size.
    
    The example below shows a text, and
    the same text scaled to fit in a 30 by 10 rectangle.
    
    .. figure::  ../examples/images/example_resize1_128.png    
    .. literalinclude:: ../examples/example_resize1.py
        :lines: 9, 11      
        
    The example below shows a sphere, and
    the same sphere scaled to size 40 in the x direction,
    unchanged (size 10) ijn the y direction,
    and z matching the x direction (scaled to 40).
    
    .. figure::  ../examples/images/example_resize2_128.png    
    .. literalinclude:: ../examples/example_resize2.py
        :lines: 9, 11      
    """
    
    amounts = vector( x, y, z )
    auto = str( [ x == None for x in amounts._list() ] ).lower()

    return modifier( 
        lambda subject :
            _apply( 
                subject, None,
                "resize( %s, auto=%s )" % 
                   ( str( amounts ), auto ), None ) )  
                
def _negative():
    return modifier( 
       lambda subject : 
          shape( "", str( subject ) ) )
       
negative = _negative()       
"""makes its subject a dominant negative
    
This manipulator makes its subject a dominant negative:
something that will not be filled.
"""
           
def _positive():
    return modifier( 
       lambda subject : 
          shape( str( subject ), "" ) )
       
positive = _positive()   
"""removes dominant negatives
    
The positive manipulator subtracts and removes 
the dominant emptinesses in its subject, so an 
solid can be placed in the space of what was a dominant emptiness.    
"""

def repeat2( 
    x: _float_or_vector,
    y: float = None, 
    z: float = None 
):
    """repeat at two positions
    
    :param x: the x of the vector, or the full vector
    :param y: (optional) the y of the vector     
    :param z: (optional) the z of the vector     
    
    The vector is either specified as a single vector
    parameter, or as separate x, y and z values.
    
    This manipulator repeats its subject twice: 
    once at its original location, 
    and once shifted by the specified vector.
    
    .. figure::  ../examples/images/example_repeat2_128.png    
    .. literalinclude:: ../examples/example_repeat2.py
        :lines: 10
    """
    
    v = vector( x, y, z )

    return modifier( 
       lambda subject :
          subject + ( v ** subject ) )
           
def repeat4( 
    x: _float_or_vector,
    y: float = None
):    
    """repeat at four positions
    
    :param x: the x of the vector, or the full vector
    :param y: (optional) the y of the vector     
    
    The vector is either specified as a single vector
    parameter, or as separate x and y values.
    
    This manipulator repeats its subject at the
    four corners of the rectangle specified by the parameters.
    
    .. figure::  ../examples/images/example_repeat4_128.png       
    .. literalinclude:: ../examples/example_repeat4.py
        :lines: 10     
    """
    
    v = vector( x, y )
    
    return modifier( 
       lambda subject :       
           vector(   0,   0 ) ** subject +
           vector( v.x,   0 ) ** subject +
           vector(   0, v.y ) ** subject +
           vector( v.x, v.y ) ** subject
    )
           
def repeat8( 
    x: _float_or_vector, 
    y: float = None, 
    z: float = None 
):
    """repeat at eight positions
    
    :param x: the x of the vector, or the full vector
    :param y: (optional) the y of the vector     
    :param z: (optional) the z of the vector     
    
    The vector is either specified as a single vector
    parameter, or as separate x, y and z values.
    
    This manipulator repeats its subject at the corners
    of the box specified by the parameters.
    
    .. figure::  ../examples/images/example_repeat8_128.png       
    .. literalinclude:: ../examples/example_repeat8.py
        :lines: 10
    """
    
    v = vector( x, y, z )

    return modifier( 
        lambda subject :
            vector(   0,   0,   0 ) ** subject +
            vector( v.x,   0,   0 ) ** subject +
            vector(   0, v.y,   0 ) ** subject +
            vector( v.x, v.y,   0 ) ** subject +
            vector(   0,   0, v.z ) ** subject +
            vector( v.x,   0, v.z ) ** subject +
            vector(   0, v.y, v.z ) ** subject +
            vector( v.x, v.y, v.z ) ** subject
    )
            
   
#============================================================================
# 
# project enclosure
#
#============================================================================ 

class m_screw:
    """a metric (m3 etc.) screw
    """

    def __init__( self, diameter, thread ):
        self.diameter = diameter
        self.thread = thread
        
m3_5  = m_screw( 3,  5 )        
m3_10 = m_screw( 3, 10 )        
m3_12 = m_screw( 3, 12 )        
m3_15 = m_screw( 3, 15 )        
m3_20 = m_screw( 3, 20 )        

def hollow_box( size : vector, walls, rounding = 0 ) -> shape:
    """a hollow box
    
    :param size: size of the box (x, y, z )
    :param walls: wall thickness
    :param rounding: rounding diameter (default: no rounding)
    
    This is a hollow project enclosure box,
    Use screw_and_nut_column() to place screw holes and recesses.
    Use split() to separate it into a top and a bottom part.
    (Or use project_enclosure() which does these things for you.)
    """
    return (
        box( size, rounding ) 
        - vector( dup3( walls )) ** box( size - 2 * dup3( walls )))
     
def screw_and_nut_column( 
   height, 
   screw : m_screw, 
   wall = 1 
) -> shape:
    """a screw and nut column
    
    :param height: height of the column
    :param srew: screw (specifies diameter and thread lenghth)    
    :param wall: wall thickness (default 1mm)   
    
    This is a vertical screw-and-nut column for keeping two parts 
    of an enclosure together with a flat screw and a hex nut.
    It is assumed to be spliced into the top and bottom parts.
    """
    
    h = height
    s = screw.thread
    m = screw.diameter
    w = wall

    # 4/5'th of the m size seems to be a good estimate
    # of the depth of the screw recess
    sh = ( 4.0 / 5.0 ) * m
    
    # height must fit two recesses and two wall thicknesses
    minimal_h = 2 * m + 2 * w
    if h < minimal_h:
       raise Exception( 
          "height %f is must be at least %f" % ( h, minimal_h ))
             
    maximum_screw = h - sh
    minimum_screw = m + 2 * w    
    screw_range = "must be %f..%f" % ( minimum_screw, maximum_screw) 
    
    # the screw must not stick out of the bottom
    if s > maximum_screw:
       raise Exception( "the screw will stick out," + screw_range )
          
    # the depth of the nut recess must match
    # the screw thread length
    nh = h - sh - s + m
    
    r = None
    
    # recess for the crew head   
    r += up( h ) ** rotate( 180, 0, 0 )  ** ( cylinder( w + m, sh + w ) - \
        negative ** cylinder( m, sh ))

    # support cone
    r += up( h - sh - w - m ) ** cylinder( m / 2 + w, m, r2 = m + w )

    # cylinder for the screw shaft
    r += cylinder( w + m / 2, h ) - \
        negative ** cylinder( m / 2, h )
        
    # recess for the hex nut
    r+= cylinder( w + m, nh + w ) - \
        negative ** cylinder( m, nh, f = 6 )       
   
    # support cone
    r += up( nh + w ) ** cylinder( m + w, m, r2 = m / 2 + w )
   
    return r   
   
def split_box( b, s, h, d = vector( 5, 0 ) ):
    """split an enclosure in top and bottom parts
   
    This function splices a box into separate top and bottom parts,
    which are placed next to each other 
    (default: 5 mm apart in x direction).
   
    :param b: the box to splice
    :param s: the size of the box    
    :param h: height at which the box is spliced
    :param d: distance between the parts
    """
    
    if d.x != 0:
       d = vector( s.x + d.x, 0, 0 )
    elif d.y != 0:
       d = vector( 0, s.y + d.y, 0 )
    else:      
       raise Exception( "both x and y distances are 0" )
    
    r = None
   
    # for debugging: the original box
    if 0: r = b
   
    # bottom part
    r = ( vector( s.x + 5, 0, 0 ) ** r ) + \
        ( b - ( vector( 0, 0, h ) ** box( s )))
       
    # top part    
    r = ( vector( s.x + 5, 0, 0 ) ** r ) + \
        vector( s.x, 0, s.z ) ** rotate( 0, 180, 0 ) ** \
           ( b - box( s.x, s.y, h ))
       
    return r   
      
def project_enclosure( size, walls, rounding = 0 ):
    """a simple 2-part project enclosure
    
    :param size: outer size of the enclosure (x, y, z )
    :param walls: wall thickness
    :param rounding: rounding diameter (default: no rounding)
    
    This is a simple 2-part project enclosure box.
    """
    
    b = hollow_box( size, walls, rounding )
    
    
    
    return b

     
      

      