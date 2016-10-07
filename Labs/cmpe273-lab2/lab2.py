import requests
import json
from datetime import *
import logging
logging.basicConfig(level=logging.DEBUG)

from spyne import Application, srpc, ServiceBase, Unicode, String
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication

class SpotCrime(ServiceBase):
  @srpc(Unicode, Unicode, Unicode, _returns=String)
  def checkcrime(lat, lon, radius):
    get_url = "https://api.spotcrime.com/crimes.json?lat=%s&lon=%s&radius=%s&key=." % (lat, lon, radius)
    get_response = requests.get(get_url)
    json_response = json.loads(get_response.content)

    crime_type = {}
    event_time = {
        "12:01am-3am" : 0,
        "3:01am-6am" : 0,
        "6:01am-9am" : 0,
        "9:01am-12noon" : 0,
        "12:01pm-3pm" : 0,
        "3:01pm-6pm" : 0,
        "6:01pm-9pm" : 0,
        "9:01pm-12midnight" : 0
    } 
    for i in json_response['crimes']:
      #crime_type_count
      if(not crime_type.has_key(i['type'])):
        crime_type[i['type']] = 1
      else:
        crime_type[i['type']] = crime_type[i['type']] + 1
      
      #event_time_count
      #extract last 8 characters from string : "10/06/16 12:27 AM"
      stime = str(i['date'])[-8:]
      #convert formatted string to time for comparison
      time = datetime.strptime(stime, '%I:%M %p')
      #time comparisons
      if(datetime.strptime('12:01 AM', '%I:%M %p')<= time <=datetime.strptime('03:00 AM', '%I:%M %p')):
        event_time['12:01am-3am'] = event_time['12:01am-3am'] + 1
      elif(datetime.strptime('03:01 AM', '%I:%M %p')<= time <=datetime.strptime('06:00 AM', '%I:%M %p')):
        event_time['3:01am-6am'] = event_time['3:01am-6am'] + 1
      elif(datetime.strptime('06:01 AM', '%I:%M %p')<= time <=datetime.strptime('09:00 AM', '%I:%M %p')):
        event_time['6:01am-9am'] = event_time['6:01am-9am'] + 1
      elif(datetime.strptime('09:01 AM', '%I:%M %p')<= time <=datetime.strptime('12:00 PM', '%I:%M %p')):
        event_time['9:01am-12noon'] = event_time['9:01am-12noon'] + 1
      elif(datetime.strptime('12:01 PM', '%I:%M %p')<= time <=datetime.strptime('03:00 PM', '%I:%M %p')):
        event_time['12:01pm-3pm'] = event_time['12:01pm-3pm'] + 1
      elif(datetime.strptime('03:01 PM', '%I:%M %p')<= time <=datetime.strptime('06:00 PM', '%I:%M %p')):
        event_time['3:01pm-6pm'] = event_time['3:01pm-6pm'] + 1
      elif(datetime.strptime('06:01 PM', '%I:%M %p')<= time <=datetime.strptime('09:00 PM', '%I:%M %p')):
        event_time['6:01pm-9pm'] = event_time['6:01pm-9pm'] + 1
      else:
        event_time['9:01pm-12midnight'] = event_time['9:01pm-12midnight'] + 1

    response = {}
    response['total_crime'] = len(json_response['crimes'])
    response['the_most_dangerous_streets'] = []
    response['event_time_count'] = event_time
    response['crime_type_count'] = crime_type
    yield response

application = Application([SpotCrime],
  tns='spyne.spotcrime.checkcrime',
  in_protocol=HttpRpc(validator='soft'),
  out_protocol=JsonDocument()
)

if __name__ == '__main__':
  from wsgiref.simple_server import make_server
  wsgi_app = WsgiApplication(application)
  server = make_server('0.0.0.0', 8000, wsgi_app)
  server.serve_forever()
