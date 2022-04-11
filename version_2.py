from collections import Counter
import urllib.request
import csv
import networkx as nx
import matplotlib.pyplot as plt
# import mplcursors
# import mpld3
# from pyvis.network import Network
# import geopandas
import numpy as np
import powerlaw
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
    current_record = {}
    try:
        current_record['airline'] = route[0]
        current_record['airline_id'] = int(route[1])
        current_record['src_airport'] = route[2]
        current_record['src_airport_id'] = int(route[3])
        current_record['dest_airport'] = route[4]
        current_record['dest_airport_id'] = int(route[5])
        current_record['codeshare'] = route[6]
        current_record['stops'] = int(route[7])
        current_record['equipment'] = route[8]
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

removed = 0
for route in route_db:
    if route['src_airport_id'] in network.nodes() and route['dest_airport_id'] in network.nodes:

        # Skip if src and dest are of the same country
        if network.nodes[route['src_airport_id']]['country'] == network.nodes[route['dest_airport_id']]['country']:
            removed += 1
            continue
        else:
            print(network.nodes[route['src_airport_id']]['country'], network.nodes[route['dest_airport_id']]['country'])

        network.add_edge(route['src_airport_id'], route['dest_airport_id'],
                         airline=route['airline'],
                         airline_id=route['airline_id'],
                         stops=route['stops'],
                         equipment=route['equipment'])

print("Total Domestics Flights Removed : ", removed)

# Remove Empty NODES
for airport, degree in list(network.degree()):
    if degree == 0:
        network.remove_node(airport)

# print(nx.info(network, 507))
# print(nx.density(network))

# Degree Centrality
degree_centrality = nx.degree_centrality(network)
for airport, centrality_value in degree_centrality.items():
    network.nodes[airport]['degree_centrality'] = centrality_value

# Eigenvector Centrality
eigenvector_centrality = nx.eigenvector_centrality(network)
for airport, centrality_value in eigenvector_centrality.items():
    network.nodes[airport]['eigenvector_centrality'] = centrality_value

# Find the highest centrality
highest_degree_airport = max(network.nodes, key=lambda index: network.nodes[index]['degree_centrality'])
print("highest_degree_airport", network.nodes[highest_degree_airport])

highest_eigenvector_airport = max(network.nodes, key=lambda index: network.nodes[index]['eigenvector_centrality'])
print("highest_eigenvector_airport", network.nodes[highest_eigenvector_airport])

# Plot degree distribution
degree_dist = sorted((d for n, d in network.degree()), reverse=True)
degree_dist = list(filter(lambda num: num != 0, degree_dist))
degree_dist_counts = Counter(degree_dist)
fig, axs = plt.subplots(num=0, nrows=2, ncols=1)
fig_x = list(degree_dist_counts.keys())
fig_y = list(degree_dist_counts.values())
## Normal Plot
axs[0].plot(fig_x, fig_y, "b-", marker="o")
axs[0].set_ylabel('Occurences')
axs[0].set_xlabel('Degree')
## Log Scale Plot
axs[1].loglog(fig_x, fig_y, "b-", marker="o")
axs[1].set_ylabel('Occurences')
axs[1].set_xlabel('Degree')
## Estimate Power law exponent and plot best fit line
fit = powerlaw.Fit(degree_dist, xmax=max(fig_y), discrete=True)
fit_x = np.linspace(1, max(fig_x), 10)
A1 = fit.power_law.xmax
A2 = 1 / pow(max(fig_x), -fit.power_law.alpha)
A = (A1*0.9 + A2*0.1)

fit_y = A * pow(fit_x, -fit.power_law.alpha)
axs[1].text(1,1, f"Best Fit Power Law Exponent:\n{fit.power_law.alpha}", fontsize=12,
            horizontalalignment='left', verticalalignment='bottom')
plt.plot(fit_x, fit_y, '--r')

fig.tight_layout()

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
        network_main[route[0]][route[1]]['size'] = 1
    elif (network_main[route[0]][route[1]]['airline'] == "US"):
        network_main[route[0]][route[1]]['color'] = 'blue'
        network_main[route[0]][route[1]]['size'] = 1
    else:
        network_main[route[0]][route[1]]['color'] = 'black'
        network_main[route[0]][route[1]]['size'] = 1

plt.figure(1)
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

# Background world map
url = "https://cloud.netlifyusercontent.com/assets/344dbf88-fdf9-42bb-adb4-46f01eedd629/0263507c-98a1-4c3e-ab72-4d4239c831a5/01-world-opt.png"
response = urllib.request.urlopen(url)
data = response.read()
file = open("./data/worldmap.png", "wb")
file.write(data)
file.close()

img = plt.imread("./data/worldmap.png")
plt.imshow(img, zorder=0, extent=[-181, +180, -91, +98])

plt.tight_layout()
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
