import maya.cmds as cmds
import random
import copy
                
def createGrid(_size,_offset,_key,_pauseKey):
    objects = []
    grille = []
    
    if cmds.objExists('Conway'):
        cmds.delete('Conway')
    
    for i in range(_size):
        row = []
        for j in range(_size):
            cubeSize = random.randint(0, 1)
            row.append(cubeSize)
            cube = cmds.polyCube(n="cel"+str(1+(i*j)))
            cmds.move( i+(_offset*i), 0, j+(_offset*j))
            cmds.scale(0,0,0)
            cmds.currentTime(1)
            cmds.setKeyframe()  
            
            cmds.currentTime(_key)
            cmds.scale(cubeSize,cubeSize,cubeSize)
            cmds.setKeyframe()
            cmds.currentTime(_pauseKey+_key)  
            cmds.setKeyframe()              
            objects.append(cube[0])                            
        grille.append(row)
    cmds.group(objects,n="Conway")
    return grille

def isAlive(_currentCellule):
    if(_currentCellule == 1):
        return True
    else:
        return False
        
def checkVoisins(_x,_y,grille):    
    nbVoisins = 0
    try:
        if(isAlive(grille[_x-1][_y-1])):
            nbVoisins += 1   
    except:
        None
    try:
        if(isAlive(grille[_x-1][_y])):
            nbVoisins += 1  
    except:
       None     
    try:
        if(isAlive(grille[_x-1][_y+1])):
            nbVoisins += 1  
    except:
        None
    try:
        if(isAlive(grille[_x][_y-1])):
            nbVoisins += 1  
    except:
        None
    try:
        if(isAlive(grille[_x][_y+1])):
            nbVoisins += 1  
    except:
        None
    try:
        if(isAlive(grille[_x+1][_y-1])):
            nbVoisins += 1  
    except:
        None
    try:
        if(isAlive(grille[_x+1][_y])):
            nbVoisins += 1  
    except:
        None
    try:
        if(isAlive(grille[_x+1][_y+1])):
            nbVoisins += 1  
    except:
        None
    return nbVoisins
    
def rules(_nbVoisins,_currentState):
          
    if(_nbVoisins < 2 or _nbVoisins > 3):
        return 0
    if(_nbVoisins == 3):
        return 1
    if(_nbVoisins == 2):
        return _currentState

def conway1(_generation,_size,_grille,_key,_pauseKey):
    newGrille = []
    print("Grille: "+str(_grille))
    for i in range(_size):
        row = []
        for j in range(_size):     
            newState = rules(checkVoisins(i,j,_grille),_grille[i][j])
            row.append(newState)
            cmds.select("cel"+str((1+j)+(i*_size)))

            cmds.setKeyframe(t=_key+_pauseKey+_key*(_generation+1)+_pauseKey*_generation,at="scaleX",v=newState)
            cmds.setKeyframe(t=_key+_pauseKey+_key*(_generation+1)+_pauseKey*_generation,at="scaleY",v=newState)
            cmds.setKeyframe(t=_key+_pauseKey+_key*(_generation+1)+_pauseKey*_generation,at="scaleZ",v=newState)
            
            cmds.setKeyframe(t=_key+_pauseKey+_key*(_generation+1)+_pauseKey*(_generation+1),at="scaleX",v=newState)
            cmds.setKeyframe(t=_key+_pauseKey+_key*(_generation+1)+_pauseKey*(_generation+1),at="scaleY",v=newState)
            cmds.setKeyframe(t=_key+_pauseKey+_key*(_generation+1)+_pauseKey*(_generation+1),at="scaleZ",v=newState)
        newGrille.append(row)        
    return newGrille

def endAnimation(_key,_pauseKey,_generation,_size):
    print("End")
    for i in range(_size):
        for j in range(_size):  
            cmds.select("cel"+str((1+j)+(i*_size)))
            cmds.setKeyframe(t=_key+_key+_pauseKey+_key*(_generation+1)+_pauseKey*(_generation+1),at="scaleX",v=0)
            cmds.setKeyframe(t=_key+_key+_pauseKey+_key*(_generation+1)+_pauseKey*(_generation+1),at="scaleY",v=0)
            cmds.setKeyframe(t=_key+_key+_pauseKey+_key*(_generation+1)+_pauseKey*(_generation+1),at="scaleZ",v=0)
    
def conway(_size,_generation,_key,_keyPause,_offset):
    size = cmds.intField(_size,q=True,v=True)
    generation = cmds.intField(_generation,q=True,v=True)
    key = cmds.intField(_key,q=True,v=True)
    keyPause = cmds.intField(_keyPause,q=True,v=True)
    offset = cmds.floatField(_offset,q=True,v=True)
    
    print("GEN 0")
    grille = createGrid(size,offset,key,keyPause)
    print(grille)

    for i in range(generation):
        print("GEN "+str(i))
        grille = conway1(i,size,grille,key,keyPause)
        print(grille)
    endAnimation(key,keyPause,generation,size)
    
if cmds.window('Conway', exists=True):
    cmds.deleteUI('Conway')
    
fenetre = cmds.window('Conway',title="Conway 2D")
cmds.columnLayout()
cmds.text( label='Size Square',align="left")
size = cmds.intField(minValue=0)
cmds.text( label='\nGeneration',align="left")
generation = cmds.intField(minValue=0)
cmds.text( label='Key',align="left")
key = cmds.intField(minValue=0)
cmds.text( label='Pause Key',align="left")
pauseKey = cmds.intField(minValue=0)
cmds.text( label='\nOffset',align="left")
offset = cmds.floatField(minValue=0.0)

cmds.button(label='Generate',command="conway('"+size+"','"+generation+"','"+key+"','"+pauseKey+"','"+offset+"')")

cmds.showWindow(fenetre)
