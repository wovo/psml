"""
This script re-creates the images and
the readme.md file from the .py files
found in this directory that do not start with "_".
"""

import subprocess
from os import listdir
from os.path import isfile, join

python = "c:/python38/python" 
openscad = "C:/Program Files (x86)/openscad/openscad"

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
      "--imgsize", "256,256",
      "-oimages/%s.png" % f ])
   return "![%s](images/%s.png)\n\n [%s.py](%s.py)\n\n" % ( f, f, f, f )     
   
def update( files ):
   s = "Each file can be run, it will  write to the output.scad file.\n\n"
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
