import pymunk as pm
from math import isinf, dist, atan2


class Space(pm.Space):
    def __init__(self, G, bg_color="white", threaded: bool = False) -> None:
        self.G = G
        self.bg_color = bg_color
        super().__init__(threaded)

    @property
    def total_impulse(self):
        total_impulse = [0, 0]
        for body in self.bodies:
            if not isinf(body.mass):
                total_impulse += body.velocity*body.mass
        return total_impulse

    @property
    def total_E(self):
        return self.kinetic_E+self.potential_E

    @property
    def kinetic_E(self):
        total_kinetic_energy = 0
        for body in self.bodies:
            body_e = body.mass * \
                ((body.velocity[0]**2+body.velocity[1]**2)**0.5)**2 / 2
            total_kinetic_energy += body_e
        return total_kinetic_energy

    @property
    def potential_E(self):
        total_potential_energy = 0
        for i, body in enumerate(self.bodies):
            for body2 in self.bodies[i+1:]:
                pair_e = self.G * 100 * body.mass * body2.mass * \
                    dist(body.position, body2.position)
                total_potential_energy += pair_e
        return total_potential_energy
