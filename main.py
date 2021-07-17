import sys
import pygame
from constants import *
from utils import *


pygame.init()
pygame.font.init()
font = pygame.font.Font('arial.ttf', 20)

clock = pygame.time.Clock()

window = pygame.display.set_mode([WIN_WIDTH, WIN_HEIGHT])
pygame.display.set_caption('Projectile Motion')
background_image = pygame.image.load('bg.png').convert()


class Ball:
    def __init__(self, g):
        self.radius = 10
        self.x = 10 + self.radius
        self.y = REST_Y - self.radius
        self.colour = BALL_COL
        self.vel_x = 0
        self.vel_y = 0
        self.vel = 0
        self.last_bounce_time = 0
        self.positions = [(self.x, self.y), (self.x, self.y)]  # must have at least 2 positions to work
        self.distance = 0
        self.time = 0
        self.g = g
        self.theta = 0

    def draw(self):
        pygame.draw.circle(window, self.colour, (self.x, self.y), self.radius)
        if DRAW_PATH:
            pygame.draw.lines(window, self.colour, False, self.positions)

    def launch(self, init_vel, angle):
        self.y = REST_Y - self.radius
        self.vel_x = init_vel * math.cos(angle)
        self.vel_y = init_vel * math.sin(angle)

    def stop_or_rebound(self):
        """
        If the time since the last bounce is below a certain value, the ball is stopped. Else, it rebounds with less
        velocity in both components.
        """
        if pygame.time.get_ticks() - self.last_bounce_time < STOPPING_LIM and self.last_bounce_time != 0:
            self.y = REST_Y - self.radius
            self.vel_x = 0
            self.vel_y = 0
            self.vel = 0
        else:
            self.vel_y = -self.vel_y * REBOUND_SCALE
            self.vel_x *= REBOUND_SCALE

    def check_if_hit_top_or_bottom(self):
        if self.y >= REST_Y - self.radius:
            # stops ball getting stuck
            self.y = REST_Y - 10
            # stops the ball if time since last bounce is very small
            self.stop_or_rebound()
            self.last_bounce_time = pygame.time.get_ticks()
        elif self.y <= 0 + self.radius:
            self.y = 10
            self.stop_or_rebound()

    def check_if_hit_side(self):
        if self.x <= 0 + self.radius:
            self.x = 10
            self.vel_x = -self.vel_x * REBOUND_SCALE
        elif self.x >= WIN_WIDTH - self.radius:
            self.x = WIN_WIDTH - 10
            self.vel_x = -self.vel_x * REBOUND_SCALE

    def update_vel_angle(self):
        self.theta = math.atan(self.vel_y / self.vel_x)
        self.vel = math.sqrt(ball.vel_x ** 2 + ball.vel_y ** 2)
        # ensures direction is kept
        if self.vel_x < 0:
            self.vel = -self.vel

    def update_vel_components(self):
        self.vel_y = self.vel * math.sin(self.theta)
        self.vel_x = self.vel * math.cos(self.theta)

    def move(self):
        # updates the instantaneous velocity and angle to the horizontal
        self.update_vel_angle()

        # drag deceleration
        self.vel -= self.vel * DRAG_COEF

        # updates x and y velocities
        self.update_vel_components()

        # gravitational acceleration
        self.vel_y -= ball.g * VEL_SCALE

        # stores positions so path can be drawn
        self.positions.append((self.x, self.y))

        # updates positions
        self.x += self.vel_x
        self.y -= self.vel_y

        # updates distance and time moved
        self.distance += abs(self.vel_x * TIME_SCALE)
        self.time += TIME_SCALE


def redraw():
    if USE_IMAGE:
        window.blit(background_image, [0, 0])
    else:
        window.fill(BG_COL)

    # draws ball
    ball.draw()

    # removes tail/path as it moves after a certain period
    if len(ball.positions) > 2:
        if time_since_stationary > 2500:
            ball.positions.pop(0)

    # text
    vel_x_text = font.render(f'X velocity / ms^-1 = {str(round(ball.vel_x, DATA_PRECISION))}', True, BLACK)
    vel_y_text = font.render(f'Y velocity / ms^-1 = {str(round(ball.vel_y, DATA_PRECISION))}', True, BLACK)
    vel_text = font.render(f'Net velocity / ms^-1 = {str(abs(round(ball.vel, DATA_PRECISION)))}', True, BLACK)
    kinetic_energy = round(.5 * 1 * ball.vel**2, 2)
    kinetic_energy_text = font.render(f'Kinetic energy / J = {str(round(kinetic_energy, DATA_PRECISION))}', True, BLACK)
    distance_text = font.render(f'Distance / m = {str(round(ball.distance, DATA_PRECISION))}', True, BLACK)
    time_text = font.render(f'Time / s = {str(round(ball.time, DATA_PRECISION))}', True, BLACK)
    window.blit(vel_x_text, (20, 20))
    window.blit(vel_y_text, (20, 50))
    window.blit(vel_text, (20, 80))
    window.blit(kinetic_energy_text, (20, 110))
    window.blit(distance_text, (20, 140))
    window.blit(time_text, (20, 170))

    # refreshes screen
    pygame.display.flip()


if __name__ == '__main__':
    ball = Ball(FIELD_STRENGTH)
    moving = False
    time_since_stationary = 0
    time_fired = 0

    while True:
        clock.tick(FPS)

        # gradually removes tail after stopping
        if not moving:
            if len(ball.positions) > 2:
                ball.positions.pop(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and moving is False:
                new_x, new_y = pygame.mouse.get_pos()
                vel, theta = calc_init_vel_angle(ball.x, ball.y, new_x, new_y, VEL_SCALE)
                ball.launch(vel, theta)
                time_fired = pygame.time.get_ticks()
                moving = True

        if moving:
            time_since_stationary = pygame.time.get_ticks() - time_fired
            ball.move()
            ball.check_if_hit_side()
            ball.check_if_hit_top_or_bottom()

            # checks if stopped
            if ball.vel_x == 0 and ball.vel_y == 0:
                moving = False
                time_since_stationary = 0

        redraw()
