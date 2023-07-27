# # build step
# FROM node:14.21-slim as build
# WORKDIR /home/frontend
# COPY . .
# COPY package.json ./
# RUN npm install
# RUN npm run build
# EXPOSE 4200
# # release step
# FROM nginx:1.21.5-alpine as release

# CMD ["ng","serve","--host","0.0.0.0","--port","4200"]


FROM node:14-alpine

WORKDIR /home/frontend

RUN npm install -g @angular/cli@latest

COPY package*.json ./
COPY . .

RUN npm install
EXPOSE 4200
COPY . .

CMD ["ng", "serve", "--host", "0.0.0.0", "--port", "4200"]
