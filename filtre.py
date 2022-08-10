import math
from tkinter import Toplevel, Button, RIGHT, LEFT
import cv2
import numpy as np
import random
import statistics
# import Image
from PIL import Image
import PIL


class FilterFrame(Toplevel):

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        self.original_image = self.master.processed_image
        self.filtered_image = None
        self.filtered_image1 = None

        self.black_white_button = Button(master=self, text="Alb Negru")
        self.sepia_button = Button(master=self, text="Sepia")
        self.negativ_button = Button(master=self, text="Negativ")
        self.zgomot_button = Button(master=self, text="Zgomot")
        self.eliminarezgomot_button = Button(master=self, text="Eliminare Zgomot")
        self.evidentieremuchii_button = Button(master=self, text="Evidentierea Muchiilor")
        self.luminozitate_button = Button(master=self, text="Luminozitate")
        self.contur_button = Button(master=self, text="Contur")

        self.cancel_button = Button(master=self, text="Ieșire")
        self.apply_button = Button(master=self, text="Aplicare")

        self.black_white_button.bind("<ButtonRelease>", self.black_white_released)
        self.sepia_button.bind("<ButtonRelease>", self.sepia_released)
        self.negativ_button.bind("<ButtonRelease>", self.negativ_released)
        self.zgomot_button.bind("<ButtonRelease>", self.zgomot_released)
        self.eliminarezgomot_button.bind("<ButtonRelease>", self.eliminarezgomot_released)
        self.evidentieremuchii_button.bind("<ButtonRelease>", self.evidentieremuchii_released)
        self.luminozitate_button.bind("<ButtonRelease>", self.luminozitate_released)
        self.contur_button.bind("<ButtonRelease>", self.contur_released)

        self.apply_button.bind("<ButtonRelease>", self.apply_button_released)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_button_released)

        self.black_white_button.pack()
        self.sepia_button.pack()
        self.negativ_button.pack()
        self.zgomot_button.pack()
        self.eliminarezgomot_button.pack()
        self.evidentieremuchii_button.pack()
        self.luminozitate_button.pack()
        self.contur_button.pack()

        self.cancel_button.pack(side=RIGHT)
        self.apply_button.pack(side=LEFT)

    def black_white_released(self, event):
        self.black_white()
        self.show_image()

    def sepia_released(self, event):
        self.sepia()
        self.show_image()

    def negativ_released(self, event):
        self.negativ()
        self.show_image()

    def zgomot_released(self, event):
        self.zgomot()
        self.show_image()

    def eliminarezgomot_released(self, event):
        self.eliminarezgomot()
        self.show_image()

    def evidentieremuchii_released(self, event):
        self.evidentieremuchii()
        self.show_image()

    def luminozitate_released(self, event):
        self.luminozitate()
        self.show_image()

    def contur_released(self, event):
        self.contur()
        self.show_image()

    def apply_button_released(self, event):
        self.master.processed_image = self.filtered_image
        self.show_image()
        self.close()

    def cancel_button_released(self, event):
        self.master.image_viewer.show_image()
        self.close()

    def show_image(self):
        self.master.image_viewer.show_image(img=self.filtered_image)

    def black_white(self):
        linie, coloana = self.original_image.shape[:2]
        self.filtered_image = np.zeros((linie, coloana), dtype=np.uint8)  # o imagine neagra
        for i in range(linie):
            for j in range(coloana):
                # Pentru a face gri: 0．3Red + 0 . 59Green + 0 . 11 Blue
                # Pentru o imagine deschisa in format cv, pixelii au forma BGR
                self.filtered_image[i, j] = 0.3 * self.original_image[i, j][2] + \
                                            0.11 * self.original_image[i, j][0] + \
                                            0.59 * self.original_image[i, j][1]

    def sepia(self):
        #  newRed =   0.393*R + 0.769*G + 0.189*B
        #  newGreen = 0.349*R + 0.686*G + 0.168*B
        #  newBlue =  0.272*R + 0.534*G + 0.131*B
        self.filtered_image = self.original_image.copy()
        self.filtered_image = np.array(self.filtered_image, dtype=np.float64)  # float pentru a preveni pierderile
        self.filtered_image = cv2.transform(self.filtered_image, np.matrix([[0.272, 0.534, 0.131],
                                                                            [0.349, 0.686, 0.168],
                                                                            [0.393, 0.769,
                                                                             0.189]]))  # inmultim cu valorile pentru sepia
        self.filtered_image[np.where(self.filtered_image > 255)] = 255
        # daca o valoare este mai mare de 255, se va modifica ca fiind 255
        self.filtered_image = np.array(self.filtered_image, dtype=np.uint8)  # revenim la int
        # return self.filtered_image

    def negativ(self):
        linie, coloana = self.original_image.shape[:2]
        self.filtered_image = self.original_image.copy()
        for i in range(linie):
            for j in range(coloana):
                pixel = self.filtered_image[i, j]
                pixel[0] = 255 - pixel[0]
                pixel[1] = 255 - pixel[1]
                pixel[2] = 255 - pixel[2]
                self.filtered_image[i, j] = pixel

    def zgomot(self):
        linie, coloana = self.original_image.shape[:2]
        self.filtered_image = self.original_image.copy()
        p = 0.1  # cu cat p este mai mare, cu atat va fi mai mult zgomot

        # parcurgem imaginea
        for i in range(linie):
            for j in range(coloana):
                r = random.random()
                if r < p / 2:
                    self.filtered_image[i][j] = 0  # zgomot negru
                elif r < p:  # mai mare decat p/2 si mai mic decat p
                    self.filtered_image[i][j] = 255  # zgomot alb
                else:
                    self.filtered_image[i][j] = self.original_image[i][j].copy()  # ramane pixelul original

    def eliminarezgomot(self):
        # filtru median
        linie, coloana = self.original_image.shape[:2]
        self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        self.filtered_image = self.original_image.copy()

        for i in range(1, linie - 1):
            for j in range(1, coloana - 1):
                self.filtered_image[i, j] = statistics.median([self.original_image[i - 1, j - 1],
                                                               self.original_image[i - 1, j],
                                                               self.original_image[i - 1, j + 1],
                                                               self.original_image[i, j - 1],
                                                               self.original_image[i, j],
                                                               self.original_image[i, j + 1],
                                                               self.original_image[i + 1, j - 1],
                                                               self.original_image[i + 1, j],
                                                               self.original_image[i + 1, j + 1]])

        self.filtered_image = cv2.cvtColor(self.filtered_image, cv2.COLOR_GRAY2BGR)

    def evidentieremuchii(self):
        # high pass
        linie, coloana = self.original_image.shape[:2]
        self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        self.filtered_image = np.zeros(shape=(linie, coloana))

        sobel_filtered_vertical = np.zeros(shape=(linie, coloana))
        sobel_filtered_orizontal = np.zeros(shape=(linie, coloana))

        # sobel kernel
        sobel_orizontal = np.array([[-1, -2, -1],
                                    [0, 0, 0],
                                    [1, 2, 1]])

        sobel_vertical = np.array([[-1, 0, 1],
                                   [-2, 0, 2],
                                   [-1, 0, 1]])

        for i in range(linie - 2):
            for j in range(coloana - 2):
                vertical = np.sum(np.multiply(sobel_vertical, self.original_image[i:i + 3, j:j + 3]))
                sobel_filtered_vertical[i + 1, j + 1] = vertical
                orizontal = np.sum(np.multiply(sobel_orizontal, self.original_image[i:i + 3, j:j + 3]))
                sobel_filtered_orizontal[i + 1, j + 1] = orizontal
                self.filtered_image[i + 1, j + 1] = np.sqrt(vertical ** 2 + orizontal ** 2)  # find the magnitude

        # float -> int
        self.filtered_image = np.round(self.filtered_image).astype(np.uint8)

    def luminozitate(self):
        linie, coloana, canale = self.original_image.shape
        self.filtered_image = np.zeros((linie, coloana, canale), dtype=np.uint8)

        luminosity_factor = 1.5

        for i in range(linie):
            for j in range(coloana):

                pixel = self.original_image[i, j]
                pixel[0] = min(luminosity_factor * pixel[0], 255)
                pixel[1] = min(luminosity_factor * pixel[1], 255)
                pixel[2] = min(luminosity_factor * pixel[2], 255)
                self.filtered_image[i, j] = pixel

    def contur(self):
        linie, coloana, canale = self.original_image.shape
        self.filtered_image = np.zeros((linie, coloana, canale), dtype=np.uint8)
        self.filtered_image1 = np.zeros((linie, coloana, canale), dtype=np.uint8)
        for i in range(linie):
            for j in range(coloana):
                self.filtered_image1[i, j] = 0.3 * self.original_image[i, j][2] + \
                                            0.11 * self.original_image[i, j][0] + \
                                            0.59 * self.original_image[i, j][1]
        for i in range(1, linie-1):
             for j in range(1, coloana-1):
                pixel0 = self.filtered_image1[i - 1, j - 1]
                pixel1 = self.filtered_image1[i - 1, j]
                pixel2 = self.filtered_image1[i - 1, j + 1]
                pixel3 = self.filtered_image1[i, j - 1]
                pixel4 = self.filtered_image1[i, j]
                pixel5 = self.filtered_image1[i, j + 1]
                pixel6 = self.filtered_image1[i + 1, j - 1]
                pixel7 = self.filtered_image1[i + 1, j]
                pixel8 = self.filtered_image1[i + 1, j + 1]
                r = 8 * pixel4 - pixel1 - pixel2 - pixel3 - pixel0 - pixel5 - pixel6 -pixel7 - pixel8
                #r = r / 1
                #r = r + 128
                r = 255 - r
                self.filtered_image[i, j] = r


    def close(self):
        self.destroy()
