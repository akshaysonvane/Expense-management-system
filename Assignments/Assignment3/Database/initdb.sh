docker run --net mynetwork --ip 172.18.0.2 --name mysqldb1 -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:latest
docker run --net mynetwork --ip 172.18.0.3 --name mysqldb2 -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:latest
docker run --net mynetwork --ip 172.18.0.4 --name mysqldb3 -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:latest
