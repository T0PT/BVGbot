import urllib.request
import urllib.parse
import urllib.error
import json

def find_station_from_coordinates(latitude, longitude, results=4): 
    url = 'https://v5.bvg.transport.rest/stops/nearby?latitude='+str(latitude)+'&longitude='+str(longitude)+'&results='+str(results)
    html = urllib.request.urlopen(url).read()
    # print(html.decode()+'\n')
    html = json.loads(html) #make json from html
    station_names=[x['name'] for x in html]
    station_ids= [x['id'] for x in html]
    return station_names, station_ids

def find_station_from_name(name='Alexandrplatz', results=4): 
    url = 'https://v5.bvg.transport.rest/locations?query=' + str(name) + '&results='+str(results)
    html = urllib.request.urlopen(url).read()
    # print(html.decode()+'\n')
    html = json.loads(html) #make json from html
    station_names=[x['name'] for x in html]
    station_ids= [x['id'] for x in html]
    return station_names, station_ids

def get_departures_from_station(station_id=900000200011, results=50, linesofstops=True, remarks=True): 
    url = 'https://v5.bvg.transport.rest/stops/'+str(station_id)+'/departures?duration='+str(results)
    url+='&linesOfStops='+str(linesofstops)+'&remarks='+str(remarks)
    # url = 'https://v5.bvg.transport.rest/stops/900000200011/departures?duration=10'
    html = urllib.request.urlopen(url).read()
    # print(html.decode()+'\n')
    html = json.loads(html) #make json from html
    # departures = [departure for departure in html]
    directions = [departure['direction'] for departure in html]
    times = [departure['when'] for departure in html]
    line_names = [departure['line']['name'] for departure in html]
    platforms = [departure['platform'] for departure in html]
    # print(times)
    # print(line_names)
    # print(directions) 
    # print(platforms)   
    return line_names, times, directions, platforms

get_departures_from_station(station_id='900000200011', results=30)