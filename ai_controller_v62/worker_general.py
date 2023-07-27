
from common_utils import *
import cv2
from inference import *
from ai_settings import *
import bson
import requests

mp = MongoHelper().getCollection('model_check')
mp_data = mp.find_one()
newvalues = { "$set": { "selected_model": None,"current_running_model": None } }
mp.update_one({'_id':mp_data['_id']}, newvalues)

## set current inspection id None
mpi = MongoHelper().getCollection("current_inspection")
mpi_data = mpi.find_one()
mpi_data["current_inspection_id"] = None
mpi.update_one({'_id':mpi_data['_id']}, {"$set":mpi_data})




def check_kanban(detector_predictions,defects,features,features_count):
    defect_list = []
    feature_list = []
    for defect in defects:
        if defect in detector_predictions:
            defect_list.append(defect)

    for feature in features:
        if not feature in detector_predictions:
            feature_list.append(feature)

    #features is from code and it is in list format 
    #detector predictions is from model and it is in list format 
    is_count_match = True
    feature_dict = {}
    detected_count = 0 
    actual_count = 0

    #random_list = ['A', 'A', 'B', 'C', 'B', 'D', 'D', 'A', 'B']
    frequency = {}
    
    # iterating over the list
    for item in detector_predictions:
       # checking the element in dictionary
       if item in frequency:
          # incrementing the counr
          frequency[item] += 1
       else:
          # initializing the count
          frequency[item] = 1
    
    # printing the frequency
    print(frequency) #{'A': 3, 'B': 3, 'C': 1, 'D': 2}
    '''
    for j in detector_predictions:
        if j in features:
            
            for k in features_count:
                for key,val in k.items():
                    if key == j:
                        detected_count = detected_count + 1

            #check for count 
            for k in features_count:
                for key,val in k.items():
                    if key == j:
                        actual_count = val
                        break
            
            dct = {j:[{"actual":actual_count,"pred":detected_count}]}
            feature_dict.update(dct)
            # {"bolt":[{"actual":5,"pred":7}] }

    if actual_count != detected_count:
        is_count_match = False

    '''

    for i in features_count:
        for key,value in i.items():
            if key in frequency.keys():
                if value == frequency[key]:
                    dct = {key:[{"actual":value,"pred":value}]}
                    feature_dict.update(dct)
                else:
                    dct = {key:[{"actual":value,"pred":frequency[key]}]}
                    feature_dict.update(dct)
                    is_count_match = False
            #else: 
            #    is_count_match = False



    if bool(defect_list)  or bool(feature_list):
        status = 'Rejected'
    else:
        #check another condition 
        if is_count_match is False:
            status = 'Rejected'
        else:
            status = 'Accepted'


    return status, defect_list,feature_list,feature_dict
    


#cap = cv2.VideoCapture(0)

print("before while loop ------------------------")
while True:

   
    mp_ins = MongoHelper().getCollection("current_inspection")
    data = mp_ins.find_one()

    current_inspection_id = data.get('current_inspection_id')
    print(current_inspection_id)
    
    mp_parts = MongoHelper().getCollection('parts')

        
    mp = MongoHelper().getCollection('model_check')
    mp_data = mp.find_one()
    print(mp_data)
    current_running_model = mp_data.get('current_running_model')
    # print("current_model",current_running_model)
    selected_model = mp_data.get('selected_model')
    # print("selectted model",selected_model)
    
    print(torch.cuda.is_available(),' <<<<<<<<<<<<< cuda ')

    if current_inspection_id is None:
        continue

    if current_running_model is None and selected_model is None:
        continue

    if selected_model is None and current_running_model is not None:
        continue

    if current_running_model is None and selected_model is not None:
        parts_data = mp_parts.find_one({'is_deleted':False,'part_name':selected_model})

        predictor = Predictor()
        predictor.model_dir = './'
        predictor.weights_path = parts_data['kanban']['weights_path']
        predictor.image_size = parts_data['kanban']['image_size']
        predictor.common_confidence = parts_data['kanban']['common_confidence']
        predictor.features = parts_data['kanban']['features']
        # predictor.features_count = parts_data['kanban']['features_count']
        predictor.defects = parts_data['kanban']['defects']
        predictor.ind_thresh = parts_data['kanban']['ind_thresh']


        predictor_model = torch.hub.load(predictor.model_dir,'custom',path=parts_data['kanban']['weights_path'],source = 'local',force_reload=True)
        predictor_model.conf = parts_data['kanban']['common_confidence']
 
        newvalues = { "$set": { "selected_model": selected_model,"current_running_model": selected_model } }

        mp.update_one({'_id':mp_data['_id']}, newvalues)
         
    if selected_model is not None and current_running_model is not None:
        if selected_model != current_running_model:

            parts_data = mp_parts.find_one({'is_deleted':False,'part_name':selected_model})
            predictor = Predictor()
            predictor.model_dir = './'
            predictor.weights_path = parts_data['kanban']['weights_path']
            predictor.image_size = parts_data['kanban']['image_size']
            predictor.common_confidence = parts_data['kanban']['common_confidence']
            predictor.features = parts_data['kanban']['features']
            # predictor.features_count = parts_data['kanban']['features_count']
            predictor.defects = parts_data['kanban']['defects']
            predictor.ind_thresh = parts_data['kanban']['ind_thresh']
            # predictor_model = predictor.load_model()

            predictor_model = torch.hub.load(predictor.model_dir,'custom',path=parts_data['kanban']['weights_path'],source = 'local',force_reload=True)
            predictor_model.conf = parts_data['kanban']['common_confidence']


        
            newvalues = { "$set": { "selected_model": selected_model,"current_running_model": selected_model } }

            mp.update_one({'_id':mp_data['_id']}, newvalues)



    ui_trigger = CacheHelper().get_json('inspection_trigger')
    #ret, frame = cap.read()
    #input_frame = frame.copy()
    input_frame = CacheHelper().get_json('input_frame')
    input_frame_copy = input_frame.copy()
    # input_frame = cv2.imread("D:\\lincode\\europe\\fiasa\\images\\images\\crack_2_re\\crack_batch_2_97.jpg")
    #CacheHelper().set_json({'frame':input_frame})
    
    if current_running_model and ui_trigger:
        parts_data = mp_parts.find_one({'is_deleted':False,'part_name':selected_model})
        predictor_model.conf = parts_data['kanban']['common_confidence']
        predicted_frame, detector_predictions,coordinates  = predictor.run_inference_hub(predictor_model,input_frame)
        print("--------predictions------------",detector_predictions)

        defects = predictor.defects
        features = predictor.features
        features_count = predictor.features_count
        status, defect_list,feature_list,feature_dict = check_kanban(detector_predictions, defects,features,features_count)
        print("feature_dict issssssssssssssssssss ",feature_dict)
        object_id = str(bson.ObjectId())

        cv2.imwrite(os.path.join(datadrive_path,object_id+'_if.jpg'),input_frame_copy)
        cv2.imwrite(os.path.join(datadrive_path,object_id+'_pf.jpg'),predicted_frame)

        input_frame_url = "http://"+my_ip_address+":3306/"+object_id+"_if.jpg"
        predicted_frame_url = "http://"+my_ip_address+":3306/"+object_id+"_pf.jpg"


        data = {'current_inspection_id':str(current_inspection_id),'all_input_frames_url':[input_frame_url],'all_inference_frames_url':[predicted_frame_url],'status':status,'defect_list':defects,'feature_list':features,'features':feature_list,'defects':defect_list,'feature_dict':feature_dict}

        print(data)

        requests.post(url = 'http://192.168.1.9:8000/livis/operators/save_inspection_details/', json = data)
        CacheHelper().set_json({'inspection_trigger':False})
    elif current_running_model:
        predicted_frame, detector_predictions,coordinates  = predictor.run_inference_hub(predictor_model,input_frame)
        print("current_running_model==>",current_running_model)
        CacheHelper().set_json({'frame':predicted_frame})


        


 