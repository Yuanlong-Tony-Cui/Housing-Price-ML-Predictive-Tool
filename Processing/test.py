import osmnx as ox
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt

geolocator = Nominatim(user_agent="my_app")
campus_location = geolocator.geocode("Earth Sciences Museum, Waterloo, Ontario, Canada")
campus_coords = (campus_location.latitude, campus_location.longitude)
g = ox.graph_from_point(campus_coords, dist=1000, network_type="walk", simplify=True)
print(campus_coords)

fig0,ax0 = ox.plot.plot_figure_ground(g,show=False,close=False)

house_location = geolocator.geocode("240 Westmount Rd N, Waterloo, Waterloo, ON")
house_coords = (house_location.latitude, house_location.longitude)
print(house_coords)

id0 = ox.distance.nearest_nodes(g, X=campus_coords[1], Y=campus_coords[0], return_dist=False)
print(id0)
id1 = ox.distance.nearest_nodes(g, X=house_coords[1], Y=house_coords[0], return_dist=False)
print(id1)

route = ox.distance.shortest_path(
                G=g,
                orig=id1,
                dest=id0,
                weight='length'
            )
print(route)
fig1,ax1=ox.plot.plot_graph_route(g,route,ax=ax0,route_color="blue",show=False,close=False)



plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
plt.margins(0,0)
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())

plt.show()