import osmnx as ox
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
from tqdm import tqdm

def dist_to_campus(addresses,plot):
    # Get the coordinates of University of Waterloo campus, using the museum as roughly the center of campus
    geolocator = Nominatim(user_agent="my_app")
    campus_location = geolocator.geocode("Earth Sciences Museum, Waterloo, Ontario, Canada")
    campus_coords = (campus_location.latitude, campus_location.longitude)
    campus_graph = ox.graph_from_point(
        center_point = campus_coords,
        dist = 6000,
        network_type = "walk",
        simplify = True)
    campus_id = ox.distance.nearest_nodes(
        G = campus_graph,
        X = campus_coords[1],
        Y = campus_coords[0])
    if plot:
        fig0,ax0 = ox.plot.plot_figure_ground(
            G = campus_graph,
            show = False,
            close = False)
    # Calculate the road distance from each address to the campus
    print("Calculating distance to campus for each house")
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
            route = ox.distance.shortest_path(
                G = campus_graph,
                orig = house_id,
                dest = campus_id,
                weight = "length"
            )
            distance = sum(ox.utils_graph.get_route_edge_attributes(
                G = campus_graph,
                route = route,
                attribute = "length"
            ))
            distances.append(round(distance/1000,2))
            if plot:
                fig0,ax0 = ox.plot.plot_graph_route(
                    G = campus_graph,
                    route = route,
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
