from common_utils import MongoHelper

import pandas as pd 

mpi = MongoHelper().getCollection("inspection")
mpi_data = [i for i in mpi.find()]
print(len(mpi_data),"mpi data length")



def get_log_details(inspection_id):
    qtc_number = None
    type = None
    is_Accepted = None
    drawing_details_type = None # qtype_ntype


    inspection_id_result = str(inspection_id)+"_result"
    mp = MongoHelper().getCollection(inspection_id_result)
    mp_data = mp.find_one()
    if not mp_data:
        return qtc_number, type, is_Accepted, drawing_details_type
    try:
        qtc_number = mp_data["q2c_number"]
    except Exception as e:
        qtc_number = "not found"
    try:
        type = mp_data["type"]
    except Exception as e:
        type = "not found"
    try:
        is_Accepted = mp_data["is_Accepted"]
    except Exception as e:
        is_Accepted = "not found"
    try:
        drawing_details_type = mp_data["drawing_details"][0]["left_table"]["Type"]
        type_check = list(drawing_details_type.values())
        type_check = list(tuple(type_check))
        temp = None
        for i in type_check:
            if i:
                if "Q" in i:
                    temp = "Q_type"
                if "E" in i:
                    temp = "E_type"
        drawing_details_type = temp

    except Exception as e:
        drawing_details = None
    
    return qtc_number, type, is_Accepted, drawing_details_type




inspection_id,date, qtc, type, status,drawing_results = [],[],[],[],[],[]


for doc in mpi_data:
    produced_on = doc["produced_on"]
    produced_on = produced_on.split(" ")[0]
    id = doc["_id"]
    qtc_number, typ, is_Accepted, drawing_details =  get_log_details(id)
    inspection_id.append(id)
    date.append(produced_on)
    qtc.append(qtc_number)
    type.append(typ)
    status.append(is_Accepted)
    drawing_results.append(drawing_details)


data = {
    "inspection_id" : inspection_id,
    "date": date,
    "q2c number": qtc,
    "type":type,
    "status": status,
    "drawing_results":drawing_results
}
  
df = pd.DataFrame(data)
    
df.to_csv("seneca_report.csv")





