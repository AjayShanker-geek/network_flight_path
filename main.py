# from matplotlib.pyplot import pink
# import networkx as nx
# import pandas as pd
# import numpy as np
# # import matplotlib as plt
# import geopandas as gp
# import matplotlib.pyplot as plt


# def iata_code(xxx):
#     return gps_airport[gps_airport['IATA'] == xxx]


# # File Path
# ROUTES_FILE = './data/routes.csv'
# routes = pd.read_csv(ROUTES_FILE, usecols=[
#                      'air', 'air_id', 'start', 'start_id', 'end', 'end_id'])

# # routes.head()
# # print()

# # Remove \N


# source_list = list(routes['start'].values)
# dest_list = list(routes['end'].values)

# sor = set(source_list)
# dest = set(dest_list)

# # print(sor.intersection(dest))

# # print (sor.union(dest) )

# # print(len(sor.union(dest) - sor.intersection(dest)))
# # print(sor.union(dest) - sor.intersection(dest))

# test_routes = routes['start'].unique()
# test_des = routes['end'].unique()
# # test_routes.append(test_des)
# airport_codes = list(np.concatenate((test_routes, test_des)))

# # create unique list of codes with GPS location. This will can be used to filtering in world airport gps locations.
# unique_codes = []
# for n in airport_codes:
#     if n not in unique_codes:
#         unique_codes.append(n)
# # print(unique_codes)

# COU_FILE = './data/countries.csv'
# gps_airport = pd.read_csv(COU_FILE, usecols=[
#     'country', 'IATA', 'ICAO', 'lat', 'long', 'alt'])

# # print(gps_airport.head())
# # print(iata_code('SIN'))
# # print(gps_airport.shape)


# latitude = []
# longitude = []
# for n in unique_codes:

#     if list(gps_airport[gps_airport['IATA'] == n]['lat']) != []:
#         latitude.append(list(gps_airport[gps_airport['IATA'] == n]['lat'])[0])

#     if list(gps_airport[gps_airport['IATA'] == n]['long']) != []:
#         longitude.append(
#             list(gps_airport[gps_airport['IATA'] == n]['long'])[0])

#     # print(n)
#     # latitude.append(list(gps_airport[gps_airport['IATA'] == n]['lat'])[0])
#     # longitude.append(list(gps_airport[gps_airport['IATA'] == n]['long'])[0])
#     if n not in list(gps_airport['IATA'].values):
#         print(f'lat or long missing {n}')
#         unique_codes.remove(n)

# # len(latitude) == len(longitude) == len(unique_codes)
# print(len(unique_codes))
# print(len(latitude))
# print(len(longitude))

# # create df with gps codes from the gps_codes into new df.

# # update df for routes and add source long, lat and similiarly dest long and dest lat.

# routes_dist = pd.DataFrame(
#     columns=['start', 'end', 'count', 'src_long', 'src_lat', 'dest_long', 'dest_lat'])


# routes_dist['start'] = routes['start']
# routes_dist['end'] = routes['end']
# # routes_dist['count'] = routes['count']

# test = list(routes_dist['start'].unique())

# # function to create unique list of shape and latitude/ longitude

# shape_list = []
# short_lat = []
# short_long = []

# for n in test:
#     mask = routes_dist[routes_dist['start'] == n]
#     shape_list.append(mask.shape[0])


# for m in test:

#     # print(short_lat.append(
#     #     [list(gps_airport[gps_airport['IATA'] == m]['lat'])]))

#     if list(gps_airport[gps_airport['IATA'] == n]['lat']) != []:
#         short_lat.append(
#             [list(gps_airport[gps_airport['IATA'] == m]['lat'])])

#     if list(gps_airport[gps_airport['IATA'] == n]['long']) != []:
#         short_long.append(
#             [list(gps_airport[gps_airport['IATA'] == m]['long'])])


# # print(shape_list)
# # print(short_lat)

# # create list of lat and long using the above function for short_lat and short_long.

# lat = []
# long = []
# for i, shape in enumerate(shape_list):
#     lat.append(short_lat[i]*shape)
#     long.append(short_long[i]*shape)
# # print(lat)
# # print(long)


# # flatten the lists of lat and long

# def flatten_list(name_list):
#     return [item for sublist in name_list for item in sublist]


# lat = flatten_list(lat)
# long = flatten_list(long)


# # update the df with the source long and lat
# routes_dist['src_long'] = long
# routes_dist['src_lat'] = lat

# # print(routes_dist.head())

# # udpate the destination gps locations. using same steps as source gps locations.

# # sort the dataframe with respect to dest
# routes_dist.sort_values(by=['end'], inplace=True)


# # prepare the list of unique airport codes used in destination.
# test_dest = list(routes_dist['end'].unique())

# # print(len(test_dest))
# # crab the shape of each airport in dest column of routes_dist['dest']
# shape_dest_list = []

# for n in test_dest:
#     mask = routes_dist[routes_dist['end'] == n]
#     shape_dest_list.append(mask.shape[0])

# # print(shape_dest_list)
# # populate the latitude and longitude data from gps_codes file into dest_lat and dest_long
# dest_lat = []
# dest_long = []
# for m in test_dest:
#     dest_lat.append([list(gps_airport[gps_airport['IATA'] == m]['lat'])])
#     dest_long.append([list(gps_airport[gps_airport['IATA'] == m]['long'])])


# # # create list of lat and long using the above function for dest_lat and dest_long. The data is shortened form
# # # update, the cells below multiplies shape with latitude and longitude. To match the lenghts of the df

# lat_dest = []
# long_dest = []
# for i, shape in enumerate(shape_dest_list):
#     lat_dest.append(dest_lat[i]*shape)
#     long_dest.append(dest_long[i]*shape)


# # ## flatten the lists
# lat_dest = flatten_list(lat_dest)
# long_dest = flatten_list(long_dest)


# # ## update the dataframe with the new values of dest long and dest lat

# # # # update the df with the source long and lat
# routes_dist['dest_long'] = long_dest
# routes_dist['dest_lat'] = lat_dest

# # rest the dataframe with source column and rearrange
# routes_dist = routes_dist.reset_index(drop=True)
# routes_dist.sort_values(by=['start'], inplace=True)
# # routes_dist.head(25)


# # print(routes_dist.head())


# # create dataframe with longtitude and latitude along with airport codes

# df = pd.DataFrame(
#     {
#         'iata': unique_codes,
#         'latitude': latitude,
#         'longitude': longitude
#     })

# # gdf = gp.GeoDataFrame(
# #     df, geometry=gp.points_from_xy(df.longitude, df.latitude))


# # print(df.head())
