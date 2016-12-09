docker build -t proxyserver .
docker run -it --net mynetwork --ip 172.18.0.10 --name proxy proxyserver
