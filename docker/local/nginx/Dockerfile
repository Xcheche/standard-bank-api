FROM docker.io/nginx:1.27.0-alpine3.19-slim


# Remove the default nginx configuration file
RUN  rm -rf /etc/nginx/conf.d/default.conf

# Copy the custom nginx configuration file to the container
COPY ./nginx.conf /etc/nginx/conf.d/default.conf