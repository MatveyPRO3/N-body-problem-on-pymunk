import pygame
import pymunk
import pymunk.pygame_util
from Space import *
from Particle import *
import math

pygame.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)


G = 4000

clock = pygame.time.Clock()
fps = 60

space = Space(G)
space.speed = 1

main_font = pygame.font.SysFont("calibri", 15)
main_font_color = (0, 0, 0, 255)

draw_options = pymunk.pygame_util.DrawOptions(screen)

# 0 - it doesn't exist at all. 1 - it exists but with 0 mass(user haven't applied impulse yet). 2 - it exists as usual particle
user_ball_exists = 0


def main_draw(space, window, draw_options):
    window.fill(space.bg_color)

    draw_tails(particles)
    if user_ball_exists == 1:
        pygame.draw.line(screen, user_ball.color,
                         user_ball.body.position, pygame.mouse.get_pos(), 3)
    if not pygame.mouse.get_pressed()[2]:
        space.debug_draw(draw_options)
    total_impulse = list(map(round, space.total_impulse, [8, 8]))
    total_energy = round(space.total_E, 6)
    draw_text(f"Total system impulse: {total_impulse}", [20, 30])
    draw_text(f"Total system energy: {total_energy}", [20, 50])
    draw_text(f"Time: {space.speed}x", [20, 70])

    pygame.display.update()


def draw_text(txt, pos):
    screen.blit(main_font.render(txt, True, main_font_color), pos)


def draw_tails(particles):
    for p in particles:
        positions = p.body.position_history
        for i in range(len(positions[:-1])):
            pygame.draw.line(screen, p.color, positions[i], positions[i+1], 2)


def calculate_distance(p1, p2):
    return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)


def calculate_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])


def convert_coordinates_to_pg(x, y):
    return x+WIDTH/2, y+HEIGHT/2


particles = []
particles.append(Particle(space, 5, 0.5, 0.95, 0.5, [0, 0], [20,20]))
particles.append(Particle(space, 5, 0.5, 0.95, 0.5, [0, 0], [200,200]))
particles.append(Particle(space, 5, 0.5, 0.999, 0.5, [0, 0], [20,200]))
particles.append(Particle(space, 5, 0.5, 0.999, 0.5, [0, 0], [200,20]))

# R = 100
# center = 0, 0
# for angle in linspace(0, 360, 10, endpoint=False):
#     coordinates = math.cos(math.radians(angle))*R + \
#         center[0], math.sin(math.radians(angle))*R+center[1]
#     particles.append(Particle(space, 5, 0.5, 0.999, 0.5, [
#                      0, 0], convert_coordinates_to_pg(*coordinates)))


while 1:
    
    print(space.kinetic_E, space.potential_E)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit()
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            pressed_pos = pygame.mouse.get_pos()
            if user_ball_exists == 2:
                space.remove(user_ball.shape, user_ball.body)
                user_ball_exists = 0
                user_ball.position_history = []
                particles.remove(user_ball)
            elif user_ball_exists == 1:
                angle = calculate_angle(
                    pygame.mouse.get_pos(), user_ball.body.position)
                force = calculate_distance(
                    pygame.mouse.get_pos(), user_ball.body.position) * -500
                fx = math.cos(angle) * force
                fy = math.sin(angle) * force
                user_ball.body.body_type = pymunk.Body.DYNAMIC
                user_ball.body.apply_impulse_at_local_point((fx, fy))
                user_ball_exists = 2
                particles.append(user_ball)
            elif user_ball_exists == 0:
                user_ball = Particle(space, 20, 0.5, 0.999, 0.5, [
                    0, 0], pygame.mouse.get_pos())
                user_ball.body.body_type = pymunk.Body.STATIC
                user_ball.body.position = pygame.mouse.get_pos()
                user_ball_exists = 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            space.speed /= 2
            if space.speed < 0.1:
                space.speed = 0
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if space.speed == 0:
                space.speed = 0.125
            else:
                space.speed *= 2

    main_draw(space, screen, draw_options)
    dt = space.speed / fps
    space.step(dt)
    clock.tick(fps)
