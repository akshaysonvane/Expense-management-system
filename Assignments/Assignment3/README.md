#Assignment 3

->Run 'initall.sh' script.
->URL: http://172.18.0.10:9000

*Three Flask expense management instances are:
-http://172.18.0.5:3000
-http://172.18.0.6:3000
-http://172.18.0.7:3000

*Three MySql db instances are:
-http://172.18.0.2:3306
-http://172.18.0.3:3306
-http://172.18.0.4:3306


*POST:
172.18.0.1 - - [12/Dec/2016 05:47:32] "POST /v1/expenses HTTP/1.1" 201 - http://172.18.0.7:3000/v1/expenses
172.18.0.1 - - [12/Dec/2016 05:47:39] "POST /v1/expenses HTTP/1.1" 201 - http://172.18.0.5:3000/v1/expenses
172.18.0.1 - - [12/Dec/2016 05:47:45] "POST /v1/expenses HTTP/1.1" 201 - http://172.18.0.5:3000/v1/expenses
172.18.0.1 - - [12/Dec/2016 05:47:52] "POST /v1/expenses HTTP/1.1" 201 - http://172.18.0.7:3000/v1/expenses
172.18.0.1 - - [12/Dec/2016 05:47:56] "POST /v1/expenses HTTP/1.1" 201 - http://172.18.0.6:3000/v1/expenses
172.18.0.1 - - [12/Dec/2016 05:48:02] "POST /v1/expenses HTTP/1.1" 201 - http://172.18.0.5:3000/v1/expenses
172.18.0.1 - - [12/Dec/2016 05:48:07] "POST /v1/expenses HTTP/1.1" 201 - http://172.18.0.5:3000/v1/expenses
172.18.0.1 - - [12/Dec/2016 05:48:13] "POST /v1/expenses HTTP/1.1" 201 - http://172.18.0.6:3000/v1/expenses
172.18.0.1 - - [12/Dec/2016 05:48:18] "POST /v1/expenses HTTP/1.1" 201 - http://172.18.0.5:3000/v1/expenses
172.18.0.1 - - [12/Dec/2016 05:48:25] "POST /v1/expenses HTTP/1.1" 201 - http://172.18.0.5:3000/v1/expenses


*GET:
172.18.0.1 - - [12/Dec/2016 05:49:11] "GET /v1/expenses/1 HTTP/1.1" 200 - http://172.18.0.7:3000/v1/expenses/1
172.18.0.1 - - [12/Dec/2016 05:49:19] "GET /v1/expenses/2 HTTP/1.1" 200 - http://172.18.0.5:3000/v1/expenses/2
172.18.0.1 - - [12/Dec/2016 05:49:23] "GET /v1/expenses/3 HTTP/1.1" 200 - http://172.18.0.5:3000/v1/expenses/3
172.18.0.1 - - [12/Dec/2016 05:49:26] "GET /v1/expenses/4 HTTP/1.1" 200 - http://172.18.0.7:3000/v1/expenses/4
172.18.0.1 - - [12/Dec/2016 05:49:29] "GET /v1/expenses/5 HTTP/1.1" 200 - http://172.18.0.6:3000/v1/expenses/5
172.18.0.1 - - [12/Dec/2016 05:49:33] "GET /v1/expenses/6 HTTP/1.1" 200 - http://172.18.0.5:3000/v1/expenses/6
172.18.0.1 - - [12/Dec/2016 05:49:36] "GET /v1/expenses/7 HTTP/1.1" 200 - http://172.18.0.5:3000/v1/expenses/7
172.18.0.1 - - [12/Dec/2016 05:49:39] "GET /v1/expenses/8 HTTP/1.1" 200 - http://172.18.0.6:3000/v1/expenses/8
172.18.0.1 - - [12/Dec/2016 05:49:43] "GET /v1/expenses/9 HTTP/1.1" 200 - http://172.18.0.5:3000/v1/expenses/9
172.18.0.1 - - [12/Dec/2016 05:49:47] "GET /v1/expenses/10 HTTP/1.1" 200 - http://172.18.0.5:3000/v1/expenses/10

