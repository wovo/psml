"""
This script re-creates the images and
the readme.md file from the .py files
found in this directory that do not start with "_".
"""

import subprocess
from os import listdir
from os.path import isfile, join

# Yes, I use Windows. Sorry.
python = "c:/python38/python" 
openscad = "C:/Program Files (x86)/openscad/openscad"

header = "Each file can be run, it will  write to the output.scad file.\n\n"

def run( list ):
   print( subprocess.run( list ))

def update_file( f ):
   run([ 
      python, 
      f + ".py" ])
   run([ 
      openscad, 
      "output.scad", 
      "--viewall", 
      "--view", "axes", 
      "--imgsize", "128,128",
      "-oimages/%s.png" % f ])
   run([ 
      openscad, 
      "output.scad", 
      "--viewall", 
      "--view", "axes", 
      "--imgsize", "512,512",
      "-oimages/%s512.png" % f ])
   return (
      "[![%s](images/%s.png)][imaqes/%s512.png]\n\n"
      "[%s.py](%s.py)\n\n" ) % ( f, f, f, f, f )     
   
def update( files ):
   s = header
   for f in files:
      print( "updating %s" % f )
      s += update_file( f )   
   f = open( "readme.md", "w" )
   f.write( s )
   f.close()
   
files = [
   f.replace( ".py", "" ) 
      for f in listdir() 
         if f.find( ".py" ) > 0 and not f.startswith( "_" ) ]   

update( files )
