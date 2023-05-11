import urllib.request
import urllib.parse
import urllib.error
import json

def find_station_from_coordinates(latitude, longitude, results=3): #returns last 3 stations names from all results 
    url = 'https://v5.bvg.transport.rest/stops/nearby?latitude='+str(latitude)+'&longitude='+str(longitude)+'&results='+str(results)
    html = urllib.request.urlopen(url).read()
    # print(html.decode()+'\n')
    html = json.loads(html) #make json from html
    station_names=[x['name'] for x in html]
    return station_names[-3:]

# find_station_from_coordinates(52.520008, 13.404954)