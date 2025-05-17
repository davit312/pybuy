#!/bin/bash

if [[ "$1" == "clean" ]]; then
    echo "Cleaning up..."
    docker rm -f shop-db
    sudo rm -rf $PWD/mysql
    exit 0
fi

if [[ -d "$PWD/mysql" ]]; then
    echo "Directory $PWD/mysql already exists. Please remove it before running this script."
    echo "Starting the existing container shop-db."
    docker start shop-db
    exit 1
else
    echo "Directory $PWD/mysql does not exist. Creating it now."
    mkdir $PWD/mysql

    docker rm -f shop-db
    docker run --name shop-db -d \
        -e MYSQL_ROOT_PASSWORD=root \
        -e MYSQL_DATABASE=shop \
        -e MYSQL_USER=shop \
        -e MYSQL_PASSWORD=shop \
        -p 3306:3306 \
        -v $PWD/mysql:/var/lib/mysql \
        mysql:8.0.42-oracle
fi

# To connect to the MySQL server, use the following command:
# mysql -hlocalhost -ushop -pshop -Dshop
