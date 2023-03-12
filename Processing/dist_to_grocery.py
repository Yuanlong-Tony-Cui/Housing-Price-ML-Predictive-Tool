import osmnx as ox
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
from tqdm import tqdm
import json

def dist_to_grocery(addresses,plot):
    # Get the coordinates of University of Waterloo campus, using the museum as roughly the center of campus
    geolocator = Nominatim(user_agent="my_app")
    campus_location = geolocator.geocode("Earth Sciences Museum, Waterloo, Ontario, Canada")
    campus_coords = (campus_location.latitude, campus_location.longitude)
    campus_graph = ox.graph_from_point(
        center_point = campus_coords,
        dist = 6000,
        network_type = "walk",
        simplify = True)

    # Import grocery stores addresses and find node IDs
    print("Getting grocery stores IDs")
    with open('Processing/grocery_addresses.json', 'r') as f:
        input_data = json.load(f)
    groceries = input_data['addresses']
    grocery_ids = []
    for grocery in tqdm(groceries):
        grocery_location = geolocator.geocode(grocery)
        if grocery_location is not None:
            grocery_coords = (grocery_location.latitude, grocery_location.longitude)
            grocery_id = ox.distance.nearest_nodes(
                G = campus_graph,
                X = grocery_coords[1],
                Y = grocery_coords[0])
            grocery_ids.append(grocery_id)

    if plot:
        fig0,ax0 = ox.plot.plot_figure_ground(
            G = campus_graph,
            show = False,
            close = False)
    
    # Calculate the road distance from each address to the closest grocery store
    print("Calculating distance to closest grocery store for each house")
    distances = []
    for address in tqdm(addresses):
        house_location = geolocator.geocode(address)
        if house_location is None:
            distances.append(None)
        else:
            house_coords = (house_location.latitude, house_location.longitude)
            house_id = ox.distance.nearest_nodes(
                G = campus_graph,
                X = house_coords[1],
                Y = house_coords[0])
            routes = []
            for grocery_id in grocery_ids:
                route = ox.distance.shortest_path(
                    G = campus_graph,
                    orig = house_id,
                    dest = grocery_id,
                    weight = "length")
                routes.append(route)
            shortest_distance = float('inf')
            for route in routes:
                distance = sum(ox.utils_graph.get_route_edge_attributes(
                    G = campus_graph,
                    route = route,
                    attribute = "length"))
                distance = round(distance/1000,2)
                if distance < shortest_distance:
                    shortest_distance = distance
                    shortest_route = route
            distances.append(shortest_distance)

            if plot:
                fig0,ax0 = ox.plot.plot_graph_route(
                    G = campus_graph,
                    route = shortest_route,
                    ax = ax0,
                    route_color = "blue",
                    show = False,
                    close = False)
    if plot:
        plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
        plt.margins(0,0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.show()
    return distances
