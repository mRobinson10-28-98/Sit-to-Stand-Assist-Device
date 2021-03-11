import pygame
import math
import csv
import Parameters as par
import Basic_Functions as bf
from Point import Point
from Linkage import Linkage

fileWriteName = '/home/pi/Documents/Senior Design/Hip Curves/03032021.csv'
fileReadName = '/home/pi/Documents/Senior Design/Hip Curves/03032021.csv'

pygame.init()

win = pygame.display.set_mode((par.screen_dim, par.screen_dim))
pygame.display.set_caption('Senior Design Inverse Kinetics!')

# List of Point elements
points = []

#List of point element coordinates
points_coordinates = []

#List of previously deleted points
deleted_points = []
print(5)
# All paramters in feet from floor below the origin (below bottom left by a distance of origin_height)
def create_point_array(x_min, x_max, y_min, y_max, increment):
    for pntx in range(bf.feet_to_pixels(x_min), bf.feet_to_pixels(x_max) + 1, bf.feet_to_pixels(increment)):
        for pnty in range(bf.feet_to_pixels(y_min), bf.feet_to_pixels(y_max) + 1, bf.feet_to_pixels(increment)):
            points.append(Point(bf.feet_to_pixels(par.origin_x) + pntx, par.screen_dim - (pnty)))


def initialize_screen():
    pygame.time.delay(par.time_delay)
    win.fill((200, 200, 200))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


def create_linkage_system():
    link1 = Linkage(bf.feet_to_pixels(par.origin_x), bf.feet_to_pixels(par.screen_dim_feet - par.origin_height),
                    bf.feet_to_pixels(par.a1), -current_point.theta1, par.blue, linkages)
    link2 = Linkage(link1.x2 - bf.feet_to_pixels((par.L2 / 2 + par.d2) * math.cos(-current_point.theta2)),
                    link1.y2 - bf.feet_to_pixels((par.L2 / 2 + par.d2) * math.sin(-current_point.theta2)),
                    bf.feet_to_pixels(par.L2),
                    -current_point.theta2, par.blue, linkages)

    actuator1 = Linkage(bf.feet_to_pixels(par.actuator1_ground[0]) + bf.feet_to_pixels(par.origin_x),
                        par.screen_dim - bf.feet_to_pixels(par.origin_height + par.actuator1_ground[1]),
                        bf.feet_to_pixels(current_point.actuator1_length), -current_point.phi1, par.red, linkages)

    actuator2 = Linkage(bf.feet_to_pixels(par.origin_x) + bf.feet_to_pixels(par.actuator2_ground[0]),
                        par.screen_dim - bf.feet_to_pixels(par.origin_height) - bf.feet_to_pixels(par.actuator2_ground[1]),
                        bf.feet_to_pixels(current_point.actuator2_length), -current_point.phi2, par.red, linkages)

linkages = []
initial_linkage_point = []

class Clock:
    def __init__(self, time = 0):
        self.time = time
        self.previous = False
        self.current = False

    def update(self):
        self.time = pygame.time.get_ticks()

    def passed(self):
        return pygame.time.get_ticks() - self.time
    
class CSV:
    def __init__(self, filename):
        self.filename = filename
        self.csvList = []
        
    def append_for_csv(self, append_list):
        self.csvList.append(append_list)
        
    def write_csv(self):
        print(' -   -   -   -   -   -   -   -   -   -   -   -  ')
        print(self.csvList)
        with open(self.filename, 'w', newline = '') as new_file:
            lengthWriter = csv.writer(new_file, delimiter = ',')
            for column in self.csvList:
                lengthWriter.writerow([str(column[0]), str(column[1]), str(column[2]), str(column[3])])
                
    def append_and_write_csv(self):
        self.csvList = []
        for point in range(0, len(points)):
            bf.initialize_screen()
            linkages = []
            self.point = points[point]
            current_point = self.point
            self.point.calculate_system()
            self.append_for_csv()
            bf.create_linkage_system()
            bf.draw_screen(win, [linkages, points])
            
        self.write_csv()


left_click = Clock()
right_click = Clock()
k_click = Clock()
z_click = Clock()
r_click = Clock()
l_click = Clock()
j_click = Clock()
p_click = Clock()
d_click = Clock()
a_click = Clock()
space_click = Clock()
ctrl_click = Clock()
shift_click = Clock()

csvWriter = CSV(fileWriteName)

point_index = 0

#points.append(Point(feet_to_pixels(origin_x) + 1, screen_height - feet_to_pixels(origin_height + L1)))
create_point_array(1.5, 4, par.origin_height - 1, par.origin_height + 2.5, 0.05)

patient_weight = 200
patient_angle = -math.pi / 2

total_load = 0
good_points = 0
#run_DPIM = False
actuator2_in_plane = False
run = True
while run:
    
    initialize_screen()

    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse_press = pygame.mouse.get_pressed()
    mouse_left_click = mouse_press[0]
    mouse_right_click = mouse_press[2]

    #Calculate all position and force variables based on current point
    current_point = points[point_index]
    current_point.FL = patient_weight
    current_point.angle = patient_angle
    current_point.calculate_system()


    if mouse_left_click and left_click.passed() > 200:
        left_click.update()
        points.append(Point(mouse_pos[0], mouse_pos[1]))
        points_coordinates.append((mouse_pos[0], mouse_pos[1]))

    # If "k" is pressed, delete all points other than original
    if keys[pygame.K_k] and k_click.passed() > 200:
        points = []
        points.append(Point(mouse_pos[0], mouse_pos[1]))
        point_index = 0
        k_click.update()

    #If "z" is pressed, delete previous point, and add it to deleted points list
    if keys[pygame.K_z] and z_click.passed() > 200:
        deleted_points.append(Point(points_coordinates[-1][0], points_coordinates[-1][1]))
        points.pop(-1)
        points_coordinates.pop(-1)
        z_click.update()

    #If "r" is pressed, redraw point most previously deleted (redo)
    if keys[pygame.K_r] and r_click.passed() > 200:
        if len(deleted_points) > 0:
            points.append(deleted_points[-1])
            points_coordinates.append((mouse_pos[0], mouse_pos[1]))
            deleted_points.pop(-1)
        r_click.update()

    #If "l" is pressed, go to next point in list
    if keys[pygame.K_l] and l_click.passed() > 10:
        points[point_index].load_vector_length = 0
        if point_index < len(points) - 1:
            point_index = point_index + 1
        else:
            point_index = 0
        l_click.update()

    #If "j" is pressed, go to previous point in list
    if keys[pygame.K_j] and j_click.passed() > 80:
        points[point_index].load_vector_length = 0
        if point_index > 0:
            point_index = point_index - 1
        else:
            point_index = len(points) - 1
        j_click.update()

    # If "d" is pressed, rotate load angle CCW
    if keys[pygame.K_d] and d_click.passed() > 80:
        patient_angle = current_point.angle - math.pi / 12
        d_click.update()

    # If "a" is pressed, rotate load angle CCW
    if keys[pygame.K_a] and a_click.passed() > 80:
        patient_angle = current_point.angle + math.pi / 12
        a_click.update()
        
    if keys[pygame.K_SPACE] and space_click.passed() >= 200:
        if keys[pygame.K_LCTRL] and ctrl_click.passed() >= 200:
            csvWriter.append_and_write_csv()
            ctrl_click.update()
        
        if keys[pygame.K_LSHIFT] and shift_click.passed() >= 200:
            points = []
            with open(fileReadName, 'r') as csv_read_file:
                csv_reader = csv.reader(csv_read_file)
                for line in csv_reader:
                    points.append(Point(int(float(line[2])), int(float(line[3]))))
                
            shift_click.update()
        space_click.update()

    #Add linkages and actuators
    linkages = []

    create_linkage_system()

    if keys[pygame.K_p] and p_click.passed() > 200:
        current_point.print_point()
        p_click.update()

    bf.draw_screen(win, [linkages, points])

    if abs(current_point.FH1) < par.actuator1_parameters[0] and current_point.actuator1_length > par.actuator1_parameters[1] and current_point.actuator1_length < par.actuator1_parameters[2]:
        if abs(current_point.FH2) < par.actuator2_parameters[0] and current_point.actuator2_length > par.actuator2_parameters[
            1] and current_point.actuator2_length < par.actuator2_parameters[2]:
            current_point.color = par.green

    pygame.display.update()
pygame.quit()
