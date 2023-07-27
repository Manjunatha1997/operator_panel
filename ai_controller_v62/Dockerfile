FROM ultralytics/yolov5:v6.2
WORKDIR /home/ai_controller_v62
RUN mkdir datadrive
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# RUN pip uninstall bson -y
# RUN pip uninstall pymongo -y
# RUN pip install pymongo
RUN pip uninstall -y bson pymongo \
&& pip install bson==0.5.7 \
&& pip install pymongo==3.7.2
COPY . .
CMD ["python","worker_general.py"]

