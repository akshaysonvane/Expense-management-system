import requests
import json
import time

data = {
    "id": "1",
    "name": "Foo 1",
    "email": "foo1@bar.com",
    "category": "office supplies",
    "description": "iPad for office use",
    "link": "http://www.apple.com/shop/buy-ipad/ipad-pro",
    "estimated_costs": "700",
    "submit_date": "12-10-2016"
}

url = "http://172.18.0.10:9000/v1/expenses"


print "\n"
while 1:
    req = requests.get(url + "/" + str(1))
    if req.status_code == 500:
        print "Waiting for docker containers to start and establish db connections...(may take up to a minute)"
        time.sleep(5)
    else:
        print "\nConnection established"
        break

print "\n\nSending POST requests"
for i in range(1, 11):
    data["id"] = str(i)
    data["name"] = "Foo " + str(i)
    data["email"] = "foo" + str(i) + "@bar.com"
    req = requests.post(url, data=json.dumps(data))
    print str(i) + " -> " + req.text, req.status_code
    time.sleep(1)

print "\n\nSending GET requests"
for i in range(1, 11):
    req = requests.get(url + "/" + str(i))
    print str(i) + " -> " + req.text
    time.sleep(1)
