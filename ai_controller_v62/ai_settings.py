
#Settings for MongoDB
MONGO_SERVER_HOST = "host.docker.internal"
MONGO_SERVER_HOST_DOCKER = '172.18.0.1'
MONGO_SERVER_PORT = 27017
#MONGO_DB = "LIVIS"
# MONGO_DB = "AUTOMATE-GENERAL"
MONGO_DB = "seneca"

INSPECTION_DATA_COLLECTION = "inspection_summary"
MONGO_COLLECTION_PARTS = "parts"
MONGO_COLLECTIONS = {MONGO_COLLECTION_PARTS: "parts"}
WORKSTATION_COLLECTION = 'workstations'
PARTS_COLLECTION = 'parts'
SHIFT_COLLECTION = 'shift'
# PLAN_COLLECTION = 'plan'


# #Settings for Redis
REDIS_CLIENT_HOST = "host.docker.internal"
REDIS_CLIENT_HOST_DOCKER = '172.18.0.1'
REDIS_CLIENT_PORT = 6379



original_frame_keyholder = "original_frame"
predicted_frame_keyholder = "predicted_frame"


mobile_id = ''
my_ip_address = "localhost"
datadrive_path = '/home/ai_controller_v62/datadrive/'

