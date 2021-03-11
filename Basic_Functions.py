import Parameters as par
import pygame
import math

def pixels_to_feet(pixels):
    return (pixels * par.screen_dim_feet) / par.screen_dim


def feet_to_pixels(feet):
    return int((feet * par.screen_dim) / par.screen_dim_feet)


def draw_screen(win, renders):
    # Grid
    for gridx in range(0, par.screen_dim, feet_to_pixels(1)):
        pygame.draw.line(win, par.gray, (0, gridx), (par.screen_dim, gridx), 2)
        pygame.draw.line(win, par.gray, (gridx, 0), (gridx, par.screen_dim), 2)

    # Radius to show where min and max points can be placed
    pygame.draw.circle(win, par.black,
                       (feet_to_pixels(par.origin_x), par.screen_dim - feet_to_pixels(par.origin_height)),
                       abs(int(feet_to_pixels(par.a1 - par.a2))), 5)
    pygame.draw.circle(win, par.black,
                       (feet_to_pixels(par.origin_x), par.screen_dim - feet_to_pixels(par.origin_height)),
                       int(feet_to_pixels(par.a1 + par.a2)), 5)

    # Desired achievable positions for mechanism
    green_box_width = 1.5
    green_box_height = 2
    pygame.draw.rect(win, par.green, (feet_to_pixels(par.origin_x + par.hip_origin_positionx - green_box_width),
                                      par.screen_dim - feet_to_pixels(
                                          par.origin_height + par.hip_origin_positiony + green_box_height),
                                      feet_to_pixels(green_box_width), feet_to_pixels(green_box_height)), 3)

    for objects in renders:
        for object in objects:
            object.render(win)

    pygame.display.update()

