# Set nginx base image
FROM nginx

# Install the certbot client for Letsencrypt
RUN apt-get update
RUN apt-get install -y python-certbot-nginx
# Install cron for handling Letsencrypt certificate renewal
RUN apt-get install -y cron
# Clean up post-installation files
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*
# The following path must match the Letsencrypt challenge path in your
# Nginx configuration. It is the target for those GET requests.
RUN mkdir /var/letsencrypt

# Copy custom configuration file from the current directory
COPY nginx.conf /etc/nginx/nginx.conf
