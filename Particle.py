from dataclasses import dataclass, field
import pymunk as pm
from random import randint
import math
from pygame import Vector2


@dataclass
class Particle():
    space: pm.Space
    radius: float
    density: float
    elasticity: float
    friction: float
    start_impulse: list[float]
    pos: list[float]
    color: list = field(default_factory=list)
    position_history_max_len: int = 100

    @property
    def mass(self):
        return self.radius**2*math.pi*self.density

    def __post_init__(self):
        if not self.color:
            self.color = [randint(0, 255) for _ in range(3)]+[255]

        self.body = pm.Body()
        self.body.position = self.pos
        self.body.velocity_func = self.gravity_velocity
        self.shape = pm.Circle(self.body, self.radius)
        self.shape.mass = self.mass
        self.shape.elasticity = self.elasticity
        self.shape.friction = self.friction
        self.shape.color = self.color
        self.space.add(self.body, self.shape)
        self.body.apply_impulse_at_local_point(self.start_impulse)
        self.body.position_history = []

    def gravity_velocity(self, body, gravity, damping, dt):
        gravity = Vector2(0, 0)
        for another_body in self.space.bodies:
            # print(len(body.position_history)<=len(
            # another_body.position_history))
            if another_body is body or another_body.body_type is pm.Body.STATIC:
                continue

            if len(another_body.position_history) > len(body.position_history):
                another_body_position = another_body.position_history[-1]
            else:
                another_body_position = another_body.position

            force = self.space.G*body.mass*another_body.mass / \
                math.dist(body.position, another_body_position)**2
            angle = math.atan2(another_body_position[1]-body.position[1],
                               another_body_position[0]-body.position[0])
            acceleration = force/body.mass
            gravity += Vector2(math.cos(angle)*acceleration,
                               math.sin(angle)*acceleration)

        self.body.position_history.append(self.body.position)
        if len(self.body.position_history) > self.position_history_max_len:
            self.body.position_history.pop(0)

        pm.Body.update_velocity(body, tuple(
            gravity) if self.space.speed > 0 else (0, 0), damping, dt)
