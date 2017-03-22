import maya.cmds as cmds
import random
import socket
import os
import sys

entoPath='C:/Users/Faust/Desktop/ATI/Creavatures/entoform'
sys.path.append(entoPath)

class Entoform:
    #Creation de l'entorform
    def __init__(self,faceTab):
        self.pattesAbdomen = [559,519,479,439,399]
        self.pattesAbdomen2 = [1135,1151,1167,1183,1199]
        self.nageoiresArray = [[908,888,928],[828,848,868],[948,968,988]]
        self.faceRange = 150
        self.faceInfo = faceTab
        self.creationSpheres(self.faceInfo[3],self.faceInfo[4])
        self.raccord("sphereR","sphereG","entoformPart1","[0:19]","[340:359]","[740:759]","[700:719]","[0:19]","[1060:1079]")
        self.raccord("entoformPart1","sphereB","entoformPart2","[700:719]","[360:379]","[1100:1119]","[1060:1079]","[720:739]","[1780:1799]")

        cmds.softSelect(sse=1)
        self.scaleBody("entoformPart2.e[160:179]",self.faceInfo[5])
        self.scaleBody("entoformPart2.e[880:899]",self.faceInfo[6])
        self.scaleBody("entoformPart2.e[1620:1639]",self.faceInfo[7])

        self.sculptCreature()
        cmds.softSelect(sse=0)
        cmds.symmetricModelling(axis='x',s=1,about='world')

        if self.faceInfo[0] < self.faceRange:
            nombreNageoires = int(1+random.random()*3)
            self.nageoires(nombreNageoires,self.nageoiresArray)        
        else:
            nombrePattes = int(2+random.random()*4)
            self.pattes(nombrePattes,self.pattesAbdomen,0.005)
            self.pattes(nombrePattes,self.pattesAbdomen2,0.05)
        self.couleur("entoformPart2")
        cmds.select("entoformPart2")
        cmds.polySmooth()

        files = os.listdir(entoPath+'/avatar')
        nbFiles = len(files)
        cmds.rename('entoformPart2', 'avatar'+str(nbFiles-1))
        
    def raccord(self,object1,object2,nameDst,faces1,faces2,faces3,faces4,edge1,edge2):
        entoform = cmds.polyUnite(object1,object2,name=nameDst)
        cmds.delete(constructionHistory=True)
        
        cmds.delete(nameDst+".f"+faces1)
        cmds.delete(nameDst+".f"+faces2)
        cmds.delete(nameDst+".f"+faces3)
        cmds.delete(nameDst+".f"+faces4)
        
        cmds.polyBridgeEdge(nameDst+".e"+edge1,nameDst+".e"+edge2)

    def creationSpheres(self,mouthWidth,mouthHeight):
        cmds.polySphere(axis=[0,0,1],name="sphereR")
        cmds.scale(mouthWidth*0.01,mouthHeight*0.01,1)
        cmds.move(0,0,2)
        cmds.polySphere(axis=[0,0,1],name="sphereG")
        cmds.scale(mouthWidth*0.01,mouthHeight*0.01,1)
        cmds.polySphere(axis=[0,0,1],name="sphereB")
        cmds.scale(mouthWidth*0.01,mouthHeight*0.01,1)
        cmds.move(0,0,-2)

    def scaleBody(self,selected,irisInfo):
        cmds.select(selected)
        cmds.scale(1,random.random()+irisInfo*0.01,1)
    
    def sculptCreature(self):
        headSize = 0.2
        moveZDebug = 0.23
        moveZHead = -0.93
        scaleXBody = 0.46
        moveZBody = 0.47
        cmds.select("entoformPart2.f[143]")
        cmds.scale(headSize,headSize,headSize)
        cmds.move(0,0,moveZDebug,relative=True)
        cmds.select("entoformPart2.f[324]")
        cmds.move(0,0,moveZHead,relative=True)
        cmds.select("entoformPart2.f[463:464]")
        cmds.scale(scaleXBody,1,1)
        cmds.select("entoformPart2.f[1116:1117]")
        cmds.move(0,0,moveZBody,relative=True)

    def pattes(self,nbPattes,pattesTab,coefHauteur):
        for i in range(nbPattes):
            cmds.select("entoformPart2.f["+str(pattesTab[i])+"]",sym=1)
            faces = cmds.ls(sl=True)       
            for f in range(len(faces)):
                cmds.polyExtrudeFacet(faces[f],localTranslate=[0,0,self.faceInfo[1]*0.01])
                cmds.polyExtrudeFacet(faces[f],localTranslate=[0,0,self.faceInfo[1]*coefHauteur])

    def nageoires(self,nbNageoires,nageoiresTab):
        for n in range(nbNageoires):
            for f in range(len(nageoiresTab[n])):
                cmds.select("entoformPart2.f["+str(nageoiresTab[n][f])+"]",sym=1)
                faces = cmds.ls(sl=True)
                for f in range(len(faces)):
                    cmds.polyExtrudeFacet(faces[f],localTranslate=[0,0,self.faceInfo[1]*0.01])
                    cmds.polyExtrudeFacet(faces[f],localTranslate=[0,0,self.faceInfo[1]*0.005])
                    cmds.move(0,0,0.1,relative=True)

    def couleur(self,creature):
        ipAdress = socket.gethostbyname(socket.gethostname())
        colorArray = ipAdress.split(".")
        color3 = colorArray[2]+colorArray[3]
        colorArray.pop()
        colorArray.pop()
        colorArray.append(color3)
        random.shuffle(colorArray)    
        shader=cmds.shadingNode("lambert",asShader=True)
        cmds.setAttr(shader + '.color', float(int(colorArray[0])/255.0), float(int(colorArray[1])/255.0), float(int(colorArray[2])/255.0), type="double3")
        cmds.select(creature)
        cmds.hyperShade( assign=shader)
