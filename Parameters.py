
red = (100, 0, 0)
blue = (10, 10, 100)
green = (10, 100, 10)
gray = (50, 50, 50)
white = (255, 255, 255)
purple = (100, 10, 100)
black = (10, 10, 10)

'''
All Measurement in FEET
x11: distance from center of link 1 to actuator 1 connection
x12: distance from center of link 1 to actuator 2 connection (should be L2/2)
x22: distance from center of link 2 to actuator 2 connection (should be L2/2)
m1: mass of link 1 (lbs)
m2: mass of link 2 (lbs)
d1: distance from link 1 center to connection to link 2 (should be L1/2)
d2: distance from link 2 center to connection to link 1
dHx: x distance from global origin to actuator 2 ground connection
'''

g = 32.2

m1 = 20 / g
m2 = 20 / g

L1 = 3
L2 = 3.5

#For next parameters:
#A POSITIVE sign indicates to the RIGHT of center,
#A NEGATIVE sign indicates to the LEFT of center,
x11 = -L1 / 4
x12 = 0
x22 = -L2 / 2 #SHOULD NOT CHANGE


d1 = L1/2 #SHOULD NOT CHANGE
d2 = 0
actuator1_ground = (1.8, -0.7)
actuator2_ground = (-1, 1)

# Max force, min distance, max distance
actuator1_parameters = (800, 19 / 12, 27 / 12)
actuator2_parameters = (400, 29 / 12, 47 / 12)

#origin_x arbitrarily place origin of mechanism on plane
origin_x = 3

#origin_height is the distance from the ground to the origin of the mechanism
origin_height = 1.5

#hip distances represent desired position ranges for mechanism
#heights are relative to ground, distances are relative to mechanism origin
hip_origin_positionx = 3.5
hip_origin_positiony = 0


a1 = L1/2 + d1
a2 = L2/2 - d2

time_delay = 30
screen_dim = 1000
screen_dim_feet = 8