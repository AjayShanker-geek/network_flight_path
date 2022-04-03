import urllib.request
import csv
import networkx as nx
import matplotlib.pyplot as plt
# import mplcursors
# import mpld3
# from pyvis.network import Network
# import geopandas
import numpy as np
# from libpysal import weights

network = nx.Graph()

####
url = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat"

response = urllib.request.urlopen(url)
data = response.read()


file = open("./data/airports_db.dat", "wb")
file.write(data)
file.close()

f = open("./data/airports_db.dat", encoding="utf8")
airport_db = []  # main arrar for airport
errors = 0
for airport in csv.reader(f, delimiter=','):
    current_record = []
    try:
        # each slots containing information about an airport
        current_record.append(int(airport[0]))  # airport ID
        current_record.append(airport[1])
        current_record.append(airport[2])
        current_record.append(airport[3])
        current_record.append(airport[4])
        current_record.append(airport[5])
        current_record.append(float(airport[6]))
        current_record.append(float(airport[7]))
        current_record.append(float(airport[8]))
        current_record.append(float(airport[9]))
        current_record.append(airport[10])
        current_record.append(airport[11])
        current_record.append(airport[12])
        current_record.append(airport[13])
    except:
        errors += 1
    else:
        airport_db.append(current_record)
print("Total Airport Imported : ", len(airport_db),
      "# of Errors : ", errors)

####

url = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat"
response = ""
data = ""
response = urllib.request.urlopen(url)
data = response.read()
file = open("./data/routes_db.dat", "wb")
file.write(data)
file.close()

f = open("./data/routes_db.dat", encoding="utf8")
route_db = []
errors = 0
for route in csv.reader(f, delimiter=','):
    current_record = []
    try:
        current_record.append(route[0])
        current_record.append(int(route[1]))
        current_record.append(int(route[3]))
        current_record.append(int(route[5]))
        current_record.append(int(route[7]))
        current_record.append(route[8])

    except:
        errors += 1
    else:
        route_db.append(current_record)
print("Total Routes Imported : ", len(route_db), "# of Errors : ", errors)

####

for airport in airport_db:
    network.add_node(airport[0], id=airport[0], name=airport[1], city=airport[2],
                     country=airport[3], iata=airport[4],
                     icao=airport[5],
                     lat=airport[6],
                     long=airport[7],
                     alt=airport[8], offset=airport[9],
                     daylight=airport[10], timezone=airport[11],
                     type=airport[12], source=airport[13])

for route in route_db:
    if route[2] in network.nodes() and route[3] in network.nodes:
        network.add_edge(route[2], route[3], airline=route[0],
                         airline_id=route[1], stops=route[4],
                         equipment=route[5])

# print(nx.info(network, 507))
# print(nx.density(network))

degree_centrality = nx.degree_centrality(network)
for airport, centrality_value in degree_centrality.items():
    network.nodes[airport]['degree_centrality'] = centrality_value
print(network.nodes[507]['degree_centrality'])

# Remove NODES
for airport, degree in list(network.degree()):
    if degree == 0:
        network.remove_node(airport)

# Vis
main_subgraph = max(nx.connected_components(network), key=len)
network_main = network.subgraph(main_subgraph)
# print(network_main.nodes())

for airport in network_main.nodes():
    network_main.nodes[airport]['coordinates'] = (network_main.nodes[airport]['long'],
                                                  network_main.nodes[airport]['lat'])


maximum_centrality = max(degree_centrality.values())
for airport in network_main.nodes():
    if network_main.nodes[airport]['timezone'].find('Europe') == 0:
        network_main.nodes[airport]['color'] = 'blue'
    elif network_main.nodes[airport]['timezone'].find('Asia') == 0:
        network_main.nodes[airport]['color'] = 'red'
    elif network_main.nodes[airport]['timezone'].find('Africa') == 0:
        network_main.nodes[airport]['color'] = 'yellow'
    elif network_main.nodes[airport]['timezone'].find('America') == 0:
        network_main.nodes[airport]['color'] = 'green'
    elif network_main.nodes[airport]['timezone'].find('Australia') == 0:
        network_main.nodes[airport]['color'] = 'orange'
    elif network_main.nodes[airport]['timezone'].find('Pacific') == 0:
        network_main.nodes[airport]['color'] = 'purple'
    else:
        network_main.nodes[airport]['color'] = 'grey'

    if network_main.nodes[airport]['degree_centrality'] >= maximum_centrality * .9:
        network_main.nodes[airport]['importance'] = 400
    elif network_main.nodes[airport]['degree_centrality'] >= maximum_centrality * .5:
        network_main.nodes[airport]['importance'] = 150
    else:
        network_main.nodes[airport]['importance'] = 10

for route in network_main.edges():
    if (network_main[route[0]][route[1]]['airline'] == "TK"):
        network_main[route[0]][route[1]]['color'] = 'red'
        network_main[route[0]][route[1]]['size'] = 1.5
    elif (network_main[route[0]][route[1]]['airline'] == "US"):
        network_main[route[0]][route[1]]['color'] = 'blue'
        network_main[route[0]][route[1]]['size'] = 1.5
    else:
        network_main[route[0]][route[1]]['color'] = 'grey'
        network_main[route[0]][route[1]]['size'] = 0.2


nx.draw_networkx_nodes(network_main, nx.get_node_attributes(network_main, 'coordinates'), node_shape='.',
                       node_size=[importance for importance in nx.get_node_attributes(
                           network_main, 'importance').values()],
                       node_color=[color for color in nx.get_node_attributes(network_main, 'color').values()])
sc = nx.draw_networkx_edges(network_main, nx.get_node_attributes(network_main, 'coordinates'),
                            width=[size for size in nx.get_edge_attributes(
                                network_main, 'size').values()],
                            edge_color=[color for color in nx.get_edge_attributes(
                                network_main, 'color').values()],
                            alpha=0.1)

# # by default the tooltip is displayed "onclick"
# # we can change it by setting hover to True
# cursor = mplcursors.cursor(sc, hover=True)
# # by default the annotation displays the xy positions
# # this is to change it to the countries name


# @cursor.connect("add")
# def on_add(sel):
#     sel.annotation.set(text=list(network_main)[sel.target.index])

# nx.draw(sc)
# plt.draw()
plt.show()
# plt.savefig()
# mpld3.fig_to_html(plt)

# nt = Network('1000px', '1000px')
# nt.from_nx(network_main)
# nt.show('nx.html')
# file_path = "./map.geojson"
# world = geopandas.read_file(file_path)

# centroids = np.column_stack(
#     (world.centroid.x, world.centroid.y))

# queen = weights.Queen.from_dataframe(centroids)
# graph = queen.to_networkx()
# positions = dict(zip(graph.nodes, centroids))

# ax = world.plot(linewidth=1, edgecolor="grey", facecolor="lightblue")
# ax.axis([-12, 45, 33, 66])
# ax.axis("off")
# nx.draw(graph, positions, ax=ax, node_size=5, node_color="r")
# plt.show()
