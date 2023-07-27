import cv2
import redis
import ai_settings as settings
import pickle






def singleton(cls):
	instances = {}
	def getinstance():
		if cls not in instances:
			instances[cls] = cls()
		return instances[cls]
	return getinstance

@singleton
class CacheHelper():
	def __init__(self):
		# self.redis_cache = redis.StrictRedis(host="164.52.194.78", port="8080", db=0, socket_timeout=1)
		self.redis_cache = redis.StrictRedis("localhost", port=settings.REDIS_CLIENT_PORT, db=0, socket_timeout=60)
		settings.REDIS_CLIENT_HOST
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



# cap = cv2.VideoCapture(r"D:\python_programs\ocr_.avi")
cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    if ret:
        print(frame.shape)
        CacheHelper().set_json({'input_frame':frame})
    else:
        cap = cv2.VideoCapture(0)

