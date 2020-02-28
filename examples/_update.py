"""
This script re-creates the images and
the readme.md file from the .py files
found in this directory that do not start with "_".
"""

import subprocess
import sys
from os import listdir
from os.path import isfile, join

# Yes, I use Windows. Sorry.
python = "c:/python38/python" 
openscad = "C:/Program Files (x86)/openscad/openscad"

header = """
Each file can be run, it will write to the output.scad file.
Click on an image to get a larger image.
"""

def run( f, list ):

   # color examples must be viewed only, not rendered
   # (because rendering doesn't support colors)
   if f.find( "color" ) < 0:
      list = list + [ "--render"]
      
   s = subprocess.run( list )
   if 0: print( s )

def update_file( f, update ):
   print( "updating %s" % f )
   run( "", [ 
      python, 
      f + ".py" ])
   if update: 
      run( f, [ 
         openscad, 
         "output.scad", 
         "--viewall", 
         "--view", "axes",  
         "--imgsize", "128,128",
         "-oimages/%s_128.png" % f ])
      run( f, [ 
         openscad, 
         "output.scad", 
         "--viewall", 
         "--view", "axes", 
         "--imgsize", "512,512",
         "-oimages/%s_512.png" % f ])
   return (
      "[![%s](images/%s_128.png)](images/%s_512.png)\n\n"
      "[%s.py](%s.py)\n\n" ) % ( f, f, f, f, f )     
   
def update( files ):
   s = header
   for f in files:
      s += update_file( f, sys.argv[ 1 ] == "update" )   
   f = open( "readme.md", "w" )
   f.write( s )
   f.close()   

if len( sys.argv ) == 2:
   files = [
      f.replace( ".py", "" ) 
         for f in listdir() 
            if f.find( ".py" ) > 0 and not f.startswith( "_" ) ]
   update( files )
else:
   update_file( sys.argv[ 2 ], sys.argv[ 1 ] == "update" )   
