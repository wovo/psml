#============================================================================
"""
a library for generating OpenSCAD_ 3D models

https://www.github.com/wovo/psml

\(c) Wouter van Ooijen (wouter.vanooijen@hu.nl)

Distributed under the Boost Software License, Version 1.0.

.. _OpenSCAD: https://www.openscad.org/

-----------------------------------------------------------------------------

This is a Python library (Python 3 required) for writing
3D model code that can be rendered and processed by OpenSCAD_.
This documentation is meant to be usable on its own, 
without having to read the OpenSCAD documentation.
Hence it is worded as if the PSML library contains all the functionality,
while in fact it is in most cases just a thin layer 
on top of the OpenSCAD language.

The library has a vector class.
A vector holds x, y and (optional) z numeric values.
A vector is used to specify (in 2D or 3D) a size, 
a location or displacement, and sometimes just 2 or 3 values
that are conveniently grouped together.
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

A flat object can be extended into a solid object
by extruding it (in the z direction), <>

.. figure::  ../examples/images/intro_extrude_128.png
Objects and be added, subtracted and intersected 
with the operators +, - and \*.

.. figure::  ../examples/images/intro_asi_128.png

Manipulators can be applied to an object with the ** (power) operator.
Basic manipulators are vector, rotate, mirror, scale and resize.

.. figure::  ../examples/images/intro_vrm_128.png

The repeat2, repeat4 and repeat8 manipulators repeat their subject.
Repeat2 does this at the original location, 
and shifted by the specified vector.
Repeat4 does this at the 4 corners of the rectangle
specified by the vector.
Repeat8 does this at the 8 corners of the box
specified by the vector.

.. figure::  ../examples/images/intro_repeat1_128.png

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

-----------------------------------------------------------------------------

"""
#============================================================================

from __future__ import annotations
from typing import Union
#from functools import reduce


#============================================================================
# 
# miscellaneous
#
#============================================================================

# the default number of facets for a circle and a sphere
number_of_circle_facets  = 32
number_of_sphere_facets  = 32
number_of_text_facets    = 32

def facets( numer_of_facts: int ) -> None:
    """accuracy (number of facets) of circles, spheres and fonts
    
    The default setting (32) is a compromise between speed and accuracy.
    
    For quick rendering of complex designs 
    a lower value (10, or even 5) might be appropriate.
    
    This function has effect on shapes that are created
    after its call, so better call it before you create any elements.
    
    .. figure::  ../examples/images/facets1_128.png    
    .. code-block:: 
    
        cylinder( 10, 20 ) + vector( 25, 0, 10 ) ** sphere( 10 )
    
    .. figure::  ../examples/images/facets2_128.png 
    .. code-block:: 
    
        facets( 9 )
        cylinder( 10, 20 ) + vector( 25, 0, 10 ) ** sphere( 10 )
    """
    
    global number_of_circle_facets
    number_of_circle_facets = n
    
    global number_of_sphere_facets
    number_of_sphere_facets = n
    
    global number_of_text_facets
    number_of_text_facets = n

def _indent( txt: string ) -> string:
    """return the text with all lines indented one indent step
    """
    return "".join( map(
        lambda s: "" if s.strip() == "" else "   " + s + "\n",
            txt.split( "\n" )
        ))

def _apply( 
    a : shape, 
    b : shape, 
    s1 : string,
    s2 : string
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
       positive : string, 
       negative : string = "" 
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
        
    def _merge( self ) -> _shape:
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
        
    def __str__( self ) -> string:       
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
        
    def __add__( self, rhs: shape ) -> shape:
        """add two shapes
        
        This could be mapped directly to an OpenSCAD union(),
        but to avoid deeply nested union()s an _shape_list is used.
        """
        if rhs == None: return self
        return _shape_list( self, rhs )
            
    __radd__ = __add__            

    def __sub__( self, rhs: shape ) -> shape:
        """subtract two shapes
        """
        return _apply( self, rhs, "difference()", "union()" )
              
    def __mul__( self, rhs: shape ) -> shape:
        """intersect two shapes  
        """
        return _apply( self, rhs, "intersection()", "union()" )       
    
_shape_or_shape_list = Union[ shape, "_shape_list" ]

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

_float_or_vector = Union[ float, "vector" ]
_float_or_none = Union[ float, None ]

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
                 "vector constructor called with a vector as first parameter"
                 " and some more parameters. " )
                 
           self.x, self.y, self.z = x.x, x.y, x.z
           
        else:
           if y == None:
              raise Exception( 
                 "called vector with one parameter which is not a vector" )
                 
           self.x, self.y, self.z = x, y, z
        
    def _add( self, 
        a: _float_or_none, 
        b: _float_or_none 
    ) -> float:
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
    ) -> float:
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
    ) -> float:
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
    ):
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

    def __str__( self ) -> string:
        """convert to [ x, y ] or [ x, y, z ] string format
        """      
        if self.z == None:
            return "[ %f, %f ]" % ( self.x, self.y)
        else:
            return "[ %f, %f, %f ]" % ( self.x, self.y, self.z )
            
    def __pow__( self, subject : shape ) -> shape:
        """apply the vector to a shape
        
        :param subject: the shape that is to be displaced (shifted)
        
        A vector can be applied to a shape using the ** operator.
        This will displace (shift) the shape.        
        """        
        return _apply( 
           subject, None,
           "translate( %s )" % str( self ), None )
      
def dup2( v ):
    """return vector( v, v ): a vector with x and y set to 0
    """
    return vector( v, v )

def dup3( v ):
    """return vector( v, v, v ): a vector with x, y and z set to 0
    """
    return vector( v, v, v )   
     
def right( v ):
    """vector that shifts right by v
    
    Return the vector( v, 0, 0 ): 
    a vector with x set to v, and y and z to 0.
    """   
    return vector( v, 0, 0 ) 
   
def left( v ):
    """vector that shifts left by v
    
    Return vector( -v, 0, 0 ): 
    a vector with x set to -v, and y and z to 0.
    """   
    return vector( -v, 0, 0 )   
      
def back( v ):
    """vector that shifts back by v
    
    Return vector( 0, v, 0 ): 
    a vector with y set to v, and x and z to 0.
    """   
    return vector( 0, v, 0 ) 
   
def front( v ):
    """vector that shifts to the front by v
    
    Return vector( 0, -v, 0 ): 
    a vector with y set to -v, and x and z to 0.
    """   
    return vector( 0, -v, 0 )   
      
def up( v ):
    """vector that shifts up by v
    
    Return vector( 0, 0, v ): 
    a vector with z set to v, and x and y to 0.
    """      
    return vector( 0, 0, v ) 
   
def down( v ):
    """vector that shifts down by v
    
    Return vector( 0, 0, -v ): 
    a vector with z set to v, and x and y to 0.
    """
    return vector( 0, 0, -v )   
      
   
#============================================================================
# 
# basic shapes
#
#============================================================================ 

def rectangle( x, y = None, rounding = 0 ):
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
    
    .. figure::  ../examples/images/rectangle1_128.png    
    .. code-block:: 
    
        rectangle( 20, 30 )
        # or rectangle( vector( 20, 30 ), rounding = 0 )
    
    .. figure::  ../examples/images/rectangle2_128.png 
    .. code-block:: 
    
        rectangle( 20, 30, 3 )
        # or rectangle( vector( 20, 30 ), rounding = 3 )
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
      
def box( x, y: float = None, z: float = None, rounding = 0 )-> shape:
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
    
    .. figure::  ../examples/images/box1_128.png    
    .. code-block:: 
    
        box( 20, 30, 10 )
        # or box( vector( 20, 30, 10 ), 0 )
    
    .. figure::  ../examples/images/box2_128.png 
    .. code-block:: 
    
        box( 20, 30, 10, 2 )
        # or box( vector( 20, 30, 10 ), 2 )
    """
    
    s = vector( x, y, z )
    
    if rounding == 0:
        return shape( "cube( %s );" % str( s ) )
        
    else:     
        x, y, z, r = s.x, s.y, s.z, rounding
        return (
            dup3( r ) ** repeat8( s - 2 * dup3( r ) ) ** sphere( r ) +
            
            vector( 0, 0, r ) ** 
                extrude( z - 2 * r ) ** rectangle ( x, y, r ) +
                
            vector( 0, y - r, 0 ) ** rotate( 90, 0, 0 ) ** 
                extrude( y - 2 * r ) ** rectangle ( x, z, r ) + 
                
            vector( x - r, 0, 0 ) ** rotate(  0, -90, 0 ) ** 
                extrude( x - 2 * r ) ** rectangle ( z, y, r )
        )       
           
def circle( radius, facets = None ):
    """circle shape
    
    :param radius: the radius of the circle
    :param facets: number of circle facets
    
    The size of the circle is specified by its radius.
    The circle is in the x-y plane, with its center at the origin.   
    Optionally, the number of circle facets can be specified.
    The default is the global variable number_of_circle_facets.   
    
    .. figure::  ../examples/images/circle1_128.png    
    .. code-block:: 
    
        circle( 20 )
    
    .. figure::  ../examples/images/circle2_128.png  
    .. code-block:: 
    
        circle( 20, facets = 5 )    
    """    
        
    # number_of_circle_facets can't be the default value because
    # that would not reflect a change of number_of_circle_facets
    if facets == None: facets = number_of_circle_facets    
        
    return shape( 
        "circle( r=%f, $fn=%d );" % ( radius, facets ) ) 
     
def cylinder( radius, height = None, facets = None ):
    """cylinder shape
    
    :param radius: the radius of the cylinder, 
       or a vector that specifies the radius and the height
    :param height: the height of the cylinder
    :param facets: number of circle facets    
    
    The size of the cylinder is specified by its the radius
    at its base, and its height.
        
    Optionally, the number of circle facets can be specified.
    The default is the global variable number_of_circle_facets.
    
    .. figure::  ../examples/images/cylinder1_128.png    
    .. code-block:: 
    
        cylinder( 10, 20 ) + right( 35 ) ** cylinder( vector( 20, 10 ))
    """   
    
    sizes = vector( radius, height )
        
    # see remark in circle
    if facets == None: facets = number_of_circle_facets  
        
    return shape( 
       "cylinder( r=%f, h=%f, $fn=%d );" 
           % ( sizes.x, sizes.y, facets ) )

def cone( radius1, radius2 = None, height = None,  facets = None ):
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
    
    .. figure::  ../examples/images/cone1_128.png    
    .. code-block:: 
    
        cylinder( 10, 20 ) + right( 35 ) ** cylinder( vector( 20, 10 ))    
    """   
    
    sizes = vector( radius1, radius2, height )    
        
    # see remark in circle
    if facets == None: facets = number_of_circle_facets  
        
    return shape( 
        "cylinder( r1=%f, r2=%f, h=%f, $fn=%d );"
            % ( sizes.x, sizes.y, sizes.z, facets ) )
    
def sphere( r, f = None ):
    """sphere shape
    
    :param radius: the radius of the sphere
    :param facets: number of sphere facets    
    
    The size of the sphere is specified by its radius.
        
    Optionally, the number of sphere facets can be specified.
    The default is the global variable number_of_sphere_facets.
    
    .. figure::  ../examples/images/sphere1_128.png    
    .. code-block:: 
    
        sphere( 10 ) \\
           + ( right( 20 ) ** sphere( 6 ) ) \\
           + ( right( 35 ) ** sphere( 4 ))     
    """    
    
    # see remark in circle    
    if f == None: f = number_of_sphere_facets
    
    return shape( 
        "sphere( r=%f, $fn=%d );" % ( r, f ) )

def text( 
    txt: string, 
    height: float = 5, 
    facets: int = None,
    args = "" 
):
    """text shape
    
    :param txt: the text
    :param height: the letter height
    :param facets: number of facets used to draw the letters
    :param args: extra arguments
            
    Optionally, the number of facets can be specified.
    The default is the global variable number_of_text_facets.
    
    .. figure::  ../examples/images/text1_128.png    
    .. code-block:: 
    
        sphere( 10 ) \\
           + ( right( 20 ) ** sphere( 6 ) ) \\
           + ( right( 35 ) ** sphere( 4 ))     
    """    
    
    # see remark in circle
    if facets == None: facets = number_of_circle_facets     

    if args != "":
       args = ", " + args
       
    return shape( 
        'text( "%s", %f, $fn=%d %s );'
            % ( txt, height, facets, args ) )   

def polygon( points ):
    """polygon shape
    
    :param points: a list of 2d vectors or value pairs
    
    A polygon is defined by the list of its edge points.
    Each edge point can be specified by either a 
    vector or a pair of values.
    
    .. figure::  ../examples/images/polygon_128.png    
    .. code-block:: 
    
        polygon( [ 
            [ 0, 0 ], [ 3, 0 ], [ 2, 1 ], [ 2, 2 ], 
            [ 3, 2 ], [ 1, 3 ], [ 0, 3 ], [ 1, 1 ] ] )    
    """    
    
    def _2d_point_str( p ):
        if isinstance( p, vector ):
            return "[%f,%f]" % ( p.x, p.y )
        else:
            return "[%f,%f]" % ( p[ 0 ], p[ 1 ] )    

    return shape( 
        'polygon( [ %s ] );' % ( 
           "".join( self._2d_point_str( p ) + "," for p in points ) ))


#============================================================================
# 
# OpenSCAD modifier
#
#============================================================================
      
class extrude:
    """extrude operator: extend a 2d object in the z direction
    """
    
    def __init__( self, z ):
        self.z = z   
         
    def __pow__( self, subject: shape ) -> shape:
        return _apply( 
           subject, None, 
           "linear_extrude( %f )\n" % self.z, None )
        
class rotate:
    """rotate operator: rotate an object around one or more axises
    """
    
    def __init__( self, x, y = None, z = None ):    
        if y != None:
           x = vector( x, y, z )
        self.angles = x

    def __pow__( self, subject: shape ) -> shape:   
        return _apply( 
            subject, None,
            "rotate( %s )" % str( self.angles ), None )     

class mirror:
    """mirror operator: mirror an object in one or more planes
    """
    
    def __init__( self, x, y = None, z = None ):    
        if y != None:
           x = vector( x, y, z )
        self.angles = x

    def __pow__( self, subject: shape ) -> shape:   
        return _apply( 
           subject, None,
           "mirror( %s )" % str( self.angles ), None )              
                    
class scale:
    """scale operator: scale an object
    """
    
    def __init__( self, x, y = None, z = None ):    
        if y != None:
           x = vector( x, y, z )
        self.amounts = x

    def __pow__( self, subject: shape ) -> shape:   
        return _apply( 
           subject, None,
           "scale( %s )" % str( self.amounts ), None )              
                    
class scale:
    """resize operator: resize an object
    """
    
    def __init__( self, x, y = None, z = None ):    
        if y != None:
           x = vector( x, y, z )
        self.amounts = x

    def __pow__( self, subject: shape ) -> shape:   
        return _apply( 
           subject, None,
           "resize( %s )" % str( self.amounts ), None )              
                    
     
#============================================================================
# 
# shape manipulators
#
#============================================================================     
     
class _negative:
    """makes its subject a dominant negative
    
    This manipulator makes its subject a dominant negative:
    something that will not be filled.
    """

    def __pow__( self, subject: shape ) -> shape:   
       return shape( "", str( subject ) )
       
negative = _negative()       
           
class _positive:
    """makes its subject a dominant negative
    
When something must be 
The positive manipulator subtracts and removes 
the dominant emptinesses in its subject, so an 
solid can be placed in the space of what was a dominant emptiness.    
    
    This manipulator makes its subject a dominant negative:
    something that will not be filled.
    """

    def __pow__( self, subject: shape ) -> shape:   
       return shape( str( subject ), "" )
       
positive = _positive()   
"""
"""

identity = vector( 0, 0, 0 )
"""modifier that doesn't change its subject
"""
           
class repeat2:
    """repeat at two positions
    
    This manipulator repeats its subject twice: once at its original
    location, and once at the indicated vector.
    """

    def __init__( self, x, y = None, z = None ):
       self.vector= vector( x, y, z )

    def __pow__( self, subject: shape ) -> shape:   
       return subject + ( self.vector ** subject )
           
class repeat4:

    def __init__( self, x, y = None ):
       if y == None:
          self.x, self.y = x.x, x.y
       else:
          self.x, self.y = x, y

    def __pow__( self, subject: shape ) -> shape:   
       return (
           vector(      0,      0 ) ** subject +
           vector( self.x,      0 ) ** subject +
           vector(      0, self.y ) ** subject +
           vector( self.x, self.y ) ** subject
       )
           
class repeat8:

    def __init__( self, x, y = None, z = None ):
       if y == None:
          self.x, self.y, self.z = x.x, x.y, x.z
       else:
          self.x, self.y, self.z, = x, y, z

    def __pow__( self, subject: shape ) -> shape:   
       return (
           vector(      0,      0,      0 ) ** subject +
           vector( self.x,      0,      0 ) ** subject +
           vector(      0, self.y,      0 ) ** subject +
           vector( self.x, self.y,      0 ) ** subject +
           vector(      0,      0, self.z ) ** subject +
           vector( self.x,      0, self.z ) ** subject +
           vector(      0, self.y, self.z ) ** subject +
           vector( self.x, self.y, self.z ) ** subject
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

     
      

      