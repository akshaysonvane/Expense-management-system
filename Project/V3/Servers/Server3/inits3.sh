docker build -t server3 .
docker run --net mynetwork --ip 172.18.0.7 --name s3 -d server3
