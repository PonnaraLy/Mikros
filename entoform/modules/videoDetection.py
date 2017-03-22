import os
import sys
#Cherche le dossier "entoform"
entoPath='C:/Users/Faust/Desktop/ATI/Creavatures/entoform'
sys.path.append(entoPath)
#Creation du dossier avatar si ce dossier n'existe pas
#/!\ Ne pas modifier
avatarPath = entoPath+'/avatar' 
if not os.path.exists(avatarPath):
    os.makedirs(avatarPath)
import numpy as np
import cv2
import copy

class VideoDetection:
    def __init__(self,_vid):
        self.vid = _vid
        self.face_cascade = cv2.CascadeClassifier(entoPath+'/modules/haarcascades\haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(entoPath+'/modules/haarcascades\haarcascade_eye.xml')
        self.nose_cascade = cv2.CascadeClassifier(entoPath+'/modules/haarcascades\haarcascade_mcs_nose.xml')
        self.mouth_cascade = cv2.CascadeClassifier(entoPath+'/modules/haarcascades\haarcascade_smile.xml')       
    
    def moyenneCouleur(self,mat,matXSize,matYSize,idCouleur):
        moyenne = 0
        for v in range (matYSize):
            for u in range (matXSize):
                moyenne += mat[u,v][idCouleur]            
        moyenne = int(moyenne/(matYSize*matXSize))
        return moyenne   
    
    def moyenne(self,mat,matParameter):
        moyenne = 0
        for i in range(len(mat)):
            moyenne += mat[i][matParameter]
        moyenne = int(moyenne/len(mat))
        return moyenne

    #Prends comme donn�es la detection faciale   
    def faceDetectionGetInfo(self):
        faceInfos=[]
        ret,src = self.vid.read()
        gray_img = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray_img, 1.3, 5)
        eyesArray=[]
        nosesArray=[]
        mouthArray=[]

        if len(faces)>0:
            #print "get face"
            #Face Size
            faceInfos.append(self.moyenne(faces,2))  
            for (x,y,w,h) in faces:           
                roi_gray = gray_img[y:y+h, x:x+w]
                roi_color = src[y:y+h, x:x+w]
                eyes = self.eye_cascade.detectMultiScale(roi_gray)
                nose = self.nose_cascade.detectMultiScale(roi_gray)
                mouth = self.mouth_cascade.detectMultiScale(roi_gray)

                if len(eyes)>0:
                    #print "get eyes"
                    for (ex,ey,ew,eh) in eyes:
                       irisArray = []
                       partX = int(ew/3)
                       partY = int(eh/3)
                       roi_iris = src[y+ey+partY:y+ey+eh-partY, x+ex+partX:x+ex+ew-partX]
                       #Calcul de la couleur moyenne de l'iris de chaque oeil
                       #0:Bleu;1:Vert;2:Rouge
                       irisArray.append(self.moyenneCouleur(roi_iris,ew-(partX*2),eh-(partY*2),0))
                       irisArray.append(self.moyenneCouleur(roi_iris,ew-(partX*2),eh-(partY*2),1))
                       irisArray.append(self.moyenneCouleur(roi_iris,ew-(partX*2),eh-(partY*2),2))
                       eyesArray.append(irisArray)
                    #Iris Blue:
                    faceInfos.append(self.moyenne(eyesArray,0))
                    #Iris Green:
                    faceInfos.append(self.moyenne(eyesArray,1))
                    #Iris Red:
                    faceInfos.append(self.moyenne(eyesArray,2))
                else:
                    print "error on eyes"

                if len(nose)>0:
                    #print "get nose"
                    for (nx,ny,nw,nh) in nose:
                       noseDetailsArray=[]
                       noseDetailsArray.append(nw)
                       noseDetailsArray.append(nh)
                       nosesArray.append(noseDetailsArray)
                    #Nose Width:
                    faceInfos.append(self.moyenne(nosesArray,0))
                    #Nose Height:
                    faceInfos.append(self.moyenne(nosesArray,1))
                else:
                    print "error on nose"

                if len(mouth)>0:
                    #print "get mouth"
                    for (mx,my,mw,mh) in mouth:
                       mouthDetailsArray=[]
                       mouthDetailsArray.append(mw)
                       mouthDetailsArray.append(mh)
                       mouthArray.append(mouthDetailsArray)
                    #Mouth Width:
                    faceInfos.append(self.moyenne(mouthArray,0))
                    #Mouth Height:
                    faceInfos.append(self.moyenne(mouthArray,1))
                else:
                    print "error on mouth"

            return faceInfos
        else:
            print "error on faces"
            return []

    #Affiche la fenetre de la detection faciale
    def faceDetectionDisplay(self):
        ret,src = self.vid.read()
        faceDetection = copy.copy(src)
        gray_img = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray_img, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(faceDetection,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray_img[y:y+h, x:x+w]
            roi_color = faceDetection[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(roi_gray)
            nose = self.nose_cascade.detectMultiScale(roi_gray)
            mouth = self.mouth_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
               cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            for (nx,ny,nw,nh) in nose:
               cv2.rectangle(roi_color,(nx,ny),(nx+nw,ny+nh),(0,0,0),2)
            for (mx,my,mw,mh) in mouth:
               cv2.rectangle(roi_color,(mx,my),(mx+mw,my+mh),(255,255,255),2)
            
            
        cv2.imshow('Face Detection',faceDetection)

    #Affiche la video source (ici, celle de la webcam)
    def sourceDisplay(self):
        ret,src = self.vid.read()
        cv2.imshow('Source',src)

    #Fait une capture d'ecran et l'enregistre dans le dossier avatar cree automatiquement
    def captureScreen(self):
        files = os.listdir(avatarPath)
        nbFiles = len(files)
        ret,src = self.vid.read()
        cv2.imwrite(avatarPath+"/avatar"+str(nbFiles)+".png",src)     
