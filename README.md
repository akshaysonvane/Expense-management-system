# RESTful Dockerized Expense management system

![Architecture](/Documents/Architecture.png?raw=true "Architecture")

## Features
-	Developed a simple expense management system that provides RESTful endpoints for CRUD operations using python flask.
-	Achieved fault tolerance by implementing active replication of docker instances which increases availability.
-	Implemented round robin load balancing for traffic distribution which eliminates overloading of a single replica instance.
-	Implemented Redis routing table which routes requests to available replica instances and maintains it for upcoming requests.
-	Achieved quick failure detection by implementing circuit breaker, preventing routing requests to failed replica instances.
-	Implemented sharding using consistent hashing (configurable to use HRW/Rendezvous hashing) which improves scalability. 
