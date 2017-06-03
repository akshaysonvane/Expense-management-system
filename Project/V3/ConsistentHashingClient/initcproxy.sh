docker build -t cproxy .
docker run --net mynetwork --ip 172.18.0.10 -d --name cproxy cproxy
