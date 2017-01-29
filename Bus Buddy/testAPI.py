import urllib.request
import json
from datetime import datetime

APP_KEY = "APP_KEY"
APP_ID = "APP_ID"

def diff_times(time1, time2):
    FMT = '%H:%M'
    diff = datetime.strptime(time1, FMT) - datetime.strptime(time2, FMT)

    diff = str(int(str(diff)[2:4]))

    if (diff == "0"):
        return "now"
    
    return diff

def get_stop_name(stop):
    name = stop['name']
    indicator = stop['indicator']

    return str(indicator + " " + name).strip()

def get_time(expected, aimed):
    if (expected == None):
        return "at " + aimed
    else:
        current = str(datetime.now().time())[:5]
        diff = str( diff_times(expected, current))
        if (diff == "now"):
            return diff
        
        return "in " + diff + " mins"

def get_next_bus(stop):
    response = str(urllib.request.urlopen("http://transportapi.com/v3/uk/bus/stop/" + stop['atcocode'] + "/live.json?app_id=" + APP_ID + "&app_key=" + APP_KEY).read())

    response = response[2:]
    response = response[:-1]

    d = json.loads(response)

    ##This makes the dictionary look pretty
    js = json.dumps(d,indent=2)

    stop_name = d['stop_name']
    bearing = d['bearing']
    departures = d['departures']

    indicator = stop['indicator']

    departure_numbers = list(departures.keys())

    to_speak = "The next buses at stop " + indicator + " " + stop_name + " are.\n"

    for key in departure_numbers:
        next_buses = departures[key]

        for bus in next_buses:
            number = bus['line']
            expected = bus['expected_departure_time']
            aimed = bus['aimed_departure_time']
            
            result = "The number " + number + ", due " + get_time(expected, aimed) + ".\n"

            to_speak = to_speak + result

    return to_speak

def get_nearest_stops():
    postcode = "POSTCODE"
    response = str(urllib.request.urlopen("http://api.postcodes.io/postcodes?q=[%22" + postcode.replace(" ","%20") + "%22]").read())

    response = response[2:]
    response = response[:-1]

    d = json.loads(response)

    ##This makes the dictionary look pretty
    js = json.dumps(d,indent=2)

    result = d['result'][0]
    
    lon = str(result['longitude'])
    lat = str(result['latitude'])

    near_response = str(urllib.request.urlopen("http://transportapi.com/v3/uk/bus/stops/near.json?&app_id=" + APP_ID + "&app_key=" + APP_KEY + "&lon=" + lon + "&lat=" + lat).read())

    near_response = near_response[2:]
    near_response = near_response[:-1]
    near_response = near_response.replace("\\","")

    near_dict = json.loads(near_response)

    stops = near_dict['stops']

    nearest = []

    for i in range(3):
        stop = stops[i]

        nearest.append(stop) 

    return nearest

def get_nearest_recent():
    stops = get_nearest_stops()

    atco = stops[0]['atcocode']
    
    return get_next_bus(atco)
    
def get_live_from_atco(atco):
    return get_next_bus(atco)

def get_live_from_name(ind, name):
    stops = get_nearest_stops()

    for stop in stops:
        if ((str(stop['name']) == name) & (str(stop['indicator']) == ind)):
            return get_next_bus(stop)

print(get_live_from_name("opp","Moorlands Close"))
