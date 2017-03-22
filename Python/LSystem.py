import maya.cmds as cmds
import copy

class LSystem:
    """Création d'un LSystem"""
    
    def __init__(self,_rule,_iteration,_alpha,_radius,_height):
        self.actions = {'F' : self.forward, '+':self.turnLeft, '-':self.turnRight, '[':self.savePos, ']':self.loadPos, '&':self.turnDown, '^':self.turnUp}
        self.rule = cmds.textField(_rule, q=True, text=True)
        self.angle = [0,0,0]
        self.iteration = cmds.intField(_iteration,q=True,v=True)
        self.txt = "F"
        self.radius = cmds.floatField(_radius,q=True,v=True)
        self.height = cmds.floatField(_height,q=True,v=True)
        self.pivotPos = [0,0,0]
        self.variousAngle = cmds.floatField(_alpha,q=True,v=True)
        
        self.saveAngle = []
        self.savePivotPos = []
        self.objects = []
        
        if(self.HasNoError(self.rule)):
            self.txt = self.LSystString(self.rule,self.iteration)
            print(self.txt)
            self.LSystActions(self.txt)
            cmds.group(self.objects)
            
    """Crée un tableau de chaîne de caractère"""
    def LSystString(self,_rule,_iteration):
        myTxt = self.txt
        for i in range(_iteration):
            myTxt = myTxt.replace("F", _rule)
        return str(myTxt)
    
    """Fait des actions à l'aide du tableau"""
    def LSystActions(self,_myTxt):
        for i in range(len(_myTxt)):
           self.actions[_myTxt[i]]()
    
    """Vérifie si la règle est écrite correctement"""        
    def HasNoError(self,_text):
        for i in range(len(_text)):
            if(_text[i] not in self.actions):
                print("Syntax error")
                return False
        return True
    
    def forward(self):
        print(self.pivotPos)
        print(self.angle)
        a = cmds.polyCylinder(h=self.height,r=self.radius)
        cmds.move(0, -self.height/2, 0, a[0]+".scalePivot",a[0]+".rotatePivot", os=True)
        cmds.move(self.pivotPos[0],self.pivotPos[1]+self.height/2,self.pivotPos[2])
        cmds.rotate(self.angle[0],self.angle[1],self.angle[2])
        cmds.move(0, self.height/2, 0, a[0]+".scalePivot",a[0]+".rotatePivot", os=True)
        self.pivotPos = cmds.xform(q=True,ws=True,rp=True)
        self.objects.append(a[0])
    
    def turnLeft(self):
        b = cmds.polySphere(r=self.radius)
        cmds.move(self.pivotPos[0],self.pivotPos[1],self.pivotPos[2])
        self.angle[0] += self.variousAngle
        self.pivotPos = cmds.xform(q=True,ws=True,rp=True)
        self.objects.append(b[0])
    
    def turnRight(self):
        c = cmds.polySphere(r=self.radius)
        cmds.move(self.pivotPos[0],self.pivotPos[1],self.pivotPos[2])
        self.angle[0] -= self.variousAngle
        self.pivotPos = cmds.xform(q=True,ws=True,rp=True)
        self.objects.append(c[0])
    
    def turnUp(self):
        d = cmds.polySphere(r=self.radius)
        cmds.move(self.pivotPos[0],self.pivotPos[1],self.pivotPos[2])
        self.angle[2] += self.variousAngle
        self.pivotPos = cmds.xform(q=True,ws=True,rp=True)
        self.objects.append(d[0])
    
    def turnDown(self):
        e = cmds.polySphere(r=self.radius)
        cmds.move(self.pivotPos[0],self.pivotPos[1],self.pivotPos[2])
        self.angle[2] -= self.variousAngle
        self.pivotPos = cmds.xform(q=True,ws=True,rp=True)
        self.objects.append(e[0])
     
    def savePos(self):
        lastPos = copy.copy(self.pivotPos)
        lastAngle = copy.copy(self.angle)
        self.savePivotPos.append(lastPos)
        self.saveAngle.append(lastAngle)
    
    def loadPos(self):    
        self.pivotPos = []
        self.angle = []
        self.angle = copy.copy(self.saveAngle[-1])
        self.pivotPos = copy.copy(self.savePivotPos[-1])
        self.savePivotPos.pop()
        self.saveAngle.pop()

def Presets(_rule,_iteration,_radius,_height,_alpha):
    cmds.textField(name, e=True, text=_rule)
    cmds.intField(iteration,e=True,v=_iteration)
    cmds.floatField(radius,e=True,v=_radius)
    cmds.floatField(height,e=True,v=_height)
    cmds.floatField(alpha,e=True,v=_alpha)
    
            
if cmds.window('LSyst', exists=True):
    cmds.deleteUI('LSyst')
    
fenetre = cmds.window('LSyst',title="L System")
cmds.columnLayout()
cmds.text( label='F= ')
name = cmds.textField(text = "F[+F]F[-F]F")
cmds.text( label='Iteration',align="left")
iteration = cmds.intField(minValue=0)
cmds.text( label='\nAngle',align="left")
alpha = cmds.floatField(minValue=0.0)
cmds.text( label='Radius',align="left")
radius = cmds.floatField(minValue=0.0)
cmds.text( label='Height',align="left")
height = cmds.floatField(minValue=0.0)
cmds.text( label='\nPresets')
cmds.button(label='Koch',command="Presets('F+F-F-F+F',3,0.2,2,90)")
cmds.button(label='Herbe',command="Presets('F[+F]F[-F]F',3,0.1,3.5,22.5)")
cmds.button(label='Herbe2',command="Presets('F[++F]F^[-&F]F',4,0.2,3,7.5)")
cmds.button(label='Arbre',command="Presets('FF-[-F+^^F+F]+[&F-F-F]',3,0.1,3,22.5)")
cmds.text( label='\n')
cmds.button(label='Generate',command="LSystem('"+name+"','"+iteration+"','"+alpha+"','"+radius+"','"+height+"')")
cmds.showWindow(fenetre)        