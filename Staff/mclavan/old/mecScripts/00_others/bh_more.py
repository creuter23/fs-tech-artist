'''
# Other code

import maya.OpenMaya as OpenMaya 
import maya.cmds as cmds
import maya.OpenMayaAnim as OpenMayaAnim
"""--------------------------------------------------------------------"""
#declare variables as types
node = OpenMaya.MObject()
selectionList = OpenMaya.MSelectionList()

OpenMaya.MGlobal.getActiveSelectionList(selectionList)
topNode = OpenMaya.MObject()
selectionList.getDependNode(0,topNode)

# node is MObject to your mesh
itDG = OpenMaya.MItDependencyGraph(topNode,OpenMaya.MItDependencyGraph.kDownstream,OpenMaya.MItDependencyGraph.kPlugLevel)
while not itDG.isDone():
	oCurrentItem = itDG.currentItem()
	if oCurrentItem.hasFn(OpenMaya.MFn.kSkinClusterFilter):
		print('Found')
	itDG.next()
'''


"""--------------------------------------------------------------------"""

def getSkinCluster():
    #define the variables as the necessary classes.
    dagPath = openMaya.MDagPath()
    selectionList = openMaya.MSelectionList()
    skinCluster = []
    #grab whatever is selected and put it in selectionList
    openMaya.MGlobal.getActiveSelectionList(selectionList)
    #take the first thing selected and grab its dagPath
    selectionList.getDagPath(0, dagPath)
    #use the path to grab the shape *note this will break if there are more shapes. Will need to add the .numberOfShapesDirectlyBelow to ensure it doesn't break. 
    dagPath.extendToShape()
    #this creates the iterator that will be used to loop through everything. *note The *It* between the M and the D denote that this is an iterator.
    itDG = openMaya.MItDependencyGraph(dagPath.node(),openMaya.MItDependencyGraph.kDownstream,openMaya.MItDependencyGraph.kPlugLevel)
    while not itDG.isDone():
        oCurrentItem = itDG.currentItem()
        #the iterator returns an MObject that we then check to see if it is a skinCluster. If it is, Save it. 
        if oCurrentItem.hasFn(openMaya.MFn.kSkinClusterFilter):
            skinCluster = openAni.MFnSkinCluster(oCurrentItem)
            print (skinCluster.name() + " will be returned")
            break 
        itDG.next()
    return skinCluster, dagPath, selectionList
    

"""--------------------------------------------------------------------"""

def averageSelection():
    #grab the skinCluster
    skinCluster, relatedShape, selectionList = getSkinCluster()
    #determine that there is or isn't a skin cluster.
    if not skinCluster:
        openMaya.MGlobal.displayError("No skinCluster found")
    else:
        infCount = openMaya.MScriptUtil()
        uInf = infCount.asUintPtr()
        skinInfluences = openMaya.MDagPathArray()
        oldSkinWeights = openMaya.MDoubleArray()
        compItr = openMaya.MItSelectionList(selectionList)
                #using the .influenceObjects to get all the joint influences.
        skinCluster.influenceObjects(skinInfluences)
        while not compItr.isDone():
            skinCluster.getWeights(relatedShape,compItr,oldSkinWeights,uInf)
            compItr.next()
        print oldSkinWeights
