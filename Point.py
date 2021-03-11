import Basic_Functions as bf
import Parameters as par
import math
import pygame

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = par.red
        self.radius = 3
        self.x_ft = bf.pixels_to_feet(self.x) - par.origin_x
        self.y_ft = bf.pixels_to_feet(par.screen_dim - self.y) - par.origin_height
        self.theta2 = 0
        self.theta1 =0
        self.theta2 = 0
        self.phi1 = 0
        self.actuator1_length = 0
        self.actuator2_xlength = 0
        self.actuator2_ylength =  0
        self.actuator2_length = 0
        self.phi2 = 0
        self.FL = 0
        self.angle = 0
        self.FH2 = 0
        self.RLy = 0
        self.RLx = 0
        self.FH1 = 0
        self.Ry = 0
        self.Rx = 0
        self.load_vector_length = 0


    def render(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)
        pygame.draw.line(window, par.purple, (self.x, self.y), (self.x - self.load_vector_length * math.cos(self.angle), self.y - self.load_vector_length * math.sin(self.angle)), 3)

    def calculate_system(self):
        self.load_vector_length = 80
        self.theta2 = -math.acos((self.x_ft ** 2 + self.y_ft ** 2 - par.a1 ** 2 - par.a2 ** 2) / (2 * par.a1 * par.a2))
        self.theta1 = math.atan((self.y_ft / self.x_ft)) - math.atan(
            (par.a2 * math.sin(self.theta2) / (par.a1 + par.a2 * math.cos(self.theta2))))
        self.theta2 = (self.theta1 + self.theta2)
        self.phi1 = math.atan2((par.L1 / 2 + par.x11) * math.sin(self.theta1) - par.actuator1_ground[1],
                               (par.L1 / 2 + par.x11) * math.cos(self.theta1) - par.actuator1_ground[0])
        self.actuator1_length = (((par.L1 / 2 + par.x11) * math.sin(self.theta1) - par.actuator1_ground[1]) ** 2 + (
                    (par.L1 / 2 + par.x11) * math.cos(self.theta1) - par.actuator1_ground[0]) ** 2) ** (1 / 2)
        self.actuator2_xlength = (par.L1 / 2 + par.d1) * math.cos(self.theta1) - (par.d2 - par.x22) * math.cos(-self.theta2) - par.actuator2_ground[0]
        self.actuator2_ylength = (par.L1 / 2 + par.d1) * math.sin(self.theta1) + (par.d2 - par.x22) * math.sin(-self.theta2) - par.actuator2_ground[1]
        self.actuator2_length = (self.actuator2_xlength ** 2 + self.actuator2_ylength ** 2) ** 0.5
        self.phi2 = math.atan2(self.actuator2_ylength, self.actuator2_xlength)
        self.FH2 = (self.FL * (par.L2 / 2 - par.d2) * math.sin(self.angle - self.theta2) - par.m2 * par.g * par.d2 * math.cos(
            self.theta2)) / ((par.d2 - par.x22) * math.sin(self.phi2 - self.theta2))
        self.RLy = -self.FL * math.sin(self.angle) - self.FH2 * math.sin(self.theta2) + par.m2 * par.g
        self.RLx = -self.FL * math.cos(self.angle) - self.FH2 * math.cos(self.theta2)
        self.FH1 = (- self.RLx * (
                par.L1 / 2 + par.d1) * math.sin(self.theta1) + self.RLy * (par.L1 / 2 + par.d1) * math.cos(
            self.theta1) + par.m1 * par.g * (par.L1 / 2) * math.cos(self.theta1)) / (
                           (par.L1 / 2 + par.x11) * math.sin(self.phi1 - self.theta1))
        self.Ry = self.FH2 * math.sin(self.phi2) - self.FH1 * math.sin(self.phi1) + self.RLy + par.m1 * par.g
        self.Rx = self.FH2 * math.cos(self.phi2) - self.FH1 * math.cos(self.phi1) + self.RLx

    def print_point(self):
        print('- - - - - - - - ')
        print('x: ' + str(self.x_ft), ', y: ' + str(self.y_ft))
        print('theta 1: ' + str(self.theta1), ', theta 2: ' + str(self.theta2))
        print('Load Force: ' + str(self.FL), ', Load Angle: ' + str(self.angle))
        print('Rx: ' + str(self.Rx), ', Ry: ' + str(self.Ry))
        print('RLx: ' + str(self.RLx), ', RLy: ' + str(self.RLy))
        print('Actuator 1 force: ' + str(self.FH1), ', Actuator 1 length: ' + str(self.actuator1_length * 12), ', Actuator 1 angle: ' + str(self.phi1))
        print('Actuator 2 force: ' + str(self.FH2), ', Actuator 2 length: ' + str(self.actuator2_length * 12), ', Actuator 2 angle: ' + str(self.phi2))
        print('- - - - - - - - ')