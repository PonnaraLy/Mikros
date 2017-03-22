import maya.cmds as cmds
import random
import copy
                
def createGrid(_size,_offset,_key,_pauseKey):
    objects = []
    grille = []
    if cmds.objExists('Conway'):
        cmds.delete('Conway')
        
    for k in range(_size):
        height = []    
        for i in range(_size):
            row = []
            for j in range(_size):
                cubeSize = random.randint(0, 1)
                row.append(cubeSize)
                cube = cmds.polyCube(n="cel"+str(1+(i*j)))
                cmds.move( i+(_offset*i), k+(_offset*k), j+(_offset*j) )
                
                cmds.scale(0,0,0)
                cmds.currentTime(1)
                cmds.setKeyframe()  
                
                cmds.currentTime(_key)
                cmds.scale(cubeSize,cubeSize,cubeSize)                                
                cmds.setKeyframe()
                cmds.currentTime(_pauseKey+_key)  
                cmds.setKeyframe()           
                objects.append(cube[0])                            
            height.append(row)
        grille.append(height)
    cmds.group(objects,n="Conway")
    return grille

def isAlive(_currentCellule):
    if(_currentCellule == 1):
        return True
    else:
        return False
        
def checkVoisins(_x,_y,_z,grille):    
    nbVoisins = 0
    X = [_x-1,_x,_x+1]
    Y = [_y-1,_y,_y+1]
    Z = [_z-1,_z,_z+1]

    for k in range(len(Z)):
        for i in range(len(Y)):
            for j in range(len(X)):
                try:
                    if(k != Z[1] and i != Y[1] and j!=X[1] and isAlive(grille[Z[k]][Y[i]][X[j]])):
                        nbVoisins += 1   
                except:
                    None
   # print("Voisins: "+str(nbVoisins))
    return nbVoisins
    
def rules(_nbVoisins,_currentState):
          
    if(_nbVoisins <= 1 or _nbVoisins >= 8):
        return 0
    if(_nbVoisins == 5):
        return 1
    else:
        return _currentState

def conway1(_generation,_size,_grille,_key,_pauseKey):
    newGrille = []
    #print("Grille: "+str(_grille))
    
    for k in range(_size):
        height = []
        for i in range(_size):
            row = []
            for j in range(_size):     
                newState = rules(checkVoisins(i,j,k,_grille),_grille[k][i][j])
                
                row.append(newState)
                cmds.select("cel"+str((k*_size*_size+i*_size+j)+1))
    
                cmds.setKeyframe(t=_key+_pauseKey+_key*(_generation+1)+_pauseKey*_generation,at="scaleX",v=newState)
                cmds.setKeyframe(t=_key+_pauseKey+_key*(_generation+1)+_pauseKey*_generation,at="scaleY",v=newState)
                cmds.setKeyframe(t=_key+_pauseKey+_key*(_generation+1)+_pauseKey*_generation,at="scaleZ",v=newState)
                
                cmds.setKeyframe(t=_key+_pauseKey+_key*(_generation+1)+_pauseKey*(_generation+1),at="scaleX",v=newState)
                cmds.setKeyframe(t=_key+_pauseKey+_key*(_generation+1)+_pauseKey*(_generation+1),at="scaleY",v=newState)
                cmds.setKeyframe(t=_key+_pauseKey+_key*(_generation+1)+_pauseKey*(_generation+1),at="scaleZ",v=newState)
            height.append(row) 
        newGrille.append(height)      
    return newGrille

def endAnimation(_key,_pauseKey,_generation,_size):
    #○print("End")
    for k in range(_size):
        for i in range(_size):
            for j in range(_size):  
                cmds.select("cel"+str((k*_size*_size+i*_size+j)+1))
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
    
fenetre = cmds.window('Conway',title="Conway 3D")
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
