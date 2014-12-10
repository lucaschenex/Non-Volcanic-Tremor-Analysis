from __future__ import division
import csv
import Pycluster
import numpy as np
import matplotlib.pyplot as plt

north_bound = 42
west_bound = -124
stations_info = dict()
parameters = []
clusters = dict()

with open("stations.txt", "rb") as csvfile:
	spamreader = csv.reader(csvfile, delimiter='|', quotechar='|')
	first_line = True
	for row in spamreader:
		#print row
		if first_line:
			first_line = False
			parameters = map(lambda x: x.strip(), row)
		else:
			network = row[0]
			station = row[1]
			if network != "NC":
				continue
			if station not in stations_info:
				stations_info[station] = dict()
			station_info = stations_info[station]
			for i in range(2, len(row)):
				station_info[parameters[i]] = row[i]
			lat = float(station_info["Latitude"])
			lon = float(station_info["Longitude"])
			if lat == 0 or lon == 0 or lat > north_bound or lon < west_bound:
				continue
			row_x = int ((north_bound - lat) / (6/10))
			col_y = int ((lon - west_bound) / (4/5))
			cluster_id = (row_x, col_y)
			if cluster_id not in clusters:
				clusters[cluster_id] = dict()
			clusters[cluster_id][station] = (row[-2], row[-1])

station_id_map = stations_info.keys()
vectors = []
for key in station_id_map:
	vectors.append([float(stations_info[key]["Latitude"]), float(stations_info[key]["Longitude"])])

def euclidean(a, b):
	return np.linalg.norm(np.array(a)-np.array(b))

def get_distance_matrix(points, distance_function):
    distances = []
    for j in range(0, len(points)):
        p1 = points[j]
        temp = []
        for i in range(0,len(points)):
            p2 = points[i] 
            temp.append ( distance_function(p1,p2) )
        distances.append (temp)
    return distances

nb_clusters = 15 # this is the number of cluster the dataset is supposed to be partitioned into
distances = get_distance_matrix(vectors, euclidean)
clusterid, error, nfound = Pycluster.kmedoids(distances, nclusters= nb_clusters, npass=100)

uniq_ids = list(set(clusterid))

new_ids = [ uniq_ids.index(val) for val in clusterid]


myColorMap =plt.cm.Accent_r
for i in range(len(clusterid)):
    p = vectors[i]
    # convert the new_ids value to a value between 0 and 1
    c = float(new_ids[i])/len(uniq_ids)
    plt.scatter (p[0], p[1], color=myColorMap(c) )



for i in uniq_ids:
    p = vectors[i]
    plt.scatter (p[0], p[1], color = myColorMap(0), marker = "+" )

plt.grid()
plt.show()


		


