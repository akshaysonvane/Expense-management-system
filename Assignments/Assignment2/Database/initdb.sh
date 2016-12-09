docker run --net mynetwork --ip 172.18.0.2 --name mysqldb -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:latest
docker run --net mynetwork --ip 172.18.0.3 --name predis -d redis
