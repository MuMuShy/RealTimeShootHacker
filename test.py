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
def on_press(key):
    try:
        print('Alphanumeric key pressed: {0} '.format(
            key.char))
    except AttributeError:
        print('special key pressed: {0}'.format(
            key))

def on_release(key):
    print('Key released: {0}'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
#with keyboard.Listener(
#        on_press=on_press,
#        on_release=on_release) as listener:
#    listener.join()

# used to record the time when we processed last frame
prev_frame_time = 0

# used to record the time at which we processed current frame
new_frame_time = 0
#Counter-Strike: Global Offensive
wincap = WindowCapture('Apex Legends')
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
    params["net_resolution"] = "-1x384" #528x320 #640x384
    params["disable_blending"] = False #是否禁止渲染場景其他物件
    params["scale_gap"] = 0.5
    params["process_real_time"] = True
    #params["face"] = True
    params["render_pose"] = 2
    params["model_pose"] = "BODY_25"
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

    fireRange = 650
    fireareaLeftX = round(xs / 2) - round(fireRange/2)
    fireareaLeftY = round(ys / 2) - round(fireRange/2)
    fireareaDownX = fireareaLeftX+fireRange
    fireareaDownY = fireareaLeftY+fireRange
    while True:
        nowx, nowy = pyautogui.position()
        #print(nowx, nowy)
        img = wincap.get_screenshot()

        img_np = np.array(img)
        datum.cvInputData = img
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))

        font = cv2.FONT_HERSHEY_SIMPLEX
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time

        # converting the fps into integer
        fps = int(fps)
        fps = str(fps)
        cv2.putText(img, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)

        #imgShow = cv2.resize(imgShow, (800, 600), interpolation=cv2.INTER_AREA)
        cv2.imshow("frame",  img)

        if cv2.waitKey(1) & 0Xff == ord('q'):
            break

    cv2.destroyAllWindows()







except Exception as e:
    print(e)
    sys.exit(-1)