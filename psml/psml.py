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
import os.path
import subprocess

# specifiers used in the type annotations
_shape_or_shape_list  = Union[ "shape", "_shape_list" ]
_shape_or_none        = Union[ "shape", None ]
_str_or_none          = Union[ str, None ]
_float_or_vector      = Union[ float, "vector" ]
_float_or_none        = Union[ float, None ]
_vector_or_pair       = Union[ "vector", Tuple[float,float]]


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
        :lines: 10-11

    .. figure::  ../examples/images/example_facets2_128.png
        :target: ../examples/images/example_facets2_512.png
    .. literalinclude:: ../examples/example_facets2.py
        :lines: 9, 11-12
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

def _apply2(
    s1 : str,
    s2 : str,
    a : _shape_or_none,
    b : _shape_or_none,
) -> shape:
    """
    apply an OpenSCAD operation to two shapes

    :param s1: operation to apply to the positive parts
    :param s2: operation to apply to the negative parts
    :param a: first shape
    :param b: second shape
    """
    if b == None:
       b = shape( "", "" )
       if a == None:
          a = b
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

def apply(
    text : str,
    subject : _shape_or_none
) -> _shape_or_none:
    """apply an OpenSCAD operation to a shape

    :param text: the text of the OpenSCAD operation
    :param subject: the shape to which the operation is applied

    This function applies an OpenSCAD operation to a shape.
    This can be useful for OpenSCAD operations that are not
    otherwise available in the library.

    For convenience, single quotes in the text are replaced by
    double quotes (OpenSCAD uses double quotes).

    Coloring and translation are available in the library,
    but could be done with OpenSCAD functions as shown in the example.

    .. figure::  ../examples/images/example_apply1_128.png
        :target: ../examples/images/example_apply1_512.png
    .. literalinclude:: ../examples/example_apply1.py
        :lines: 10
    """
    text = text.replace( "'", '"' )
    return None if subject == None else shape(
        text + "{\n" + _indent(
            subject._positive() + "\n" ) +
        "}",
        text + "{\n" + _indent(
            subject._negative() + "\n" ) +
        "}",
    )


#============================================================================
#
# shape
#
#============================================================================

def _select_existing_file( list, default ):
   for file in list:
      if os.path.isfile( file ):
         return file
   return default      

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

    def write( self, file_name = "output" ):
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

        if not "." in file_name: 
            file_name = file_name+ ".scad"
            
        f = open( file_name, "w" )
        f.write( str( self ) )
        f.close()
        
    def stl( self, file_name = "output" ):
        """write the stl to the specified file

        :param file_name: name of the file

        This function uses OpenSCAD to render, and then 
        export the stl representation to the specified 
        file (default: output.stl).

        If the file_name does not en in ".stl" 
        that suffix is appended.
        
        A temporary file _output.scad will be created
        which is the input for OpenSCAD.
        
        NOTE: the path to openscad is now 

        .. code-block::

            # these lines have the same effect
            sphere( 10 ).stl()
            sphere( 10 ).stl( "output" )
            sphere( 10 ).stl( "output.stl" )
        """
        
        if not file_name.endswith( ".stl" ): 
            file_name = file_name+ ".stl"
        
        self.write( "_output.scad" )
        
        openscad = _select_existing_file( [
           "C:/Program Files (x86)/OpenSCAD/OpenSCAD.exe",
           "C:/Program Files/OpenSCAD/OpenSCAD.exe",
        ], "openscad" )   
        
        s = subprocess.run( [ 
            openscad, 
            "_output.scad", 
            "-o", file_name ] )        

    def gcode( self, file_name = "output" ):
        """write the gcode to the specified file
        
        THIS DOESN NOT WORK (YET)?
        Running cura from a command line seems to be a dark art.

        :param file_name: name of the file

        This function uses OpenSCAD to render, and then 
        Cura to slice the design to the specified 
        file (default: output.gcode).

        If the file_name does not en in ".stl" 
        that suffix is appended.
        
        A temporary file _output.scad will be created
        which is the input for OpenSCAD.
        
        NOTE: the path to openscad is now 

        .. code-block::

            # these lines have the same effect
            sphere( 10 ).gcode()
            sphere( 10 ).gcode( "output" )
            sphere( 10 ).gcode( "output.gcode" )
        """
        
        if not "." in file_name: 
            file_name = file_name+ ".gcode"
        
        self.stl( "_output.stl" )
        
        cura = "C:/Program Files/Ultimaker Cura 4.4/CuraEngine"
        s = subprocess.run( [ 
            cura, 
            "slice"
            " -o", file_name,       
            " -l", "_output.scad" ] )

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
        return _apply2( "difference()", "union()", self, rhs )

    def __mul__( self, rhs: shape ) -> shape:
        """intersect two shapes
        """
        return _apply2( "intersection()", "union()", self, rhs )

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

    def _merge( self, function = "union()" ) -> shape:
        return shape(
            function + "{\n" +
               _indent( "".join( x._positive() for x in self.list )) +
            "}",
            function + "{\n" +
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

    # these assignments are here just as anchors for the docstrings

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
        return a / b

    def __truediv__( self, v: float ):
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
        return apply( "translate( %s )" % str( self ), subject )

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
           dup2( r ) ** repeat4( s - 2 * dup2( r ) ) 
              ** circle( radius = r ) +
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
            dup3( r ) ** repeat8( s - 2 * dup3( r ) ) 
               ** sphere( radius = r ) +

            vector( 0, 0, r ) **
                extrude( z - 2 * r ) ** rectangle( x, y, r ) +

            vector( 0, y - r, 0 ) ** rotate( 90, 0, 0 ) **
                extrude( y - 2 * r ) ** rectangle( x, z, r ) +

            vector( x - r, 0, 0 ) ** rotate(  0, -90, 0 ) **
                extrude( x - 2 * r ) **
                rectangle( z, y, r )
        )
        
def _radius_from_radius_or_diameter( 
    radius:    _float_or_none = None,
    diameter:  _float_or_none = None
):
    if(
        (( radius == None ) and ( diameter == None ))
        or (( radius != None ) and ( diameter != None ))
    ):
        raise Exception(
            "specify either a radius or a diameter" )
    if diameter != None:
       return diameter / 2.0
    return radius   

def _optional_radius_from_radius_or_diameter( 
    radius:    _float_or_none = None,
    diameter:  _float_or_none = None
):
    if(( radius != None ) and ( diameter != None )):
        raise Exception(
            "specify either a radius or a diameter, but not both" )
    if diameter != None:
       return diameter / 2.0
    return radius   

def circle(
    *,
    radius:    _float_or_none = None,
    diameter:  _float_or_none = None,
    facets:    _float_or_none = None
) -> shape:
    """circle shape

    :param radius: the radius of the circle
    :param diameter: the diameter of the circle
    :param facets: number of circle facets

    The size of the circle is specified by either
    its radius or its diameter.
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
    
    r = _radius_from_radius_or_diameter( radius, diameter )

    return shape(
        "circle( r=%f, $fn=%d );" % ( r, facets ) )

def cylinder(
    height:    _float_or_vector = None,
    *,
    radius:    _float_or_none = None,
    diameter:  _float_or_none = None,
    rounded_top:  bool = False,
    facets:    _float_or_none = None
) -> shape:
    """cylinder shape

    :param height: the height of the cylinder,
       or a vector that specifies  the height and the radius
    :param radius: the radius of the cylinder
    :param diameter: the diameter of the circle
    :param rounded_top: whether the top is rounded (default: not)    
    :param facets: number of circle facets  
    
    The size of the cylinder is specified by its the radius
    at its base, and its height.

    Optionally, the number of circle facets can be specified.
    The default is the global variable number_of_circle_facets.

    .. figure::  ../examples/images/example_cylinder1_128.png
        :target: ../examples/images/example_cylinder1_512.png
    .. literalinclude:: ../examples/example_cylinder1.py
        :lines: 10-11
    """

    r = _optional_radius_from_radius_or_diameter( radius, diameter )
    sizes = vector( height, r )
    height, radius = sizes.x, sizes.y

    # see remark in circle
    if facets == None: facets = number_of_circle_facets  
        
    if rounded_top:
        return (
            cylinder( 
               height = height - radius, 
               radius = radius, 
               facets = facets )
            + up( height - radius ) ** sphere( radius = radius ) )
    else:
        return shape( "cylinder( h=%f, r=%f, $fn=%d );" 
            % ( height, radius, facets ) )

def cone(
   height:     _float_or_vector = None,
   *,
   radius1:    _float_or_none = None,
   diameter1:  _float_or_none = None,
   radius2:    _float_or_none = None,
   diameter2:  _float_or_none = None,
   facets:     _float_or_none = None
) -> shape:
    """cone shape

    :param height: the height of the cone,
       or a vector that specifies the height and the two radiuses
    :param radius1: the radius of the cone at its bottom,
    :param radius2: the radius of the cone at its top
    :param diameter1: the diameter of the cone at its bottom,
    :param diameter2: the diameter of the cone at its top
    :param facets: number of circle facets

    The size of the cone is specified by its height,
    its the radius or diameter at its base, 
    and its radius or diameter at its top.

    Optionally, the number of circle facets can be specified.
    The default is the global variable number_of_circle_facets.

    .. figure::  ../examples/images/example_cone1_128.png
        :target: ../examples/images/example_cone1_512.png
    .. literalinclude:: ../examples/example_cone1.py
        :lines: 10-11
    """

    r1 = _optional_radius_from_radius_or_diameter( radius1, diameter1 )
    r2 = _optional_radius_from_radius_or_diameter( radius2, diameter2 )
    sizes = vector( height, r1, r2 )

    # see remark in circle
    if facets == None: facets = number_of_circle_facets

    return shape(
        "cylinder( h=%f, r1=%f, r2=%f, $fn=%d );"
            % ( sizes.x, sizes.y, sizes.z, facets ) )

def sphere(
    radius:    _float_or_none = None,
    diameter:  _float_or_none = None,
    facets:    _float_or_none = None
) -> shape:
    """sphere shape

    :param radius: the radius of the sphere
    :param diameter: the diameter of the sphere
    :param facets: number of sphere facets

    The size of the sphere is specified by either
    its radius or its diameter.

    Optionally, the number of sphere facets can be specified.
    The default is the global variable number_of_sphere_facets.

    .. figure::  ../examples/images/example_sphere1_128.png
        :target: ../examples/images/example_sphere1_512.png
    .. literalinclude:: ../examples/example_sphere1.py
        :lines: 10-12
    """

    # see remark in circle
    if facets == None: facets = number_of_sphere_facets

    r = _radius_from_radius_or_diameter( radius, diameter )

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
        :target: ../examples/images/example_modifier1_512.png
    .. literalinclude:: ../examples/example_modifier1.py
        :lines: 9, 12
    """

    def __init__( self, function ):
        self.function = function

    def __pow__( self, subject: _shape_or_none ) -> _shape_or_none:
        if subject == None:
           return None
        else:
           return self.function( subject )

def _minkowski():
    return modifier(
        lambda subject :
           subject._merge( "minkowski()" )
           if isinstance( subject, _shape_list )
           else subject )

minkowski = _minkowski()
"""minkowski sum

This modifier computes the Minkowski sum of two or more
2D or 3D objects. It must be applied to a sum of objects.
When it is applied to something else (for instance
the result of applying a modifier) it is a no-op.

    .. figure::  ../examples/images/example_minkowski1_128.png
        :target: ../examples/images/example_minkowski1_512.png
    .. literalinclude:: ../examples/example_minkowski1.py
        :lines: 9, 12

    .. figure::  ../examples/images/example_minkowski2_128.png
        :target: ../examples/images/example_minkowski2_512.png
    .. literalinclude:: ../examples/example_minkowski2.py
        :lines: 9, 12

"""

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
        lambda subject : apply(
            "linear_extrude( height=%f, twist=%f, scale=%f, $fn=%d )\n"
                % ( height, twist, scale, facets ), subject ) )
                
def rotate_extrude(
    angle: float = 360, 
    convexity: int = 2,
    facets: int = None
):              

    # see remark in circle
    if facets == None: facets = number_of_extrude_facets
    
    return modifier(
        lambda subject : apply(
            "rotate_extrude( angle=%f, convexity=%d, $fn=%d )\n"
                % ( angle, convexity, facets ), subject ) )    

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
        :target: ../examples/images/example_mirror1_512.png
    .. literalinclude:: ../examples/example_mirror1.py
        :lines: 11,14-17
    """

    normal_vector = vector( x, y, z )

    return modifier( lambda subject :
        apply( "mirror( %s )" % str( normal_vector ), subject ) )

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
        :target: ../examples/images/example_rotate1_512.png
    .. literalinclude:: ../examples/example_rotate1.py
        :lines: 9-16
    """

    angles = vector( x, y, z )

    return modifier( lambda subject :
        apply( "rotate( %s )" % str( angles ), subject ) )

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
        :target: ../examples/images/example_scale1_512.png
    .. literalinclude:: ../examples/example_scale1.py
        :lines: 9-15
    """

    directions = vector( x, y, z )

    return modifier( lambda subject :
        apply( "scale( %s )" % str( directions ), subject ) )

def _hull():
    return modifier( lambda subject :
         apply( "hull()", subject ) )

hull = _hull()
"""convex hull

This manipulator creates the convex hull around its subject,
which can be 2D or 3D.

.. figure::  ../examples/images/example_hull1_128.png
    :target: ../examples/images/example_hull1_512.png
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
    A negative size scales that size in that direction
       in proportion with another non-0 non-None size.

    The example below shows a text, and
    the same text scaled to fit in a 30 by 10 rectangle.

    .. figure::  ../examples/images/example_resize1_128.png
        :target: ../examples/images/example_resize1_512.png
    .. literalinclude:: ../examples/example_resize1.py
        :lines: 9, 11

    The example below shows a sphere, and
    the same sphere scaled to size 40 in the x direction,
    unchanged (size 10) ijn the y direction,
    and z matching the x direction (scaled to 40).

    .. figure::  ../examples/images/example_resize2_128.png
        :target: ../examples/images/example_resize2_512.png
    .. literalinclude:: ../examples/example_resize2.py
        :lines: 9, 11
    """

    amounts = vector( x, y, z )
    auto = str( [ x == None for x in amounts._list() ] ).lower()

    return modifier( lambda subject :
        apply(
            "resize( %s, auto=%s )" % ( str( amounts ), auto ),
            subject ) )

def _negative():
    return modifier( lambda subject :
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
        :target: ../examples/images/example_repeat2_512.png
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
        :target: ../examples/images/example_repeat4_512.png
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
        :target: ../examples/images/example_repeat8_512.png
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
# colors
#
#============================================================================

_colors = [
   "Lavender", "Thistle", "Plum", "Violet", "Orchid", "Fuchsia", "Magenta",
   "MediumOrchid", "MediumPurple", "BlueViolet", "DarkViolet", "DarkOrchid",
   "DarkMagenta", "Purple", "Indigo", "DarkSlateBlue", "SlateBlue",
   "MediumSlateBlue", "Pink", "LightPink", "HotPink", "DeepPink",
   "MediumVioletRed", "PaleVioletRed", "Aqua", "Cyan", "LightCyan",
   "PaleTurquoise", "Aquamarine", "Turquoise", "MediumTurquoise",
   "DarkTurquoise", "CadetBlue",  "SteelBlue", "LightSteelBlue",
   "PowderBlue", "LightBlue", "SkyBlue", "LightSkyBlue", "DeepSkyBlue",
   "DodgerBlue", "CornflowerBlue", "RoyalBlue", "Blue", "MediumBlue",
   "DarkBlue", "Navy", "MidnightBlue", "IndianRed", "LightCoral", "Salmon",
   "DarkSalmon", "LightSalmon", "Red", "Crimson", "FireBrick", "DarkRed",
   "GreenYellow", "Chartreuse", "LawnGreen", "Lime", "LimeGreen",
   "PaleGreen", "LightGreen", "MediumSpringGreen", "SpringGreen",
   "MediumSeaGreen", "SeaGreen", "ForestGreen", "Green", "DarkGreen",
   "YellowGreen", "OliveDrab", "Olive", "DarkOliveGreen", "MediumAquamarine",
   "DarkSeaGreen", "LightSeaGreen", "DarkCyan", "Teal", "LightSalmon",
   "Coral", "Tomato", "OrangeRed", "DarkOrange", "Orange", "Gold", "Yellow",
   "LightYellow", "LemonChiffon", "LightGoldenrodYellow", "PapayaWhip",
   "Moccasin", "PeachPuff", "PaleGoldenrod", "Khaki", "DarkKhaki",
   "Cornsilk", "BlanchedAlmond", "Bisque", "NavajoWhite", "Wheat",
   "BurlyWood", "Tan", "RosyBrown", "SandyBrown", "Goldenrod",
   "DarkGoldenrod", "Peru", "Chocolate", "SaddleBrown", "Sienna", "Brown",
   "Maroon", "White", "Snow", "Honeydew", "MintCream", "Azure", "AliceBlue",
   "GhostWhite", "WhiteSmoke", "Seashell",  "Beige", "OldLace", "FloralWhite",
   "Ivory", "AntiqueWhite", "Linen", "LavenderBlush", "MistyRose",
   "Gainsboro", "LightGrey", "Silver", "DarkGray", "Gray", "DimGray",
   "LightSlateGray", "SlateGray", "DarkSlateGray", "Black" ]

_current_module = __import__(__name__)
for c in _colors:
    # c_copy forces a copy, otherwise the *variable* c
    # would be captured (and all colors would be Black
    f = modifier( lambda s, c_copy = c: apply( 'color( "%s" )' % c_copy, s ))
    setattr( _current_module, c, f )
    setattr( _current_module, c.lower(), f )

def color(
   r: _float_or_vector,
   g: float = None,
   b: float = None,
   alpha: float = 1.0
):
    """a color in RGB format

    :param r: the r of the vector, or the full color vector
    :param g: (optional) the g of the color
    :param b: (optional) the b of the color
    :param alpha: (optional) the alpha value (opacity)

    The color is either specified as a single vector
    parameter, or as separate r, g and b values.
    When a single vector is specified, and alpha value
    (if present) must be named parameter.

    The individual color values must be in the range 0..255.

    An alpha of 0 is full transparency, a value of 1 is a solid color.
    A lower alpha makes the object more faintly colored.
    It does not make it opaque (translucent).

    Colors are visible in OpenSCAD preview, but NOT in after
    rendering. Hence the examples below show previews, unlike
    the other examples, which show the result of rendering.

    .. figure::  ../examples/images/example_color1_128.png
        :target: ../examples/images/example_color1_512.png
    .. literalinclude:: ../examples/example_color1.py
        :lines: 10-12

    The color names in the World Wide Web consortium's SVG color list
    are available, both with PascalCase and in lowercase.

    .. figure::  ../examples/images/example_color2_128.png
        :target: ../examples/images/example_color2_512.png
    .. literalinclude:: ../examples/example_color2.py
        :lines: 10-12
    """

    # the range of OpenSCAD color channels is 0..1
    c = vector( r, g, b ) / 255.0

    return modifier( lambda s:
       apply( "color( %s, %f )" % ( str( c ), alpha ), s ) )


#============================================================================
#
# screw-and-nut column
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
m3_30 = m_screw( 3, 30 )
m3_40 = m_screw( 3, 40 )

def screw_and_nut_column(
   height,
   screw : m_screw,
   wall = 1
) -> shape:
    """a screw and nut column

    :param height: height of the column
    :param srew: screw (specifies diameter and thread length)
    :param wall: wall thickness (default 1mm)

    This is a vertical screw-and-nut column for keeping two parts
    of an enclosure together with a flat screw and a hex nut.
    It is assumed to be split into the top and bottom parts.
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
    ch = 1

    # recess for the crew head
    r += ( 
        up( h ) ** rotate( 180, 0, 0 ) 
            ** ( cylinder( radius = w + m, height = sh + w )
        - negative ** cylinder( radius = m, height = sh ) ) )

    # recess cone
    r += up( h - w ) ** cone( 
        radius1 = w + m, 
        radius2 = w + m + ch,
        height  = ch )    

    # support cone
    r += up( h - sh - w - m ) ** cone( 
        radius1 = m / 2 + w, 
        radius2 = m + w, 
        height  = m )

    # cylinder for the screw shaft
    r += ( cylinder( radius = w + m / 2, height = h )
        - negative ** cylinder( radius = m / 2, height = h ) )

    # recess for the hex nut
    r+= (
        cylinder( radius = w + m, height = nh + w )
        - negative ** cylinder( 
            radius = m, 
            height  = nh, 
            facets = 6 ) )

    # recess cone
    r += up( w ) ** cone( 
        radius1 = w + m + ch, 
        radius2 = w + m,
        height  = ch )    

    # support cone
    r += up( nh + w ) ** cone( 
        radius1 = m + w, 
        radius2 = m / 2 + w,
        height  = m )

    return r

    
#============================================================================
#
# hollow (project) box
#
#============================================================================

def hollow_box( 
    size : vector, 
    walls = 1, 
    rounding = 0 
) -> shape:
    """a hollow box

    :param size: outer size of the box (x, y, z )
    :param walls: wall thickness
    :param rounding: outer rounding diameter (default: no rounding)

    This is a hollow project enclosure box,
    Use screw_and_nut_column() to place screw holes and recesses.
    
    Use split() to separate it into a top and a bottom part.
    (Or use project_enclosure() which does these things for you.)
    """
    return (
        box( size, rounding = rounding )
        - vector( dup3( walls )) ** box( size - 2 * dup3( walls )))


#============================================================================
#
# split a box into bottom and/or top parts
#
#============================================================================

def split_box( b, s, h, d = vector( 5, 0 ) ):
    """split an enclosure in top and bottom parts

    This function splices a box into separate top and bottom parts,
    which are placed next to each other
    (default: 5 mm apart in x direction).

    :param b: the box to split
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
    if 1: r = ( vector( s.x + 5, 0, 0 ) ** r ) + \
        ( b - ( vector( 0, 0, h ) ** box( s )))

    # top part
    if 1: r = ( vector( s.x + 5, 0, 0 ) ** r ) + \
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




