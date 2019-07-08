# -- coding: UTF-8 --
# -- Linter: Pylint --
# -- Python ver. 3.7.3 --
# -- PySimpleGUI ver. 3.37.0
# -- opencv-python ver. 4.1.0.25
"""OpenCV Licence
Copyright (C) 2000-2019, Intel Corporation, all rights reserved.
Copyright (C) 2009-2011, Willow Garage Inc., all rights reserved.
Copyright (C) 2009-2016, NVIDIA Corporation, all rights reserved.
Copyright (C) 2010-2013, Advanced Micro Devices, Inc., all rights reserved.
Copyright (C) 2015-2016, OpenCV Foundation, all rights reserved.
Copyright (C) 2015-2016, Itseez Inc., all rights reserved.
Third party copyrights are property of their respective owners.

OpenCV was built to provide a common infrastructure for computer vision
applications and to accelerate the use of machine perception in the
commercial products.
Being a BSD-licensed product, OpenCV makes it easy for businesses to
utilize and modify the code."""

# -- Imports
import urllib.request
from os.path import normpath, realpath

import cv2
import numpy as np
import PySimpleGUI as sg


# -- Definición de funciones

def tryload():

    # -- Carga de cascadas e info OPENCV/CPU
    print("-"*100)
    print("Hilos:", cv2.getNumThreads())
    print("Nucleos:", cv2.getNumberOfCPUs())
    print("OpenCV optimizado:", cv2.useOptimized())
    print("-"*100)
    file = frontalface_cascades.read()
    # frontalface_cascade.load(cv2.samples.findFile(file)):
    if not frontalface_cascade.load(cv2.samples.findFile(file)):
        print(' -- (!)Error cargando "face cascade"')
        exit(0)
    file = profileface_cascades.read()
    if not profileface_cascade.load(cv2.samples.findFile(file)):
        print(' -- (!)Error cargando "face cascade"')
        exit(0)
    file = eyes_cascades.read()
    if not eyes_cascade.load(cv2.samples.findFile(file)):
        print(' -- (!)Error cargando "eyes cascade"')
        exit(0)
    file = smile_cascades.read()
    if not smile_cascade.load(cv2.samples.findFile(file)):
        print(' -- (!)EError cargando "smile cascade"')
        exit(0)
    playvideo()
# -- Función modificada por Cristian 06-06-2019


def detect_and_display(frame):
    # -- Función encargada de detectar y dibujar las cascadas
    frame_color = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.equalizeHist(frame_color)
    # -- Detectar caras de frente
    ffaces = frontalface_cascade.detectMultiScale(frame_gray, 1.25, 5)
    if type(ffaces) != type(tuple):
        for i in ffaces:
            print(i)
    #print(type(ffaces))
    if len(ffaces) > 0:
        for (x, y, w, h) in ffaces:
            top_left = (x, y)
            botom_right = (x+w, y+h)
            faceROI = frame_gray[y:y+h, x:x+w]
            faceColor = frame[y:y+h, x:x+w]
            frame = cv2.rectangle(frame,
                                  top_left, botom_right, (43, 248, 243), 1)
            cv2.circle(frame, (x,y), (15),(255,0,255), 1)
            faces_xywh = str(x), str(y), str(w), str(h)
            faces_str = str(faces_xywh)
            cv2.putText(frame, faces_str,
                        (x-15, y-15), cv2.FONT_HERSHEY_PLAIN,
                        1, (255, 0, 255), 1)
            # -- Detectar ojos
            eyes = eyes_cascade.detectMultiScale(faceROI)
            for (x2, y2, w2, h2) in eyes:
                eye_center = (x + x2 + w2//2, y + y2 + h2//2)
                radius = int((w2 + h2)*0.25)
                cv2.circle(frame,
                           eye_center, radius, (43, 248, 243), 1)
            # -- Detectar sonrisas
            smiles = smile_cascade.detectMultiScale(faceROI, 1.3, 26)
            for (x3, y3, w3, h3) in smiles:
                top_left = (x3, y3)
                botom_right = (x3 + w3, y3 + h3)
                cv2.rectangle(faceColor,
                              top_left, botom_right, (43, 248, 243), 1)
                cv2.putText(frame, "Sonriendo",
                            (x-15, y + 250), cv2.FONT_HERSHEY_PLAIN,
                            1, (255, 0, 255), 1)
    else:
        # -- Detectar caras de frente
        pfaces = profileface_cascade.detectMultiScale(frame_gray, 1.3, 2)
        for (x, y, w, h) in pfaces:
            top_left = (x, y)
            botom_right = (x+w, y+h)
            faceROI = frame_gray[y:y+h, x:x+w]
            faceColor = frame[y:y+h, x:x+w]
            frame = cv2.rectangle(frame,
                                  top_left, botom_right, (43, 248, 243), 1)
            faces_xywh = str(x), str(y), str(w), str(h)
            faces_str = str(faces_xywh)
            cv2.putText(frame, faces_str,
                        (x-15, y-15), cv2.FONT_HERSHEY_PLAIN,
                        1, (255, 0, 255), 1)
    cv2.imshow('IP Camera - Deteccion de caras', frame)
# -- Función modificada por Cristian 06-06-2019


def readvideo():
    # -- Intentar capturar video streaming
    success = False
    count = 1
    while not success:
        try:
            imgResp = urllib.request.urlopen(url.load())
            imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
            img = cv2.imdecode(imgNp, -1)
            success = True
            return img
        except Exception as e:
            yesno = sg.PopupYesNo(
                'Error al conectar, ¿Desea reintentar la conexión?',
                '\n(Intento %d/3)\n\n' % count,
                'Detalle del error: %s\n\n' % e,
                title='Error')
            if yesno == 'Yes':
                count += 1
                if count > 3:
                    return
            else:
                sg.PopupAutoClose('Cancelando la conexión', title='Open CV')
                return
# -- Función modificada por Cristian 06-06-2019


# -- Reproducir el video capturado.
def playvideo():
    while True:
        img = readvideo()
        if img is None:
            sg.PopupAutoClose(
                'No se ha logrado capturar una imagen',
                'Streaming finalizado', title='Error')
            exit(0)
        cv2.useOptimized()
        detect_and_display(img)
        if cv2.waitKey(1) == ord('q'):
            # -- Consulta de seguridad para finalizar streaming proceso
            yesno = sg.PopupYesNo(
                '¿Esta seguro que desea cerrar el streaming?',
                title='OpenCV Camera')
            if yesno == 'Yes':
                sg.PopupAutoClose(
                    'El streaming de la IP Camera ha terminado',
                    title='OpenCV Camera')
                exit(0)
            else:
                pass
# -- Función modificada por Cristian 06-06-2019.


# -- Clases definidas
class video:

    # -- Crea la clase video con su respectivo URL
    def __init__(self, url_video):
        self.url = url_video

    def load(self):
        return self.url
# -- Clase modificada por Cristian 05-06-2019


class cascada:

    # -- Crea la clase cascada con su respectiva dirección PATH
    def __init__(self, dir_path):
        path_str = r'%s' % dir_path
        path_str = str(path_str).replace('\\', '\\\\')
        self.dir_path = path_str

    def read(self):
        return self.dir_path
# -- Clase modificada por Cristian 06-06-2019


# -- Proceso principal
# -- Se crean objetos con sus respectivos atributos
frontalface_cascades = cascada(normpath(realpath(
    'D:/OpenCV/opencv/sources/data/' +
    'lbpcascades/lbpcascade_frontalface_improved.xml')))
profileface_cascades = cascada(normpath(realpath(
    'D:/OpenCV/opencv/sources/data/' +
    'lbpcascades/lbpcascade_profileface.xml')))
eyes_cascades = cascada(normpath(realpath(
    'D:/OpenCV/opencv/sources/data/' +
    'haarcascades/haarcascade_eye_tree_eyeglasses.xml')))
smile_cascades = cascada(normpath(realpath(
    'D:/OpenCV/opencv/sources/data/' +
    'haarcascades/haarcascade_smile.xml')))
frontalface_cascade = cv2.CascadeClassifier()
profileface_cascade = cv2.CascadeClassifier()
eyes_cascade = cv2.CascadeClassifier()
smile_cascade = cv2.CascadeClassifier()

# -- Consulta inicial para empezar proceso
yesno = sg.PopupYesNo(
    'Bienvenido\n¿Desea iniciar el streaming de la IP camera?',
    title='OpenCV Camera')
if yesno == 'Yes':
    url = video('http://192.168.43.112:8080/shot.jpg')
    tryload()
    playvideo()
else:
    sg.PopupAutoClose(
        'El streaming de la IP Camera ha sido cancelado',
        title='OpenCV Camera')
