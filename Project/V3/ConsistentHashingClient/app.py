from ConsistentHashRing import ConsistentHashRing
from flask import Flask, request, jsonify
import requests, json

app = Flask(__name__)

hash_ring = ConsistentHashRing()


@app.route('/v1/expenses', methods=['POST'])
def expenses_post():
    content = request.get_json(force=True)
    url = "http://" + str(hash_ring[content['id']]) + "/v1/expenses"
    # print "id: " + content['id'] + "   url: " + url
    req = requests.post(url, data=json.dumps(content))

    return req.url, req.status_code


@app.route('/v1/expenses/<int:_id>', methods=['GET'])
def expenses_get(_id):
    url = "http://" + str(hash_ring[str(_id)]) + "/v1/expenses/" + str(_id)
    req = requests.get(url)

    return req.url, req.status_code


if __name__ == '__main__':
    server_info = ["172.18.0.5:3000", "172.18.0.6:3000", "172.18.0.7:3000"]

    for server in server_info:
        hash_ring[server] = server

    app.run(debug=True, host='0.0.0.0', port=9000)
