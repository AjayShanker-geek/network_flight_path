import csv

print("Reading routes file")
routes = []
with open("./data/routes.dat", "r") as f:
    for line in csv.reader(f, delimiter=','):
        src = line[2]
        dest = line[4]
        routes.append([src, dest])

print("Parsing routes array")
bidirectional_count = 0
single_directional_count = 0
single_directional_routes = []
for i, route in enumerate(routes):
    if route[::-1] in routes:
        bidirectional_count += 1
        continue # bidirectional
    else:
        single_directional_count += 1
        single_directional_routes.append(routes)

print("bidirectional_count", bidirectional_count)
print("single_directional_count", single_directional_count)
print("single_directional_routes", single_directional_routes)
