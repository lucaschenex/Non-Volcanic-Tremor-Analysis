import math

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
def distance_senity_check(lat1, long1, lat2, long2):
	if (distance_on_unit_sphere(lat1, long1, lat2, long2) < 3):
		return False
	else:
		return True















