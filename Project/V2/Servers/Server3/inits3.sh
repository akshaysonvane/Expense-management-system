docker build -t server3 .
docker run --net mynetwork --ip 172.18.0.6 --name s3 -d server3
