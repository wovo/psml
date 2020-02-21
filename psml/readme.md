The psml.py file is the library. 
Put it in a location where your Python code can find it,
or arrange for it to find it.
I prefer to add its location to the path,
in this case relative to the psml examples or work directory:

~~~Python
import sys
sys.path.append( "../psml" )
~~~