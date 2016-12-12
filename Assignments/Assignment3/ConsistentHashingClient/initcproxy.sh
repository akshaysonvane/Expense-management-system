docker build -t cproxy .
docker run --net mynetwork --ip 172.18.0.10 --name cproxy cproxy
