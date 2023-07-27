from re import X
from automate.settings import MONGO_SERVER_HOST,MONGO_SERVER_PORT,MONGO_DB,REDIS_CLIENT_HOST,REDIS_CLIENT_PORT
from bson import ObjectId
import datetime
import time
import base64
import uuid 
import datetime
import numpy as np
import sqlite3
from pymongo import MongoClient
import json
import sys
import redis
import pickle
import cv2




def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance



@singleton
class MongoHelper:
    client = None
    def __init__(self):
        if not self.client:
            self.client = MongoClient(host=MONGO_SERVER_HOST, port=MONGO_SERVER_PORT)
        self.db = self.client[MONGO_DB]

    def getDatabase(self):
        return self.db

    def getCollection(self, cname, create=False, codec_options=None, domain_override = None):
        _DB = MONGO_DB
        DB = self.client[_DB]
        # if cname in MONGO_COLLECTIONS:
        #     if codec_options:
        #         return DB.get_collection(MONGO_COLLECTIONS[cname], codec_options=codec_options)
        #     return DB[MONGO_COLLECTIONS[cname]]
        # else:
        return DB[cname]


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        else:
            return obj


@singleton
class CacheHelper():
    def __init__(self):
        # self.redis_cache = rediStrictRedis(host="164.52.194.78", port="8080", db=0, socket_timeout=1)
        self.redis_cache = redis.StrictRedis(host=REDIS_CLIENT_HOST, port=REDIS_CLIENT_PORT, db=0, socket_timeout=60)
        REDIS_CLIENT_HOST
        print("REDIS CACHE UP!")

    def get_redis_pipeline(self):
        return self.redis_cache.pipeline()
    
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




def get_running_process_util():
    """
        Usage: Return the inspection_id if the start process was initiated, and the inspection process is running. With the
            input workstation_id we query the inspection collection for process started and return the inspection ID of
            the running process.
        Request Parameters: {
                        "workstation_id": "6224257708f3e625aa6b3b26"
                        }
        Request Method: GET
        Response: [
            {   "_id":"87597596997",
                "part_id": "61d4257708f3e625aa6b3b26"
                "workstation_id": "6392257708f3e625aa6b3b26",
                "plan_id":plan_id,
                "start_time":createdAt,
                "end_time":"",
                "shift_id":shift_id,
                "operator_id":operator_id,
                "produced_on":current_date,
                "status":"started",
                "inference_urls" : ["url1","url2"]
                }
                ]

    """
    mp = MongoHelper().getCollection('current_inspection')
    doc = mp.find_one()

    if doc:
        current_id = doc["current_inspection_id"]
        from automate.settings import INSPECTION_COLLECTION
        mp = MongoHelper().getCollection(INSPECTION_COLLECTION)
        insp_coll = mp.find_one({'_id':ObjectId(current_id)})

        return [insp_coll], 200
    else:
        return [],200


def get_metrics_util(inspection_id):
    """
        Usage: Return the report of the the current inspection happening, that is stored in database. This information
            is used in the operator panel dashboard to convey to the user the current inspection process results.
        Request Parameters: {
                            "inspection_id": "6224257708f3e625aa6b3b26"
                            }
        Request Method: GET
        Response: {
                    "part_id": "61d4257708f3e625aa6b3b26"
                    "workstation_id": "6392257708f3e625aa6b3b26",
                    "plan_id":plan_id,
                    "start_time":createdAt,
                    "end_time":"",
                    "shift_id":shift_id,
                    "operator_id":operator_id,
                    "produced_on":current_date,
                    "status":"started",
                    "inference_urls" : ["url1","url2"],
                    "duration":"",
                    "total_accpeted":100,
                    "total_rejected":10,
                    "total":110
                }
        """


    mp = MongoHelper().getCollection( str(inspection_id) + "_" + "log")
    dataset = [p for p in mp.find().sort( "$natural", -1 )]
    # print(" dataset is ",dataset)
    # dataset1 = [p for p in mp.find({"isAccepted":True})]
    # dataset2 = [p for p in mp.find({"isAccepted":False})]

    dataset1 = [p for p in mp.find({"status":"Accepted"})]
    dataset2 = [p for p in mp.find({"status":"Rejected"})]

    
    total_production = len(dataset)
    total_accepted_count = len(dataset1)
    total_rejected_count = len(dataset2)

    if len(dataset) > 0:
        dataset = dataset[0]
        #s = datetime.datetime.strptime(dataset.get('inference_start_time',""), '%Y-%m-%d %H:%M:%S')
        #e = datetime.datetime.strptime(dataset.get('inference_end_time',""), '%Y-%m-%d %H:%M:%S')
        #dataset['duration'] = str(e-s)
        dataset['total'] = str(total_production)
        dataset['total_accepted'] = str(total_accepted_count)
        dataset['total_rejected'] = str(total_rejected_count)
        # x = dataset['inference_frame']
        # dataset['inference_frame'] = X
        #dataset['inference_urls'] = inference_urls
    else:
        dataset = {}
    return dataset, 200
    
    
def start_process_util(data):
    """
        Usage:  Start the inspection process for the given time frame eg: day/night shift or plan and storing
                in the database with  part id, start time etc.
        Request Parameters: {
                "part_id":"61d4257708f3e625aa6b3b26",
                "workstation_id": "6224257708f3e625aa6b3b26"
                }
        Request Method: POST
        Response: {
                "part_id": "61d4257708f3e625aa6b3b26"
                "workstation_id": "6392257708f3e625aa6b3b26",
                "plan_id":plan_id,
                "start_time":createdAt,
                "end_time":"",
                "shift_id":shift_id,
                "operator_id":operator_id,
                "produced_on":current_date,
                "status":"started",
                "inference_urls" : ["url1","url2"]
                }

    """

    part_name = data.get('part_name',None)
    CacheHelper().set_json({"part_name":part_name})
    
    if part_name is None:
        return "Please provide part name", 400

    mp = MongoHelper().getCollection('model_check')
    mp_data = mp.find_one()
    if not mp_data:
        mp.insert_one({"selected_model":part_name,"curent_running_model":part_name})
    else:
        newvalues = { "$set": { "selected_model": part_name,"current_running_model": None } }
        mp.update_one({'_id':mp_data['_id']}, newvalues)
    CacheHelper().set_json({"part_name":part_name})

    from automate.settings import INSPECTION_COLLECTION
    mp = MongoHelper().getCollection(INSPECTION_COLLECTION)
    current_date = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    createdAt = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    coll = {
    "part_name":part_name,
    "start_time":createdAt,
    "end_time":"",
    "produced_on":current_date,
    "status":"started",
    }

    _id = mp.insert(coll)

    ## adding to current_inspection
    bb = MongoHelper().getCollection('current_inspection')
    ps = bb.find_one()
    if ps is None:
        bb.insert_one({'current_inspection_id': str(_id)})
    else:
        ps['current_inspection_id'] = str(_id)
        bb.update({"_id": ps['_id']}, {"$set": ps})
    
    ret = mp.find_one({'_id' : _id})
    return ret ,200



def get_redis_image_util(key):
    rec = CacheHelper()
    while True:
        
        frame = rec.get_json(key)

       
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def start_inspection_util(data):
    inspection_id = data.get("inspection_id",None)
    part_name = data.get("part_name",None)

    try:
        
        message = "Inspection starts"
        CacheHelper().set_json({"inspection_trigger":True})
        status_code = 200
    except:
        message = "Inspection is not started"
        status_code = 403

    return message,status_code


def save_inspection_details_util(data):
    inspection_id = data.get('current_inspection_id',None)
    part_name = CacheHelper().get_json("part_name")
    if inspection_id is None:
        return "inspection is none",400

    status = data.get('status',None)
    defect_list = data.get('defect_list',[])  
    inference_frame = data.get('all_inference_frames_url',None)
    input_frame = data.get('all_input_frames_url',None)
    feature_list = data.get('feature_list',[])
    features = data.get('features',[])
    defects = data.get('defects',[])
    feature_dict = data.get('feature_dict',{})
    

    inspection_details = {
        "inspection_id":inspection_id,
        "input_frame": input_frame,
        "defect_list":defect_list,
        "inference_frame":inference_frame,
        "status":status,
        "reject_reason":{"features":features, "defects":defects},
        "feature_list": feature_list,
        "part_name":part_name,
        "created_at" : datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "feature_dict":feature_dict
    }
    print(inspection_details)

    try:
        mp = MongoHelper().getCollection(str(inspection_id)+"_log")


        # ins = [i for i in mp.find().sort([( '$natural', -1)]).limit(1)][0]
        # print('********************************')

        # mp.update_one({'_id':ObjectId(ins["_id"])},{'$set':inspection_details})
        mp.insert_one(inspection_details)
        print('********************************11')



        return "success",200
    except Exception as e:
        print(e)

        return "Object not available", 400


def end_process_util(data):
    """
        Usage:  Ending  the inspection process by updating the status as completed, with the end time
        Request Parameters: {
                    "inspection_id":"61d4257708f3e625aa6b3b26"
                    }
        Request Method: POST
        Response: {
                    "part_id": "61d4257708f3e625aa6b3b26"
                    "workstation_id": "6392257708f3e625aa6b3b26",
                    "plan_id":plan_id,
                    "start_time": "10:00:00",
                    "end_time":"11:00:00",
                    "shift_id":shift_id,
                    "operator_id":operator_id,
                    "produced_on":current_date,
                    "status":"completed",
                    "inference_urls" : ["url1","url2"]
                    }

        """
    inspection_id = data.get('inspection_id',None)
    if inspection_id is None:
        return "Inspection ID not found", 400

    part_name =CacheHelper().get_json("part_name")
    if part_name is None:
        return "Part name not found", 400
    mp = MongoHelper().getCollection('current_inspection')
    doc = mp.find_one()

    if doc:
        inspection_id = doc["current_inspection_id"]
    endedAt = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    colle = {
    "status" : "completed",
    "end_time" : endedAt
    }
    from automate.settings import INSPECTION_COLLECTION
    mp = MongoHelper().getCollection(INSPECTION_COLLECTION)
    dataset = mp.find_one({'_id' : ObjectId(inspection_id)})

    mp.update({'_id' : ObjectId(dataset['_id'])}, {'$set' :  colle})

    bb = MongoHelper().getCollection('current_inspection')
    ps = bb.find_one()
    if ps is None:
        bb.insert_one({'current_inspection_id': None})
    else:
        ps['current_inspection_id'] = None
        bb.update({"_id": ps['_id']}, {"$set": ps})
    
    mpc = MongoHelper().getCollection('model_check')
    mp_data = mpc.find_one({'selected_model':part_name})
    newvalues = { "$set": { "selected_model": None,"current_running_model": None } }
    mp.update_one({'_id':mp_data['_id']}, newvalues)

    
    return {"message":"process completed"},200


def get_camera_feed_urls():
    """
        Usage: Get the list of urls for all workstations with which we are viewing the live camera feed for the given
                workstation via a browser or the LIVIS web app
        Request Parameters: {
                    }
        Request Method: GET
        Response: {
                       "data": {
                               ["url1_camera1","url2_camera2"]
                           }
                    }
    """
    rch = CacheHelper()
    while True:
        frame1 = rch.get_json("frame")
        # frame1= cv2.imread("/home/lincode/Documents/seneca/backend/image/bom2022_02_16_21_53_50.jpg")
        ret, jpeg = cv2.imencode('.jpg', frame1)
        frame =  jpeg.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def get_all_parts_util():
    mp = MongoHelper().getCollection('parts')
    mp_data = mp.find({"is_deleted":False})
    parts_data = []
    for i in mp_data:
        parts_data.append(i['part_name'])
    
    return parts_data,200



def get_mega_report_util(data):
    '''
    {
    "from_date":"",
    "to_date":"",
    "operator_id":"",
    "status":"",
    "shift_id":"",
    "skip":0,
    "limit":10,
    "workstation_id":""
}
    '''

    try:
        from_date = data.get('from_date')
        to_date = data.get('to_date')
        operator_id = data.get('operator_id',None)
        status = data.get('status',None) #pass / fail
        shift_id = data.get('shift_id',None)
        skip = data.get('skip',None)
        limit = data.get('limit',None)
        workstation_id = data.get('workstation_id',None)

        query = []

        if workstation_id:
            query.append({'workstation_id': workstation_id})
        if operator_id:
            query.append({'operator_id': operator_id })
        if shift_id:
            query.append({'shift_id': shift_id })
        if from_date:
            query.append({'start_time': {"$gte":from_date}})#,"$lte":to_date
        if to_date:
            query.append({'end_time': {"$lte":to_date}})
        # if status:
        #     query.append({'status': status})

        # print(query)
        from automate.settings import INSPECTION_COLLECTION
        if bool(query):
            inspectionid_collection = MongoHelper().getCollection(INSPECTION_COLLECTION)
            objs = [i for i in inspectionid_collection.find({"$and":query}).sort([( '$natural', -1)]) ]
        else:
            inspectionid_collection = MongoHelper().getCollection(INSPECTION_COLLECTION)
            objs = [i for i in inspectionid_collection.find().sort([( '$natural', -1)])]
        print(objs)
        p = []
        for ins in objs:
            inspection_id = str(ins['_id'])
            log_coll = MongoHelper().getCollection(str(inspection_id)+"_log")
            if status == "Accepted" or status == "Rejected":
                pr = [i for i in log_coll.find({'status':status}).sort([( 'created_at', -1)])]
            else:
                pr = [i for i in log_coll.find().sort([( 'created_at', -1)])]
            p.extend(pr) 
        q = []
        if skip is not None and limit is not None:
            for items in p[skip:skip+limit]:
                q.append(items)
        else:
            q = p.copy()
        coll={
            "data":q,
            "total":len(p)
        }
        # print("length is :::: ",len(q))
        return coll,200
    except Exception as e:
        print(e)
        return "nodata",400
    

def set_confidence_util(data):
    common_conf = float(data.get("common_conf",None))
    part_name = data.get('part_name',None)
    mp = MongoHelper().getCollection('parts')
    mp_data = mp.find_one({"part_name":part_name})

    newvalues = { "$set": { "kanban.common_confidence":common_conf } }
    mp.update_one({'_id':mp_data['_id']}, newvalues)

    return mp_data,200


