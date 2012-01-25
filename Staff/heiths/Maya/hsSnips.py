#!/usr/bin/python

# Things I find useful/interesting...
# Some I'll breakdown... others I'll just post.
# Heith Seewald 2012



#------------- Get Current Scene Name In Maya ---------------
#I admit it's not the most pythonic way... but it's one line and does the trick.
fileName = env.sceneName().split('/')[-1].split('.')[0]
'''
Breakdown:  
     env.sceneName     gives the full path to your scene...
    .split('/')        turns the full path name into a list of folders
    [-1]               grabs the last item in the list... which is scene file with the extention
    .split('.')[0]     Another split to grab the file name without the extention...
'''





#-------------------Fun With Math -----------
from pymel.core import *
import math

curveListA = []
curveListB = []

for i in range(1000):
    curveListA.append([math.sin(i)*2*i,math.cos(i)*i*2,math.cos(i)*100])
    curveListB.append([math.cos(i)*i*2,math.sin(i)*i*2,math.cos(i) *100])

hsCurveA = curve(p=curveListA)
hsCurveB = curve( hsCurveA, a=True, p=curveListB )

#That's it... just paste it in maya and play with the math... it's kind of fun.