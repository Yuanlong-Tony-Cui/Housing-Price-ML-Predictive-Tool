import osmnx as ox
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
from tqdm import tqdm
import json
import time

WAIT_SEC = 1.5
TIMEOUT = 5

def dist_to_POI(addresses,plot,option):
    # Get the coordinates of university campus
    geolocator = Nominatim(user_agent="my_app")
    # campus_location = geolocator.geocode("Earth Sciences Museum, Waterloo, Ontario, Canada", timeout=TIMEOUT)
    campus_location = geolocator.geocode("University of Toronto, Toronto, Ontario, Canada", timeout=TIMEOUT)
    campus_coords = (campus_location.latitude, campus_location.longitude)
    campus_graph = ox.graph_from_point(
        center_point = campus_coords,
        dist = 8000,
        network_type = "walk",
        simplify = True)

    # Import addresses and find node IDs
    print("Getting POI IDs")
    if (option == "grocery"):
        with open('Processing/grocery_addresses.json', 'r') as f:
            input_data = json.load(f)
    elif (option == "bus"):
        with open('Processing/bus_stop_addresses.json', 'r') as f:
            input_data = json.load(f)
    else:
        print("Specified option is not valid")
        return
    
    POIs = input_data['addresses']
    POI_ids = []
    for POI in tqdm(POIs):
        time.sleep(WAIT_SEC)
        POI_location = geolocator.geocode(POI, timeout=TIMEOUT)
        if POI_location is not None:
            POI_coords = (POI_location.latitude, POI_location.longitude)
            POI_id = ox.distance.nearest_nodes(
                G = campus_graph,
                X = POI_coords[1],
                Y = POI_coords[0])
            POI_ids.append(POI_id)

    if plot:
        fig0,ax0 = ox.plot.plot_figure_ground(
            G = campus_graph,
            show = False,
            close = False)
    
    # Calculate the road distance from each address to the closest POI
    print("Calculating distance to closest POI for each house")
    distances = []
    for address in tqdm(addresses):
        time.sleep(WAIT_SEC)
        house_location = geolocator.geocode(address, timeout=TIMEOUT)
        if house_location is None:
            distances.append(None)
        else:
            house_coords = (house_location.latitude, house_location.longitude)
            house_id = ox.distance.nearest_nodes(
                G = campus_graph,
                X = house_coords[1],
                Y = house_coords[0])
            routes = []
            for POI_id in POI_ids:
                route = ox.distance.shortest_path(
                    G = campus_graph,
                    orig = house_id,
                    dest = POI_id,
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
                    route_color = "red",
                    show = False,
                    close = False)
    if plot:
        plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
        plt.margins(0,0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.show()
    return distances
