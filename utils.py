import math


def calc_init_vel_angle(prev_x, prev_y, new_x, new_y, vel_scale):
    """
    Calculates the initial velocity and angle given the previous coordinates and the mouse coordinates
    """
    dx = new_x - prev_x
    dy = prev_y - new_y
    magnitude = math.sqrt(dx ** 2 + dy ** 2)
    vel = magnitude * vel_scale
    theta = math.atan(dy / dx)
    if new_x < prev_x:
        vel = -vel

    return vel, theta
