docker build -t server1 .
docker run --net mynetwork --ip 172.18.0.5 --name s1 -d server1
