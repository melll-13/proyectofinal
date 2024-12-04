import folium
from folium.plugins import MarkerCluster
import heapq
from geopy.distance import geodesic

# Locations (latitude and longitude)
locations = {
    "AG - Agora": (19.053210013385815, -98.28128742657283),
    #"AG - Artes Escenicas": (19.053210013385815, -98.28128742657284),
    "HU - Asuntos Internacionales": (19.052913803457084, -98.28059422919708),
    "AU - Auditorio Guillermo y Sofia Jenkins": (19.05350706713399, -98.28261182994294),
    "BI - Biblioteca": (19.054322115740042, -98.28317056118392),
    "CE - Centro Estudiantil": (19.053886165038303, -98.28388686101674),
    "CN - Ciencias A-4": (19.053870266037862, -98.2821119786718),
    "CI - Ciencias (Laboratorios)": (19.05419203845536, -98.28122043032522),
    "SL - Ciencias de la salud-36": (19.054162561404176, -98.28389564813112),
    "CS - Ciencias sociales": (19.053295392490064, -98.28375808824501),
    "PU - Comunicacion": (19.056775063352113, -98.28224018945284),
    "1 - Credito y Cobranza": (19.054820797424636, -98.28241548750108),
    "HU - Humanidades-31": (19.052913803457084, -98.28059422919708),
    "IA - Ingenierias-2": (19.05405533964374, -98.28188264980193),
    "1- Incorporacion estudiantil": (19.054820797424636, -98.28241548750108),
    "iOS - iOS Development Lab": (19.054099451038706, -98.28366265200468),
    "LB - Laboratorio B-34": (19.05435623227102, -98.28075227058156),
    "LA - Laboratorio A-3": (19.053765518233384, -98.281398682956),
    "NE - Negocios-8": (19.052758175314935, -98.28378666522364),
    "PF - Planta Fisica": (19.0565756349198, -98.2832665128955),
    "HA - Rectoria": (19.053015080200954, -98.2820424131189),
    "RH - Recursos Humanos": (19.056484269097776, -98.28234267095792),
    "TI - Tecnologias de Informacion": (19.053988978114738, -98.28248958266256),
    #"HU - Udlap Consultores": (19.052913803457084, -98.28059422919708),
    "A - Alberca": (19.054158177381485, -98.28720261139927),
    "CL - Campo de lanzamiento": (19.056136805845778, -98.28501153489843),
    "CFR - Cancha de futbol Rapido": (19.055656235693295, -98.28017171505046),
    "BQ - Canchas de basquetbol": (19.053792166104422, -98.28741373974674),
    "CT - Canchas de tenis": (19.053140178560856, -98.28749235126895),
    "GA - Gimnasio Morris 'Moe Willams'": (19.05466918675329, -98.28685327789827),
    "GB - Gimnasio de pesas": (19.053785740261244, -98.28753491771305),
    "GC - Gimnasio Luis 'Luison' Gomez Lopez": (19.05465144004459, -98.28775718230143),
    "ATL - Pista de atletismo": (19.05569681913915, -98.28765345532236),
    "TD - Templo de Dolor": (19.054943586961063, -98.2854702211442),
    "CC - Colegio Cain-Murray": (19.054821978770796, -98.28382659085489),
    "CL - Colegio Ray Lindley": (19.053748103829864, -98.28481167484523),
    "CB - Colegio Ignacio Bernal": (19.051735716854534, -98.27997742843714),
    "CG - Colegio Jose Gaos": (19.05193113472868, -98.28494296561416),
    "J1 - Plaza de las Banderas": (19.05426306547253, -98.28280708433341),
    "J2 - Jardin de la Fogata": (19.051554408891622, -98.28296897903022),
    "J3 - Jardin de la Meditacion": (19.05192314282747, -98.28290436705785),
    "J4 - Jardin de la pareja": (19.054514299857093, -98.28344346595397),
    "J5 - Lago": (19.05415682972365, -98.2846504600154),
    "J6 - Jardin Central": (19.05364217279041, -98.28319133831576),
    "CIR - Centro Intregal de Rehabilitacion": (19.054680089797536, -98.2873922961321),
    "AC - Analisis clinicos": (19.051445095594623, -98.28082959879515),
    "S - Seguridad": (19.0529754282607, -98.27969188416905),
    "CE - Tienda Universitaria": (19.053886165038303, -98.28388686101674),
    #"1 - Unicaja": (19.054820797424636, -98.28241548750108),
}

# Create a weighted graph based on distances between locations
def create_graph(locations, avoid_direct=False, start=None, end=None):
    graph = {name: {} for name in locations}  # Initialize empty adjacency list
    location_list = list(locations.items())  # Convert to list for pairwise comparison

    for i, (name1, coord1) in enumerate(location_list):
        for j, (name2, coord2) in enumerate(location_list):
            if i != j:  # Avoid self-loops
                # Prevent any direct paths (if specified)
                if avoid_direct and start and end and (name1 == start and name2 == end) or (name1 == end and name2 == start):
                    continue

                distance = geodesic(coord1, coord2).kilometers  # Calculate distance
                graph[name1][name2] = distance

    return graph

# Dijkstra's algorithm
def dijkstra(graph, start, end):
    priority_queue = [(0, start)]  # (distance, node)
    distances = {node: float('inf') for node in graph}  # Set all distances to infinity
    distances[start] = 0  # Start node distance is 0
    previous_nodes = {node: None for node in graph}  # To reconstruct the path

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    # Reconstruct the shortest path
    path = []
    current = end
    while current:
        path.insert(0, current)
        current = previous_nodes[current]

    return path, distances[end]

# Function to calculate total distance of a path
def calculate_total_distance(path, locations):
    total_distance = 0
    for i in range(len(path) - 1):
        point1 = locations[path[i]]
        point2 = locations[path[i + 1]]
        total_distance += geodesic(point1, point2).km
    return total_distance

# Create map with both paths and distances
def create_map_with_paths(locations, path1, path2, distance1, distance2):
    center_lat = sum(lat for lat, lon in locations.values()) / len(locations)
    center_lon = sum(lon for lat, lon in locations.values()) / len(locations)

    map_with_paths = folium.Map(location=[center_lat, center_lon], zoom_start=14)
    marker_cluster = MarkerCluster().add_to(map_with_paths)

    for name, (lat, lon) in locations.items():
        folium.Marker(location=[lat, lon], popup=name, tooltip=name).add_to(marker_cluster)

    # Add path 1 (first shortest path)
    for i in range(len(path1) - 1):
        point1 = locations[path1[i]]
        point2 = locations[path1[i + 1]]
        folium.PolyLine([point1, point2], color="blue", weight=2.5, opacity=1).add_to(map_with_paths)
        midpoint = [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2]
        distance_text = f"{geodesic(point1, point2).km:.2f} km"
        folium.Marker(location=midpoint, popup=distance_text, icon=folium.Icon(color="blue")).add_to(map_with_paths)

    # Add path 2 (alternate shortest path)
    for i in range(len(path2) - 1):
        point1 = locations[path2[i]]
        point2 = locations[path2[i + 1]]
        folium.PolyLine([point1, point2], color="red", weight=2.5, opacity=1).add_to(map_with_paths)
        midpoint = [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2]
        distance_text = f"{geodesic(point1, point2).km:.2f} km"
        folium.Marker(location=midpoint, popup=distance_text, icon=folium.Icon(color="red")).add_to(map_with_paths)

    
    # Add a combined total distance marker at the destination point
    destination_lat = locations[path1[-1]][0]  # Using the last location from path1 (destination)
    destination_lon = locations[path1[-1]][1]

    popup_text = f"1st Path Total Distance: {distance1:.14f} km\n2nd Path Total Distance: {distance2:.14f} km"

    # Create a single marker at the destination point with the popup showing both distances
    folium.Marker(
        location=[destination_lat, destination_lon],
        popup=popup_text,
        icon=folium.Icon(color="green")
    ).add_to(map_with_paths)

    return map_with_paths

# Main logic
if __name__ == "__main__":
    start_location = input("\nEnter the start location: ")
    end_location = input("Enter the destination location: ")

    if start_location not in locations or end_location not in locations:
        print("Invalid locations entered.")
    else:
        print(f"Calculating shortest paths from {start_location} to {end_location}...")

        # Create graph without direct path
        graph_no_direct = create_graph(locations, avoid_direct=True, start=start_location, end=end_location)

        # Find the first shortest path (without direct path)
        shortest_path, shortest_distance = dijkstra(graph_no_direct, start_location, end_location)

        # Print distances between locations on the shortest path with high precision
        print("\nDistances on the shortest path:")
        for i in range(len(shortest_path) - 1):
            point1 = locations[shortest_path[i]]
            point2 = locations[shortest_path[i + 1]]
            distance = geodesic(point1, point2).km
            print(f"{shortest_path[i]} -> {shortest_path[i + 1]}: {distance:.14f} km")

        # Calculate total distance for the shortest path
        total_distance_1 = calculate_total_distance(shortest_path, locations)
        print(f"Total Distance of the 1st Path: {total_distance_1:.14f} km")

        # Create a modified graph excluding the first path nodes (but not directly banning origin-destination)
        nodes_to_exclude = set(shortest_path[1:-1])
        modified_locations = {k: v for k, v in locations.items() if k not in nodes_to_exclude}
        graph_no_direct_2 = create_graph(modified_locations, avoid_direct=True, start=start_location, end=end_location)

        # Find the second shortest path
        alternate_path, alternate_distance = dijkstra(graph_no_direct_2, start_location, end_location)

        # Print distances between locations on the alternate path with high precision
        print("\nDistances on the alternate path:")
        for i in range(len(alternate_path) - 1):
            point1 = locations[alternate_path[i]]
            point2 = locations[alternate_path[i + 1]]
            distance = geodesic(point1, point2).km
            print(f"{alternate_path[i]} -> {alternate_path[i + 1]}: {distance:.14f} km")

        # Calculate total distance for the alternate path
        total_distance_2 = calculate_total_distance(alternate_path, locations)
        print(f"Total Distance of the 2nd Path: {total_distance_2:.14f} km")

        # Ensure the second path is different from the first path
        if alternate_path == shortest_path:
            print("The alternate path is identical to the shortest path.")
        else:
            # Create map for both paths
            map_with_both_paths = create_map_with_paths(locations, shortest_path, alternate_path, total_distance_1, total_distance_2)

            # Save the map with both paths
            map_with_both_paths.save("udlap_paths_combined.html")
            print("Map with both paths saved as 'udlap_paths_combined.html'.")
