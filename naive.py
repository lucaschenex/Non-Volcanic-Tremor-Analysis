from __future__ import division
import csv
import math

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
	print clusters


#########################################
#	input: stationA, stationB objects	#
#	output: geographical distance 		#
#			between them, in km 		#
#########################################
def distance_on_unit_sphere(lat1, long1, lat2, long2):
 
    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
         
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
         
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
         
    # Compute spherical distance from spherical coordinates.
         
    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
     
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
 
    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    # Multiplier is the ratio between *km* and earth arc coverage
    return arc * 6373

#########################################
#	input: stationA, stationB objects	#
#	output: geographical distance 		#
#			between them, in km 		#
#########################################
def isvalid(stationA, stationB):
	lat1 = stations_info[stationA]["Latitude"]
	long1 = stations_info[stationA]["Longitude"]
	lat2 = stations_info[stationB]["Latitude"]
	long2 = stations_info[stationB]["Longitude"]

	if (distance_on_unit_sphere(float(lat1), float(long1), float(lat2), float(long2)) < 3):
		return False
	else:
		return True


#{clusterID:{stationID:(yearS, yearE)}}

def cover_time(clusterdic):
	returncluser = {}
	for cluster in clusterdic:
		returncluser[cluster]=[]
		stationdic = clusterdic[cluster]
		stationID, start, end, restlist = findearliest(stationdic)
		returncluser[cluster].append(stationID)
		while(len(restlist)!=0):
			stationID, start, end, restlist = findsuitable(restlist, start, end)
			returncluser[cluster].append(stationID)
	return returncluser

def findsuitable(rest, start, end):
	flag, stationinfo, new = isoverlap(rest, start, end)
	if flag:
		maxdur = 0
		returnstation =0
		returnstart = 0
		returnend = 0
		for station in new:
			dur = toyear(new[station][1])-end
			if dur>maxdur:
				maxdur = dur
				returnstation = station
				returnstart = new[station][0]
				returnend = new[station][1]
		del rest[returnstation]
		returnrest = rest
		for key in rest:
			if not isvalid(returnstation, key):
				del returnrest[key]
		return returnstation, returnstart, returnend, returnrest

	else:
		del rest[stationinfo[0]]
		returnrest = rest
		for key in rest:
			if not isvalid(stationinfo[0], key):
				del returnrest[key]
		return stationinfo[0], stationinfo[1], stationinfo[2], returnrest

def isoverlap(rest, start, end):
	new = rest
	flag  = False
	near = 1000
	returnstat = 0
	returnstart = 0
	returnend = 0
	for station in rest:
		s = toyear(rest[station][0])
		if abs(s-start)<near:
			returnstat = station
			returnstart = rest[station][0]
			returnend = rest[station][1]

		if s>start:
			del new[station]
		else:
			flag = True
	if flag:
		return flag, 0, new
	else:
		return flag, [returnstat, returnstart, returnend], rest   

def findearliest(stationlist):
	earliest = 2222
	end = 0
	stationID = 0
	for station in stationlist:
		start = toyear(stationlist[station][0])
		if start<earliest:
			earliest = start
			end = stationlist[station][1]
			stationID = station

	del stationlist[stationID]
	returnstationlist = stationlist
	for key in stationlist:
		if not isvalid(stationID, key):
			del returnstationlist[key]
	return stationID, earliest, end, returnstationlist

def toyear(time):
	return int(time.split("-")[0])






print cover_time(clusters)
		