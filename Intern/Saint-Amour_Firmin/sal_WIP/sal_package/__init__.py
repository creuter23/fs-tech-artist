# this will get the path for the comment.txt files
# and pass them to the actual script
# and that way they only have to be semi hardcoded


import sys
import os.path
import sal_proj01
reload(sal_proj01)

dir_path = os.path.dirname(__file__)
print dir_path

import sys
sys.path.append(r"%s/Imaging-1.1.7" % dir_path)
from PIL import Image

print dir_path
full_path = os.path.join(dir_path, 'Comments')
print full_path

def gui():
    
    sal_proj01.gui(dir_path)
    