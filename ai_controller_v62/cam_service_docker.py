import cv2
import redis
from bson import ObjectId
import json
import pickle
#from common_utils import *


def singleton(cls):
    """
    This is a decorator which helps to create only 
    one instance of an object in the particular process.
    This helps the preserve the memory and prevent unwanted 
    creation of objects.
    """
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


@singleton    
class RedisKeyBuilderWorkstation():
    def __init__(self):
        # self.wid = get_workstation_id('livis//workstation_settings//settings_workstation.json')
        self.workstation_name = "WS_01" #get_workstation_by_id(self.wid)
    def get_key(self, camera_id, identifier):
        return "{}_{}_{}".format(self.workstation_name, str(camera_id), identifier)


import pickle

@singleton
class CacheHelper():
    def __init__(self):
        # self.redis_cache = redis.StrictRedis(host="164.52.194.78", port="8080", db=0, socket_timeout=1)
        self.redis_cache = redis.StrictRedis(host='localhost', port=6379, db=0, socket_timeout=60)
        # settings.REDIS_CLIENT_HOST
        print("REDIS CACHE UP!")

    def get_redis_pipeline(self):
        return self.redis_cache.pipeline()
    
    #should be {'key'  : 'value'} always
    def set_json(self, dict_obj):
        try:
            k, v = list(dict_obj.items())[0]
            v = pickle.dumps(v)
            return self.redis_cache.set(k, v)
        except redis.ConnectionError:
            return None

    def get_json(self, key):
        try:
            temp = self.redis_cache.get(key)
            #print(temp)\
            if temp:
                temp= pickle.loads(temp)
            return temp
        except redis.ConnectionError:
            return None
        return None

    def execute_pipe_commands(self, commands):
        #TBD to increase efficiency can chain commands for getting cache in one go
        return None

cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    if frame is not None:
        CacheHelper().set_json({"frame":frame})
        
