import sys
sys.path.append( "../psml" )
from psml import *

facets(100)
thickness = 5

pipeDiameter = 50
pipeHeight = 50
outer_boxSize = vector(60, 60, 100)


inner_boxSize = vector(outer_boxSize.x-thickness,
                       outer_boxSize.y-thickness, outer_boxSize.z-thickness)
document = 'skimmer_v6.scad'


def pipe_shape(h, inner_diameter, thickness, position=None):
    a = cylinder(h, diameter=inner_diameter+thickness)
    b = cylinder(h, diameter=inner_diameter)
    if position is not None:
        thing = position ** (a - b)
        return thing
    return a-b

# def roster(size_vector):
#     plaat = box(size_vector)
#     for x in size_vector.x:
#         for y in size_vector.y:
#             print(x,y) 

def hooked_corner(height, thickness, length):
    a = box(vector(length, thickness, height))
    b = left(thickness)**box(vector(length, thickness, height))
    a = (rotate(0, 0, 90) ** a)
    return a + b


def open_box_shape(outer_vector, inner_vector):
    difference = vector(outer_vector.x - inner_vector.x,
                        outer_vector.y-inner_vector.y, outer_vector.z-inner_vector.z)
    boxA = box(outer_vector)
    boxB = up((difference.z)) ** right(difference.x /
                                       2) ** back(difference.y/2) ** box(inner_vector)
    return boxA - boxB


# pijp
###########################################################################
pipeHole = down(pipeHeight/2) ** cylinder(pipeHeight, diameter=pipeDiameter)
pipe = down(pipeHeight) ** pipe_shape(pipeHeight, pipeDiameter, thickness)
###########################################################################
# deur gat
###########################################################################
doorHoleSize = vector(thickness, outer_boxSize.x-20, outer_boxSize.z-50)
doorHole = up(doorHoleSize.z) ** right((outer_boxSize.y/2) -
                                       thickness) ** back(-(outer_boxSize.x-20)/2) ** box(doorHoleSize)
hookLeft = right((outer_boxSize.x/2)+10)**back(-(outer_boxSize.y/2) + thickness /
                                               2) ** rotate(0, 0, 90) ** hooked_corner(outer_boxSize.z, thickness/2, 10)
hookRight = back((outer_boxSize.y/2))**right((outer_boxSize.x/2)+10-thickness /
                                             2) ** rotate(0, 0, 180) ** hooked_corner(outer_boxSize.z, thickness/2, 10)
# met vector dingen bewegen is een stuk makkelijker up, down etc niet zo intuitief
bottom = vector(outer_boxSize.x/2, -(outer_boxSize.y/2),
                0) ** box(10, outer_boxSize.y, thickness)
###########################################################################
# pieletjes voor het rooster
###########################################################################
pal1 = vector(-(inner_boxSize.x/2), -(inner_boxSize.y/2),
              0)**box(thickness, 10, doorHoleSize.z-thickness)
pal2 = vector((inner_boxSize.x/2)-thickness, -(inner_boxSize.y/2),
              0)**box(thickness, 10, doorHoleSize.z-thickness)
pal3 = vector(-(inner_boxSize.x/2), (inner_boxSize.y/2)-10,
              0)**box(thickness, 10, doorHoleSize.z-thickness)
pal4 = vector((inner_boxSize.x/2)-thickness, (inner_boxSize.y/2) -
              10, 0)**box(thickness, 10, doorHoleSize.z-thickness)
###########################################################################
# skimmer totaal
###########################################################################
# roster(vector(10,10,5))
skimmerBox = left(outer_boxSize.x/2) ** back(-(outer_boxSize.y/2)) ** open_box_shape(
    outer_boxSize, inner_boxSize) - doorHole - pipeHole + pipe + hookLeft + hookRight + bottom + pal1 + pal2 + pal3+pal4
skimmerBox.write(document)
