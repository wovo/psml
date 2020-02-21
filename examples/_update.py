import subprocess

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
      "-oimages/%s.png" % f ])
   return "![%s](images/%s.png)\n [%s](%s.py)\n\n" % ( f, f, f, f )     
   
def update( files ):
   s = "Each file can be run, it will  write to the output.scad file.\n\n"
   for f in files:
      print( "updating %s" % f )
      s += update_file( f )   
   f = open( "reame.md", "w" )
   f.write( s )
   f.close()
      
update([ 
   "snowman", 
   "triangle",
   "rectangles",
   "repeat",
   "dice",
])

