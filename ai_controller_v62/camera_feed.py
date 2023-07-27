import neoapi
import datetime
import cv2
import time
import numpy as np
from common_utils import *
from inference import *
from ai_settings import *
import camera_module


# def config_file1():
#     baumer_ip = []
#     baumer_ip.append("192.168.137.2")
#     # baumer_ip.append("192.168.1.3")
#     return baumer_ip
# cap=cv2.VideoCapture(0)
try:
    cam_1 = camera_module.camera('baumer','192.168.32.2')
except:
    print('camera not connecetd ..!!!')
    sys.exit(0)


while True:
        
    # ret,frame=cap.read()
    try:
        baumer_camera_1 = cam_1.fetch_image()
        CacheHelper().set_json({"baumer_input_frame":baumer_camera_1})
    except Exception as e:
        print(e)

