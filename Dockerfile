# Use an official MariaDB image as the base image
FROM mariadb:latest

# Set the root password for MariaDB
ENV MYSQL_ROOT_PASSWORD=password

ENV MYSQL_DATABASE=db \
    MYSQL_USER=admin \
    MYSQL_PASSWORD=password \
    MYSQL_HOST=localhost \
    MYSQL_PORT=3306 \
    ADMIN_PASSWORD=password

# Copy the database initialization script to the container
COPY ./init.sql /docker-entrypoint-initdb.d/

# Copy the script to start MariaDB and the Flask app to the container
COPY start_services.sh /start_services.sh
RUN chmod +x /start_services.sh

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip pkg-config libmysqlclient-dev mysql-client

# Set the working directory for the Flask app
WORKDIR /app

# Copy the Flask app to the container
COPY ./src/ /app/
COPY ./requirements.txt /app

# Install Flask and required dependencies
RUN pip3 install --break-system-packages -r /app/requirements.txt

# Command to start MariaDB and the Flask app
CMD ["/start_services.sh"]
