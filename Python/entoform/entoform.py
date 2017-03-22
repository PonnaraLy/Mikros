import os
import sys
sys.path.append('C:/Users/Faust/Desktop/ATI/Creavatures/entoform/modules')

import numpy as np
import cv2
import copy
import videoDetection as vd
import entoformCreation as entoform
import maya.cmds as cmds

cap = cv2.VideoCapture(0)
video = vd.VideoDetection(cap)

if cmds.window('entoWindow', exists=True):
    cmds.deleteUI('entoWindow')
    
fenetre = cmds.window('entoWindow',title="Entoform Instructions")
cmds.columnLayout()
cmds.text( label="Les entoforms sont g�n�r�es � l'aide de la d�tection faciale et de l'adresse IP de la machine")
cmds.text( label="ECHAP : G�n�re l'entoform et prend une capture dans le dossier avatar qui sera g�n�r�")
cmds.text( label="/!\ Quatre cadres minimum doivent �tre pr�sents: ")
cmds.text( label="Bleu : Visage")
cmds.text( label="Vert : Yeux")
cmds.text( label="Noir : Nez")
cmds.text( label="Blanc : Bouche\n")
cmds.text( label="Pour quitter, appuyez quand m�me sur la touche ECHAP\n")
cmds.text( label="/!\ Si vous relancez le script alors que la fen�tre de la d�ection faciale est d�j� ouverte,")
cmds.text( label="vous devrez appuyer autant de fois sur la touche ECHAP que vous avez relanc� le script !\n")
cmds.showWindow(fenetre)

while True:
    #Affiche la vid�o source (pour Debug)
    #video.sourceDisplay()
    #Affiche la fen�tre de la d�tection faciale
    video.faceDetectionDisplay()
    
    if (cv2.waitKey(1)==27):
        faceInfos = video.faceDetectionGetInfo()
        print faceInfos
        if(len(faceInfos) == 8):
            video.captureScreen()
            entoform = entoform.Entoform(faceInfos)
        else:
			#print ()
			entoform = entoform.Entoform([231, 31, 34, 41, 82, 50, 20, 10])
            print "error on face detection"
        break

cmds.deleteUI(fenetre)
cv2.destroyAllWindows()
cap.release()
