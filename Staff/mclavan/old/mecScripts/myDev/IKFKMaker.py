import maya.cmds as cmds

win='primeWin'
scriptName=__name__

def gui():
	if(cmds.window(win,q=1,ex=1)):
		cmds.deleteUI(win)
	if(cmds.windowPref(win,q=1,ex=1)):
		cmds.windowPref(win,r=1)
	cmds.window(win,t='IKFK Maker')
	cmds.columnLayout()
	cmds.rowColumnLayout(nc=3)
	cmds.text('Curve for switch')
	cmds.textField('cvTxt')
	cmds.button(l='grab',c=scriptName + '.cvGrab()')
	cmds.setParent('..')
	cmds.button(l='Set up IKFK',c=scriptName + '.argIKFKMaker()')
	cmds.showWindow(win)

def cvGrab():
	mycvGrab=cmds.ls(sl=1)
	cmds.textField('cvTxt',e=1,text=mycvGrab[0])	

def argIKFKMaker():
	myStuff=cmds.ls(sl=1,dag=1)
	
	myIK=cmds.duplicate(rr=1,rc=1)
	myFK=cmds.duplicate(rr=1,rc=1)
	cmds.select(hi=1)
	myStuffIK=cmds.ls(myIK,dag=1)
	myStuffFK=cmds.ls(myFK,dag=1)
	myCv=cmds.textField('cvTxt',q=1,text=1)
	#cmds.circle(n='mytest')
	
	newIK=[]
	i=0	
	while(i<len(myStuffIK)):
		newname=myStuff[i] + '_IK'
		cmds.rename(myStuffIK[i],newname)
		newIK.append(newname)
		i=i+1
	
	newFK=[]
	i=0	
	while(i<len(myStuffFK)):
		newname=myStuff[i] + '_FK'
		cmds.rename(myStuffFK[i],newname)
		newFK.append(newname)
		i=i+1
	
	
	grpName=myStuff[0] + '_grp'
	cmds.group(myStuff[0],newIK[0],newFK[0],n=grpName)
	cmds.addAttr(myCv,ln="IKFK",at='double',min=0,max=10,dv=0,r=1,w=1,s=1,k=1)
	i=0
	myCtst=[]
	while(i<(len(myStuff)-1)):
		newCv=[myCv +'.IKFK']
		cmds.setAttr(newCv[0],0)
		myCT=cmds.orientConstraint(newIK[i],newFK[i],myStuff[i])
		ctAttrFK=[myCT[0] + '.' + newFK[i] + 'W1']
		ctAttrIK=[myCT[0] + '.' + newIK[i] + 'W0']
		cmds.setAttr(ctAttrIK[0],1)
		cmds.setAttr(ctAttrFK[0],0)
	
		cmds.setDrivenKeyframe(ctAttrFK[0],currentDriver=newCv[0])
		cmds.setDrivenKeyframe(ctAttrIK[0],currentDriver=newCv[0])
	
		cmds.setAttr(newCv[0],10)
	
		cmds.setAttr(ctAttrIK[0],0)
		cmds.setAttr(ctAttrFK[0],1)
		cmds.setDrivenKeyframe(ctAttrFK[0],currentDriver=newCv[0])
		cmds.setDrivenKeyframe(ctAttrIK[0],currentDriver=newCv[0])	
		myCtst.append(myCT)
	
		i=i+1
		
	myIKH=cmds.ikHandle( n=(myStuff[0] + '_ikHandle'), sj=newIK[0], ee=newIK[(len(newIK))-1] )
	myIKCtrl=cmds.circle(n=(myStuff[0] + 'IK_ctrl'))
	myPrimer(newIK[-1],myIKCtrl)
	#cmds.pointConstraint(myIKH,myIKCtrl,n='ptTemp')
	#cmds.delete('ptTemp')
	cmds.pointConstraint(myIKCtrl,(myStuff[0] + '_ikHandle'),n=(myStuff[0] + '_ptCnst'))
	i=0
	while(i<(len(myStuff)-1)):
		fkcvName=[newFK[i]+ '_ctrl']
		tmpCv=cmds.circle(n=fkcvName[0])
		myPrimer(newFK[i],tmpCv)
		cmds.orientConstraint(tmpCv,newFK[i])
		if(i<1):
			tmpwa=cmds.ls(sl=1)
			cmds.parentConstraint(grpName,tmpwa,mo=1)
		if(i>0):
			tmpjt=cmds.ls(sl=1)
			tmpwa=[newFK[i-1]+ '_ctrl']
			cmds.parent(tmpjt,tmpwa)
		i=i+1

	#cmds.setAttr(newCv[0],10)
	
	trmpikvis=myIKCtrl[0] + '_wa.v'
	trmpfkvis=[newFK[0]+ '_ctrl_wa.v']
	print trmpikvis
	print trmpfkvis
	#starts at 10
	cmds.setAttr(trmpikvis,0)
	cmds.setAttr(trmpfkvis[0],1)
	cmds.setDrivenKeyframe(trmpikvis,currentDriver=newCv[0])
	cmds.setDrivenKeyframe(trmpfkvis,currentDriver=newCv[0])
	
	cmds.setAttr(newCv[0],9.5)
	cmds.setAttr(trmpikvis,1)
	cmds.setAttr(trmpfkvis[0],1)
	cmds.setDrivenKeyframe(trmpikvis,currentDriver=newCv[0])
	cmds.setDrivenKeyframe(trmpfkvis,currentDriver=newCv[0])
	
	
	cmds.setAttr(newCv[0],0.5)
	cmds.setAttr(trmpikvis,1)
	cmds.setAttr(trmpfkvis[0],1)
	cmds.setDrivenKeyframe(trmpikvis,currentDriver=newCv[0])
	cmds.setDrivenKeyframe(trmpfkvis,currentDriver=newCv[0])
	
	
	cmds.setAttr(newCv[0],0)
	cmds.setAttr(trmpikvis,1)
	cmds.setAttr(trmpfkvis[0],0)
	cmds.setDrivenKeyframe(trmpikvis,currentDriver=newCv[0])
	cmds.setDrivenKeyframe(trmpfkvis,currentDriver=newCv[0])
	

		
	

	
def myPrimer(myjtText,mycvText):
	#myjtText=cmds.textField('jtText',q=1,text=1)	
	#mycvText=cmds.textField('cvText',q=1,text=1)	
	#mypadInt=cmds.intField('padInt',q=1,v=1)
	mypadInt=3
	cmds.pointConstraint(myjtText,mycvText,n='tmpCt')
	cmds.delete('tmpCt')
	print myjtText
	print mycvText
	cmds.parent(mycvText,myjtText)
	i=0
	while(i<mypadInt):
		if(i==0):
			newname=[mycvText[0] + '_wa']
			topNode=newname

		else:
			newname=[mycvText[0] + '_pad']

		cmds.group(mycvText,n=newname[0])
		i=i+1
		print topNode
		
	cmds.select(topNode)
	cmds.parent(w=1)
	cmds.makeIdentity(mycvText,apply=1,t=1,r=1,s=1,n=0)


