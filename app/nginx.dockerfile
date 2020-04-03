FROM nginx:1.15.12-alpine

# copy project
COPY . /usr/src/app/

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
