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

import os
import distutils
import distutils.sysconfig
import string
import numpy as np
import cv2
import cv2.cv as cv
import video
import common
import PIL
import win32gui
#for draw overlay image            
import wx 
import time 

from PIL import Image
from PIL import ImageGrab
from pytesser import *

#to clear clipboard
from ctypes import windll
## for keylogger
import pythoncom, pyHook, sys
import threading

from Tkinter import Tk


'''
from PIL import ImageGrab

'''

# 1 2 3 4 5


class App:
    key_storage = ''
    tag_current_clipboard = False
    tag_current_image = False
    tagID = 0
    def __init__(self, param):
        pass
    
    def OnKeyboardEvent(self,event):
        if chr(event.Ascii) == '#':
            self.key_storage = ''
            self.key_storage = '#'
        else:
            self.key_storage = self.key_storage + chr(event.Ascii)
            if self.key_storage.find('#tag'):
                #generate unique tag ID for image copy
                self.tag_current_clipboard = True
            
        print "Key: ", chr(event.Ascii)
        return True
    
    def SaveImage(self,TagID):
        im = ImageGrab.grabclipboard()
        if im <> None:
            im.save(str(TagID) + '.png','PNG')
            self.tag_current_image = False
            if windll.user32.OpenClipboard(None):
                windll.user32.EmptyClipboard()
                windll.user32.CloseClipboard()

    def init_keyboardlog(self):
        #setup keyboard hook to sniff keyboard key
        hm = pyHook.HookManager()
        hm.KeyDown = self.OnKeyboardEvent
        hm.HookKeyboard()
        pythoncom.PumpMessages()
        
    def addToClipBoard(self,text):
        command = 'echo ' + text.strip() + '| clip'
        os.system(command)

    def test(self):
        pass
    def run(self):
        while True:
            # Note 0 1 2 3 4 5 6 7 8 9 10 11 12 13 T A G N O T E
            flags, hcursor, (x,y) = win32gui.GetCursorInfo()
            self.mouse_x = x
            self.mouse_y = y
            
            im = ImageGrab.grab()
            width = 300
            height = 30
            box = (x - (width), y - (height/2), x + (width/2), y + (height/2))
            im_cropped = im.crop(box)
            pix = np.array(im_cropped.getdata()).reshape(im_cropped.size[0], im_cropped.size[1], 3)
            #pix = np.asarray(im_cropped)
            # To gray image
            imcv = np.asarray(im_cropped.convert('L'))
            #To gray
            #gray = cv2.cvtColor(pix, cv2.COLOR_GRAY2BGR)
            #Sharpen the image
            i = 3
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
    
            if string.find(result_string,'234') <> -1:
                self.draw(1)
            
            # 1 2 3 4 5
            # you can insert new comment with Tag
            if self.tag_current_clipboard:
                #generate the next ID
                #todo
                self.tagID = 656565
                self.addToClipBoard(str(self.tagID))
                self.tag_current_clipboard = False
                self.tag_current_image = True
                #tag this
                #paste the tag on to the clipboad
            if self.tag_current_image:
                self.SaveImage(self.tagID)
                
            cv2.waitKey(20)
    def draw(self,tagID):
    #draw over lay image on top of detected tag
        if tagID == 1:
            cv2.namedWindow('Tag1')
            cv2.moveWindow('Tag1', self.mouse_x + 400, self.mouse_y)
            fn = 'tag1.jpg'
            im_gray = cv2.imread(fn)
            cv2.imshow('Tag1', im_gray)
            

if __name__ == '__main__':
    
    print __doc__

    import sys
    
    site_packages = distutils.sysconfig.get_python_lib(plat_specific=1)
    build_no = open(os.path.join(site_packages, "pywin32.version.txt")).read().strip()
    print ("Python version = ",sys.version)
    print ("Opencv version = ",cv.__version__)
    #print("Qt version = ", QT_VERSION_STR)
    print("Numpy version = ", np.version.version)
    #print ("Matplotlib version = ",matplotlib.__version__)    
    print("PILLOW / PIL version = ",Image.VERSION)
    print("PyWin32 version = ",build_no)
    print("PyHook version = ",build_no)
    
    try: param = sys.argv[1]
    except: param = 0
    application = App(param)

    try:
        
        class myThread_1 (threading.Thread):
            def __init__(self, threadID, name, counter):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
                self.counter = counter
            def run(self):
                print "Starting " + self.name
                application.run()

        class myThread_2 (threading.Thread):
            def __init__(self, threadID, name, counter):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
                self.counter = counter
            def run(self):
                print "Starting " + self.name
                application.init_keyboardlog()
        
        # Create new threads
        thread1 = myThread_1(1, "Thread-1", 1)
        thread2 = myThread_2(2, "Thread-2", 2)
        
        # Start new Threads
        thread1.start()
        thread2.start()
        
        # 2 3 4 5
        # Add threads to thread list
        application.threads.append(thread1)
        application.threads.append(thread2)
        
        #thread.start_new_thread( application.Camera_Monitoring())
        #thread.start_new_thread( application.PathFinderMain())
        
    except:
        print "Error: unable to start thread"    
    #App(param).run()