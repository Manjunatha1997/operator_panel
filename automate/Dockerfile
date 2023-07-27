FROM python:3.8.16-slim-buster
WORKDIR /home/backend
RUN apt update -y 
RUN apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000
CMD [ "python","manage.py","runserver","0.0.0.0:8000" ]



