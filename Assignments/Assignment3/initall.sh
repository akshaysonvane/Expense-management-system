docker network create --subnet=172.18.0.0/16 mynetwork

cd Database
./initdb.sh

cd ../Servers
cd Server1
./inits1.sh
cd ../Server2
./inits2.sh
cd ../Server3
./inits3.sh

cd ../../ConsistentHashingClient
./initcproxy.sh
