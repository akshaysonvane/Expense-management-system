docker build -t server2 .
docker run --net mynetwork --ip 172.18.0.5 --name s2 -d server2
