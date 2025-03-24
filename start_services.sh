#!/bin/sh

# Start MariaDB
mariadbd --user=root --skip-grant-tables --skip-networking &

# Check if MariaDB is running
while ! mysqladmin ping -h"localhost"; do
    echo "Waiting for MariaDB to start..."
    sleep 1
done

echo "MariaDB started"

# Initialize MariaDB with /docker-entrypoint-initdb.d/init.sql
mysql -u root < /docker-entrypoint-initdb.d/init.sql
echo "MariaDB initialized"

# Run Flask app
gunicorn -b 0.0.0.0:5000 --timeout 10 -- app:app
