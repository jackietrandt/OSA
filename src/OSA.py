'''
Onscreen System Assistance
==================


Usage
-----
OSA.py 

Keys:
   SPACE  -  pause video

Select:
'''


import numpy as np
import cv2
import cv2.cv as cv
import video
import common
import PIL
import win32gui

from PIL import Image
from PIL import ImageGrab
from pytesser import *


class App:
    def __init__(self, param):
        #self.cap = video.create_capture(src)
        #self.frame = None
        self.test()
    
    #_____________________Test function for debug________________________________
    #__
    #____________________________________________________________________________
    #__
    #__
    def test(self):
        pass
    def run(self):
        while True:
            


        # Note 0 1 2 3 4 5 6 7 8 9 10 11 12 13 T A G N O T E
        

            flags, hcursor, (x,y) = win32gui.GetCursorInfo()
            im = ImageGrab.grab()
            width = 300
            height = 30
            box = (x - (width/2), y - (height/2), x + (width/2), y + (height/2))
            im_cropped = im.crop(box)
            pix = np.array(im_cropped.getdata()).reshape(im_cropped.size[0], im_cropped.size[1], 3)
            #pix = np.asarray(im_cropped)
            # To gray image
            imcv = np.asarray(im_cropped.convert('L'))
            #To gray
            #gray = cv2.cvtColor(pix, cv2.COLOR_GRAY2BGR)
            #Sharpen the image
            i = 5
            gaussian_blur = cv2.GaussianBlur(imcv,(i,i),0)
            sharpend = cv2.addWeighted(imcv, 1.5, gaussian_blur, -0.5,0)
            ## gray to binary: threshold = 100 (arbitrary); maxValue = 255; type = cv2.THRESH_BINARY
            flag, binaryImage = cv2.threshold(sharpend, 30, 255, cv2.THRESH_BINARY) # cv2.THRESH_BINARY = 0
            invertedImage = cv2.bitwise_not(binaryImage)
            image_big = cv2.resize(invertedImage, (int(invertedImage.shape[1] * 2), int(invertedImage.shape[0] * 2)))

            #cv2.imshow('input', image_big)
            sub = Image.fromarray(image_big)
            cv2.imwrite('Capture_bw.png', image_big)
            image = Image.open('Capture_bw.png')
            #r, g, b, a = image.split()

            #image = Image.merge("RGB", (r, g, b))
            result_string = image_to_string(sub)
            print result_string

            
            
            
            #cv2.imshow('plane', vis)
            ch = cv2.waitKey(1)
            if ch == ord(' '):
                self.paused = not self.paused
            if ch == 27:
                break





if __name__ == '__main__':
    
    print __doc__

    import sys
    print ("Python version = ",sys.version)
    print ("Opencv version = ",cv.__version__)
    #print("Qt version = ", QT_VERSION_STR)
    print("Numpy version = ", np.version.version)
    #print ("Matplotlib version = ",matplotlib.__version__)    
    print("PILLOW / PIL version = ",Image.VERSION)
    try: param = sys.argv[1]
    except: param = 0
    App(param).run()