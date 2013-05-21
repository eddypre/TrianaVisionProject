#!/usr/bin/python

from pytesser import * 
import os
import Image
import sys
import cv2.cv as cv
import cv2
import pyscreenshot as ImageGrab
from PIL import *

cf = [0,0,0,0]
fich = open('positivas.txt','w')
def marcarCoordenadas(imagenes):
  global cf 
	cv.NamedWindow("salida")
	box = [-1,-1,0,0]
	tot = len(imagenes)
	for i in range(tot):
		nombre = imagenes.pop(0)
		#fich.write(nombre+' 1 ')
		imagen = cv.LoadImage(nombre)
                temp = cv.CloneImage(imagen)
                cv.SetMouseCallback('salida',funcion_mouse,imagen)
		while True:
			cv.Copy(imagen,temp)
			if drawing_box:
				draw_box(temp)
			cv.ShowImage('salida',temp)
			s = cv.WaitKey(10) 
			if s == 13:
				break
	fich.close()
	print 'archivo creado'

def funcion_mouse(event,x,y,flags,param):
	global drawing_box
	global box
	if event == cv.CV_EVENT_MOUSEMOVE:
		if drawing_box == True:
			box[2] = x - box[0]
			box[3] = y - box[1]
	elif event == cv.CV_EVENT_LBUTTONDOWN:
		drawing_box = True
		box = [x,y,0,0]
	elif event == cv.CV_EVENT_LBUTTONUP:
		drawing_box = False
		if box[2] < 0:
			box[0] +=box[2]
			box[2] *=-1
		if( box[3]<0):
			box[1] += box[3]
			box[3] *= -1
		cf = [box[0],box[1],box[2],box[3]]
		#fich.write(str(box[0])+' '+str(box[1])+' '+str(box[2])+' '+str(box[3])+'\n')
		fich.write(str(box[0])+'\n')
		fich.write(str(box[1])+'\n')
		fich.write(str(box[0]+box[2])+'\n')
		fich.write(str(box[1]+box[3])+'\n')		
		im=ImageGrab.grab(bbox=(box[0],box[1],box[0]+box[2],box[1]+box[3]))
		im=ImageGrab.grab(bbox=(0, 0, 640, 480))
		im.save('recortada.png')
                print 'coordenadas: '+str(box[0])+', '+str(box[1])+', '+str(box[0]+box[2])+', '+str(box[1]+box[3])

def draw_box(img):
	cv.Rectangle(img,(box[0],box[1]),(box[0]+box[2],box[1]+box[3]),cv.RGB(255,0,0))	

# NUEVO ********************************************************************************************

def recortar(c):
	img = cv2.imread("salida598.jpg")
	crop_img = img[c[1]:c[3], c[0]:c[2]] # Crop from x, y, w, h -> 100, 200, 100, 200
	#crop_img = img[166:189, 282:300] # Crop from x, y, w, h -> 100, 200, 100, 200

	#[0(inicio hacia abajo) : 400(hacia abajo), 0(inicio desde que tanto derecha) : 400(que tanto hacia la derecha)]
	cv2.imshow("cropped", crop_img)
	cv2.imwrite('out.png', crop_img)
	cv2.waitKey(0)

def binarizar():
	image = cv2.imread('out.png')
	gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	thresh = 115
	im_bw = cv2.threshold(gray_image, thresh, 255, cv2.THRESH_BINARY)[1]
	cv2.imwrite('bw.png', im_bw)

def leertxt():
	archi=open('positivas.txt','r')
	coords = []
	linea=archi.readline()
	while linea!="":
		coords.append(int(linea))
		print linea
		linea=archi.readline()
	archi.close()
	print coords
	return coords

def deteccion():
	im = Image.open('bw.png')
	text = image_to_string(im)
	print text
	return text

def escribir():
	fichero = open('salida.txt', 'w')
	texto = deteccion()
	fichero.write(str(texto))
	fichero.close()
	os.system("sh abrirGedit.sh")

# FIN DE NUEVO *************************************************************************************
 		
if __name__ == '__main__':
    drawing_box = False
    capture = cv.CreateCameraCapture(0)

    cv.NamedWindow("result", 1)
    i = 598 # Triana = 400
    imagenes = []
    if capture:
        frame_copy = None
        while True:
            frame = cv.QueryFrame(capture)
            if not frame:
                cv.WaitKey(0)
                break
            if not frame_copy:
                frame_copy = cv.CreateImage((frame.width,frame.height),
                                            cv.IPL_DEPTH_8U, frame.nChannels)
            if frame.origin == cv.IPL_ORIGIN_TL:
                cv.Copy(frame, frame_copy)
            else:
                cv.Flip(frame, frame_copy, 0)
	    
	    valor = cv.WaitKey(10)

            if valor == 32:
		nombre = "salida"+str(i)+".jpg"
		cv.SaveImage(nombre,frame_copy)
		i = i + 1
		imagenes.append(nombre)
		print 'guarde imagen, total: '+str(i)
		if i == 599: 
			break

            if valor == 27:
		print 'pique salir'
                break

	    cv.ShowImage("result", frame_copy)
    else:
        print 'algo malo paso'

    cv.DestroyWindow("result")
    marcarCoordenadas(imagenes)

    #NUEVO **************************************

    coords = leertxt()
    recortar(coords)
    binarizar()
    escribir()
