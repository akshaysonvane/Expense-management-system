import requests
import json
# import logging
# logging.basicConfig(level=logging.DEBUG)
from datetime import *
from collections import OrderedDict
from operator import itemgetter
from spyne import Application, srpc, ServiceBase, Unicode
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication


class SpotCrime(ServiceBase):
    @srpc(Unicode, Unicode, Unicode, _returns=Unicode)
    def checkcrime(lat, lon, radius):
        get_url = "https://api.spotcrime.com/crimes.json?lat=%s&lon=%s&radius=%s&key=." % (lat, lon, radius)
        get_response = requests.get(get_url)
        json_response = json.loads(get_response.content)

        response = {}
        crime_type = {}
        street_name = {}
        event_time = {
            "12:01am-3am": 0,
            "3:01am-6am": 0,
            "6:01am-9am": 0,
            "9:01am-12noon": 0,
            "12:01pm-3pm": 0,
            "3:01pm-6pm": 0,
            "6:01pm-9pm": 0,
            "9:01pm-12midnight": 0
        }

        for i in json_response['crimes']:
            # most_dangerous_streets
            # case : &
            if "&" in i['address']:
                string = i['address'].split(" & ")
                if not street_name.has_key(string[0]):
                    street_name[string[0]] = 1
                else:
                    street_name[string[0]] = street_name[string[0]] + 1

                if not street_name.has_key(string[1]):
                    street_name[string[1]] = 1
                else:
                    street_name[string[1]] = street_name[string[1]] + 1
            # case : BLOCK OF
            elif "BLOCK OF" in i['address']:
                string = i['address'].split(" BLOCK OF ")

                if not street_name.has_key(string[1]):
                    street_name[string[1]] = 1
                else:
                    street_name[string[1]] = street_name[string[1]] + 1
            # case : BLOCK BLOCK
            elif "BLOCK BLOCK" in i['address']:
                string = i['address'].split(" BLOCK BLOCK ")

                if not street_name.has_key(string[1]):
                    street_name[string[1]] = 1
                else:
                    street_name[string[1]] = street_name[string[1]] + 1
            else:
                # case : BLOCK
                if i['address'].count('BLOCK') is 1:
                    string = i['address'].split(" BLOCK ")

                    if not street_name.has_key(string[1]):
                        street_name[string[1]] = 1
                    else:
                        street_name[string[1]] = street_name[string[1]] + 1
                else:
                    # case : direct street name
                    if not street_name.has_key(i['address']):
                        street_name[i['address']] = 1
                    else:
                        street_name[i['address']] = street_name[i['address']] + 1

            # crime_type_count
            if not crime_type.has_key(i['type']):
                crime_type[i['type']] = 1
            else:
                crime_type[i['type']] = crime_type[i['type']] + 1

            # event_time_count
            # extract last 8 characters from string : "10/06/16 12:27 AM"
            stime = str(i['date'])[-8:]
            # convert formatted string to time for comparison
            time = datetime.strptime(stime, '%I:%M %p')
            # time comparisons
            if datetime.strptime('12:01 AM', '%I:%M %p') <= time <= datetime.strptime('03:00 AM', '%I:%M %p'):
                event_time['12:01am-3am'] = event_time['12:01am-3am'] + 1
            elif datetime.strptime('03:01 AM', '%I:%M %p') <= time <= datetime.strptime('06:00 AM', '%I:%M %p'):
                event_time['3:01am-6am'] = event_time['3:01am-6am'] + 1
            elif datetime.strptime('06:01 AM', '%I:%M %p') <= time <= datetime.strptime('09:00 AM', '%I:%M %p'):
                event_time['6:01am-9am'] = event_time['6:01am-9am'] + 1
            elif datetime.strptime('09:01 AM', '%I:%M %p') <= time <= datetime.strptime('12:00 PM', '%I:%M %p'):
                event_time['9:01am-12noon'] = event_time['9:01am-12noon'] + 1
            elif datetime.strptime('12:01 PM', '%I:%M %p') <= time <= datetime.strptime('03:00 PM', '%I:%M %p'):
                event_time['12:01pm-3pm'] = event_time['12:01pm-3pm'] + 1
            elif datetime.strptime('03:01 PM', '%I:%M %p') <= time <= datetime.strptime('06:00 PM', '%I:%M %p'):
                event_time['3:01pm-6pm'] = event_time['3:01pm-6pm'] + 1
            elif datetime.strptime('06:01 PM', '%I:%M %p') <= time <= datetime.strptime('09:00 PM', '%I:%M %p'):
                event_time['6:01pm-9pm'] = event_time['6:01pm-9pm'] + 1
            else:
                event_time['9:01pm-12midnight'] = event_time['9:01pm-12midnight'] + 1

        # sort dictionary
        street_name = OrderedDict(sorted(street_name.items(), key=itemgetter(1), reverse=True))

        response['total_crime'] = len(json_response['crimes'])
        response['the_most_dangerous_streets'] = list(street_name)[:3]
        response['crime_type_count'] = crime_type
        response['event_time_count'] = event_time

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
