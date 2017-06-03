#!/usr/bin/python
"""
Sample usage:
chmod +x assignment1_check.py
./assignment1_check.py -sid <student_id> -an assignment1 -u <ur_encoded> -fn <first name use \ if there is a space>
-ln <last name> -e <email_id>
./assignment1_check.py -sid 010095345 -an assignment1 -u http:\/\/localhost:5000 -fn Nagkumar -ln Arkalgud
-e nagkumar.arkalgud@sjsu.edu
"""
import json
import sys
import argparse
import datetime
import uuid
import requests
import unittest

parser = argparse.ArgumentParser(description='Arguments for the automated assignment corrector')
parser.add_argument('-sid', '--student_id', help='Student ID that you use to login to canvas.', required=True)
parser.add_argument('-an', '--assignment_name', help='Assignment name. Please use assignment1 here.', required=True)
parser.add_argument('-u', '--url', help='Base URL where your code works (no slash in the end)', required=True)
parser.add_argument('-fn', '--first_name', help='First name according to canvas', required=True)
parser.add_argument('-ln', '--last_name', help='Last name according to canvas', required=True)
parser.add_argument('-e', '--email_id', help='Email ID according to canvas', required=True)
args = parser.parse_args()

student_id = args.student_id
if len(student_id) != 9:
    print "Student ID is not valid."
    exit(1)
assignment_name = args.assignment_name
if assignment_name != 'assignment1':
    print "Assignment Name is not valid."
    exit(1)
url = args.url
first_name = args.first_name
last_name = args.last_name
email_id = args.email_id

object_to_post = {
    "name": "Foo Bar",
    "email": "foo@bar.com",
    "category": "travel",
    "description": "iPad for office use",
    "link": "http://www.apple.com/shop/buy-ipad/ipad-pro",
    "estimated_costs": "700",
    "submit_date": "09-08-2016"
}

points = {
    'post_returns_201': 2,
    'get_returns_200': 1,
    'get_returns_all_keys_and_values': 2,
    'get_returns_404_if_no_object_exists': 1,
    'put_returns_202': 1,
    'put_changes_values_appropriately': 1,
    'delete_returns_204': 1,
    'get_after_delete_returns_404': 1
}

timestamp = str(datetime.datetime.now())
user_log = {
    'uuid': str(uuid.uuid4()),
    'student_id': student_id,
    'first_name': first_name,
    'last_name': last_name,
    'email_id': email_id,
    'timestamp': timestamp,
    'post_returns_201': 0,  # 2
    'get_returns_200': 0,  # 1
    'get_returns_all_keys_and_values': 0,  # 2
    'get_returns_404_if_no_object_exists': 0,  # 1
    'put_returns_202': 0,  # 1
    'put_changes_values_appropriately': 0,  # 1
    'delete_returns_204': 0,  # 1
    'get_after_delete_returns_404': 0  # 1
}


def submit_to_lambda():
    total_points = user_log['post_returns_201'] + user_log['get_returns_200'] + user_log[
        'get_returns_all_keys_and_values'] + user_log['get_returns_404_if_no_object_exists'] + user_log[
                       'put_returns_202'] + user_log['put_changes_values_appropriately'] + user_log[
                       'delete_returns_204'] + user_log['get_after_delete_returns_404']
    user_log['total_points'] = total_points
    import hashlib
    user_log['hash'] = hashlib.md5(open('assignment1_check.py', 'rb').read()).hexdigest()
    print "Ending the test script. Grade: %s/10" % total_points
    data_to_send = {
        "Item": user_log,
        "TableName": assignment_name
    }
    r = requests.post('https://ytxt3nsddb.execute-api.us-west-2.amazonaws.com/working', json.dumps(data_to_send))
    if r.status_code != 200:
        print "Something went wrong with the log. Please include the below line in the email to the TA"
        print "Status code for log %s" % r.status_code
        print r.content
    else:
        return


# checking post
# POST should be working on /v1/expenses
post_url = "%s/v1/expenses" % args.url
post_response = requests.post(post_url, json.dumps(object_to_post))
if post_response.status_code != 201:
    print "Response Status code for post is not 201"
    user_log['post_returns_201'] = 0
else:
    user_log['post_returns_201'] = points['post_returns_201']
    user_log['post_response'] = json.loads(post_response.content)
json_response = json.loads(post_response.content)
id_for_object = None
invalid_id = None
try:
    id_for_object = json_response['id']
    invalid_id = id_for_object + 339
except KeyError:
    print "Id not returned on POST."
    exit(0)
except TypeError:
    invalid_id = id_for_object + str(339)
for key in object_to_post.keys():
    if key not in json_response.keys():
        print "Key %s not found in response " % key
        user_log['post_returns_201'] = 0
        submit_to_lambda()
        exit(1)

# checking GET on /v1/expenses/{id}
get_url = "%s/v1/expenses/%s" % (args.url, id_for_object)
get_response = requests.get(get_url)
json_response = json.loads(get_response.content)
if get_response.status_code == 200:
    user_log['get_returns_200'] = points['get_returns_200']
    for key in object_to_post.keys():
        if key not in json_response.keys():
            print "Key %s not found in response " % key
            user_log['get_returns_all_keys_and_values'] = 0
            submit_to_lambda()
            exit(1)
    user_log['get_returns_all_keys_and_values'] = points['get_returns_all_keys_and_values']
    user_log['get_response'] = json_response
else:
    user_log['get_returns_200'] = 0
    print "Get did not return 200 as expected."
    submit_to_lambda()
    exit(1)

# checking get for invalid id
invalid_get_url = "%s/v1/expenses/%s" % (args.url, invalid_id)
get_response = requests.get(invalid_get_url)
if get_response.status_code != 404:
    user_log['get_returns_404_if_no_object_exists'] = 0
    print "Response expected was 404."
    submit_to_lambda()
    exit(1)
else:
    user_log['get_returns_404_if_no_object_exists'] = points['get_returns_404_if_no_object_exists']

# checking for put on /v1/expenses/{id}
put_url = "%s/v1/expenses/%s" % (args.url, id_for_object)
put_response = requests.put(put_url, json.dumps({"estimated_costs": "800"}))
if put_response.status_code == 202:
    user_log['put_returns_202'] = 1
else:
    user_log['put_returns_202'] = 0
    submit_to_lambda()
    exit(1)


# checking if values have changed after PUT
get_response = requests.get(get_url)
if get_response.status_code == 200:
    json_response = json.loads(get_response.content)
    if json_response['estimated_costs'] == '800':
        user_log['put_changes_values_appropriately'] = points['put_changes_values_appropriately']
    else:
        user_log['put_changes_values_appropriately'] = 0
        print "PUT has not changed the value."
        submit_to_lambda()
        exit(1)
else:
    print "Get after PUT did not respond with 200"
    user_log['put_changes_values_appropriately'] = 0
    submit_to_lambda()
    exit(1)


# checking for delete at /v1/expenses/{id}
delete_url = "%s/v1/expenses/%s" % (args.url, id_for_object)
delete_response = requests.delete(delete_url)
if delete_response.status_code == 204:
    user_log['delete_returns_204'] = points['delete_returns_204']
else:
    user_log['delete_returns_204'] = 0
    submit_to_lambda()
    exit(1)


# checking if object still exists
get_response = requests.get(get_url)
if get_response.status_code == 404:
    user_log['get_after_delete_returns_404'] = points['get_after_delete_returns_404']
    print "Test successful"
    submit_to_lambda()
    exit(1)
else:
    user_log['get_after_delete_returns_404'] = 0
    submit_to_lambda()
    exit(1)
