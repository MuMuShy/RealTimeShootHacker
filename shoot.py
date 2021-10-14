import sys
import cv2
import os
from sys import platform
import argparse
import numpy as np
from math import pi,asin
from PIL import ImageGrab
from mss import mss
from PIL import Image
import pyautogui
import keyboard as kb
import time
import math
import win32api, win32con
import operator
xs = 1920
ys = 1080
from pynput import keyboard
from windowcapture import WindowCapture

_activekey = "t"
_isActive = False
def on_press(key):
    global _isActive
    global _activekey
    try:
        #print('Alphanumeric key pressed: {0} '.format(key.char))
        if key.char == _activekey:
            print("案啟動鍵")
            if _isActive == True:
                _isActive = False
            else:
                _isActive = True
    except AttributeError:
        print('special key pressed: {0}'.format(
            key))

def on_release(key):
    print('Key released: {0}'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def listen():
    listener = keyboard.Listener(on_press = on_press,
                                 on_release = on_release)

    listener.start()

# used to record the time when we processed last frame
prev_frame_time = 0

# used to record the time at which we processed current frame
new_frame_time = 0
#Counter-Strike: Global Offensive
#Apex Legends
wincap = WindowCapture('Counter-Strike: Global Offensive')
pyautogui.FAILSAFE = False


def cropND(img, bounding):
    start = tuple(map(lambda a, da: a//2-da//2, img.shape, bounding))
    end = tuple(map(operator.add, start, bounding))
    slices = tuple(map(slice, start, end))
    return img[slices]
try:
    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        # Windows Import
        if platform == "win32":
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append(dir_path + '/openposelib/');
            os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + './x64/Release;' +  dir_path + './bin;'
            import pyopenpose as op
        else:
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append('../../python');
            # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
            # sys.path.append('/usr/local/python')
            from openpose import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e

    # Flags
    parser = argparse.ArgumentParser()
    args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "./models/"
    params["net_resolution"] = "-1x320" #528x320 #640x384
    params["disable_blending"] = False #是否禁止渲染場景其他物件
    params["scale_gap"] = 0.3
    params["process_real_time"] = True
    #params["face"] = True
    params["render_pose"] = 1
    params["scale_number"] = 1
    params["model_pose"] = "BODY_25" #BODY_25
    print(cv2.cuda.getCudaEnabledDeviceCount())


    # Construct it from system arguments
    # op.init_argv(args[1])
    # oppython = op.OpenposePython()

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()
    # Process Imagec
    datum = op.Datum()
    temp_list=[]

    fireRange = 1000
    fireareaLeftX = round(xs / 2) - round(fireRange/2)
    fireareaLeftY = round(ys / 2) - round(fireRange/2)
    fireareaDownX = fireareaLeftX+fireRange
    fireareaDownY = fireareaLeftY+fireRange
    listen()

    font = cv2.FONT_HERSHEY_SIMPLEX
    while True:
        key = cv2.waitKey(1)
        nowx, nowy = pyautogui.position()
        img = wincap.get_screenshot()
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time

        # converting the fps into integer
        fps = int(fps)
        fps = str(fps)
        if key & 0Xff == ord('q'):
            break

        if _isActive == True:
            datum.cvInputData = img
            opWrapper.emplaceAndPop(op.VectorDatum([datum]))
            detectedResult = datum.poseKeypoints
            IsShoot = False
            hasTarget = False
            target_x = 0
            target_y = 0
            imgShow = datum.cvOutputData
            cv2.rectangle(imgShow, (fireareaLeftX,fireareaLeftY), (fireareaDownX,fireareaDownY), (0, 255, 0), 2)
            if detectedResult is not None and len(detectedResult)>0:
                numberPeopleDetected = len(detectedResult);
                dis = 9999999
                for i in range(numberPeopleDetected):
                    temp_x =(detectedResult[i][0][0])
                    temp_y =(detectedResult[i][0][1])
                    distance = math.hypot(temp_x - (fireareaLeftX+fireRange/2), temp_y- (fireareaLeftY+fireRange/2))
                    cv2.putText(imgShow, "out side distance: " + str(distance), (round(temp_x), round(temp_x)), cv2.FONT_HERSHEY_SIMPLEX, 1,(255, 255, 255), 3, cv2.LINE_AA)
                    if temp_x>fireareaLeftX and temp_x<fireareaDownX and temp_y>fireareaLeftY and temp_y<fireareaDownY:
                        hasTarget = True
                        if distance<dis: #範圍內最近的
                            x = temp_x
                            y = temp_y
                            strpos = "x:"+str(x)+"/y:"+str(y)
                            dis = distance
                            cv2.putText(imgShow, "target distance: "+str(dis), (round(x), round(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 123), 3,cv2.LINE_AA)
                if hasTarget is True:
                    target_x = x
                    target_y = y
                    nx = round((x-(xs/2))/1.6)  #1920*1080 -> 1.6
                    ny = round(((y-(ys/2))+40)/1.6)  #1920*1080 -> 1.6
                    #print("Detected! Shoot pos",str(target_x),"/",str(target_y),"  distance X:", str(target_x-(xs/2)))
                    #temp_list.append([nx,ny])
                    #print(temp_list)
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, nx, ny)
                    time.sleep(0.01)
                    IsShoot = True
                else:
                    #print("no click")
                    IsShoot = False


            #imgShow = cv2.resize(imgShow, (640, 360))
            # font which we will be using to display FPS


            cv2.putText(imgShow, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
            if IsShoot is True:
                #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                #time.sleep(0.01)
                imgShow = cv2.circle(imgShow,(round(target_x),round(target_y)),10,(0,0,255),-1)
                cv2.putText(imgShow, "shoot!", (round(target_x),round(target_y)), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
            else:
                #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                time.sleep(0.01)

            #imgShow = cv2.resize(imgShow, (800, 600), interpolation=cv2.INTER_AREA)
            cv2.imshow("frame",  imgShow)
        else:
            cv2.putText(img, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
            cv2.imshow("frame",  img)



    cv2.destroyAllWindows()







except Exception as e:
    print(e)
    sys.exit(-1)