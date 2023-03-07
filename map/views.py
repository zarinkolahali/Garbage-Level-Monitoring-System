from django.shortcuts import render
import folium
from map.models import EVChargingLocation, Tracker
from geopy import distance
from map import getroute

# Create your views here.
def index(request):
    stations = EVChargingLocation.objects.all()
    trackers = Tracker.objects.all()
    # create a Folium map centred on Connecticut
    m = folium.Map(location=[41.5, -72.7], zoom_start=8)

    tk = []
    st = []
    dict = {}
    
    # add a marker for every station and tracker
    for station in stations:

        dis = []
        min_route = 0

        for tracker in trackers:

            coordinates_tracker = [tracker.latitude, tracker.longitude]
            coordinates_station = [station.latitude, station.longitude]

            folium.Marker(coordinates_tracker, popup=tracker.tracker_name, icon=folium.Icon(color='lightgray', icon='car', prefix='fa')).add_to(m)

            if station.level <= 60 and station.level >= 0:
                folium.Marker(coordinates_station, popup=station.station_name, icon=folium.Icon(color='green', icon='home', prefix='fa')).add_to(m)

            if station.level <= 85 and station.level >= 60:
                folium.Marker(coordinates_station, popup=station.station_name, icon=folium.Icon(color='pink', icon='home', prefix='fa')).add_to(m)

            if station.level <= 100 and station.level >= 90:
                folium.Marker(coordinates_station, popup=station.station_name, icon=folium.Icon(color='red', icon='home', prefix='fa')).add_to(m)
                dis.append(distance.distance(coordinates_tracker, coordinates_station).km)
                min_route = dis.index(min(dis))

                if len(dis) == len(trackers):
                    dict[str(coordinates_station)] = min_route
    
            if station.level > 100 and station.level < 0:
                print("Error: Level is not in range")
    print(dict)
    for x,y in dict.items():
        latitude, longitude = x.split("[")[-1].split("]")[0].split()
        latitude=latitude.replace(",","")
        route = getroute.get_route(trackers[y].longitude, trackers[y].latitude, float(longitude), float(latitude))
        folium.PolyLine(route['route'], color='blue', weight=2.5, opacity=1).add_to(m)


    # save the map as an HTML file
    context = {'map': m._repr_html_()}

    return render(request, 'map/index_map.html', context)