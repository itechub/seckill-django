# production environment
FROM nginx:1.13.9-alpine
RUN rm -rf /etc/nginx/conf.d
COPY ./deployment/nginx/nginx.conf /etc/nginx
EXPOSE 80
VOLUME ["/usr/share/nginx/statics", "/usr/share/nginx/media"]
CMD ["nginx", "-g", "daemon off;"]
