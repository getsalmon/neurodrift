import math

import pygame


class Car:
    def __init__(self):
        self.current_position = (20, 10)
        self.angle = 0
        self.velocity = 0
        self.velocity_delta = 0
        self.angle_delta = 0

    def get_vector(self):
        return math.cos(self.angle * math.pi / 180), -math.sin(self.angle * math.pi / 180)

    def get_position(self):
        return self.current_position

    def update(self):
        self.velocity += self.velocity_delta
        self.angle += self.angle_delta
        if self.angle < 0:
            self.angle = 360 + self.angle
        if self.angle > 360:
            self.angle = self.angle - 360
        if self.velocity < 0:
            self.velocity = 0
        if self.velocity > 6:
            self.velocity = 6
        self.current_position = (
            self.current_position[0] + self.get_vector()[0] * self.velocity,
            self.current_position[1] + self.get_vector()[1] * self.velocity
        )

    def update_stat(self, velocity_delta, angle_delta):
        if velocity_delta:
            self.velocity_delta = velocity_delta
        if angle_delta:
            self.angle_delta += angle_delta
        else:
            self.angle_delta = 0


class Graphic:
    def __init__(self, field):
        self.surface_size = field
        self.surface = pygame.display.set_mode(self.surface_size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.car_surf = self.init_car_surface()
        self.font = pygame.font.SysFont('consolas', 16)
        self.car_size = 40, 20

    @staticmethod
    def init_car_surface():
        margin = 2
        brick = pygame.Surface((40, 20), pygame.SRCALPHA)
        pygame.draw.rect(brick, pygame.Color('blue'), [0, 0, 40, 20])
        pygame.draw.rect(
            brick, pygame.Color('tomato'),
            [margin, margin, 40 - 2 * margin, 20 - 2 * margin]
        )
        return brick

    def get_car_draw_pos(self, car):
        return car.get_position()[0] - self.car_size[0] / 2, car.get_position()[1] - self.car_size[1] / 2,

    def draw_debug(self, car):
        msg = f'Car\nPos:{car.get_position()}\nVelocity:{car.velocity}\nAngle:{car.angle}\nVector:{car.get_vector()}'
        parts = msg.split('\n')
        for i in range(len(parts)):
            surface = self.font.render(parts[i], True, (0xFF, 0xFF, 0xFF))
            h_margin = (len(parts) - i) * 20
            self.surface.blit(surface, (self.surface_size[0] - 500, self.surface_size[1] - h_margin))

    def redraw(self, car):
        self.surface.fill((0, 0, 0))
        surf = pygame.transform.rotate(self.car_surf, car.angle)
        self.surface.blit(surf, self.get_car_draw_pos(car))
        self.draw_debug(car)
        pygame.display.flip()


class GameLogic:
    def __init__(self, car: Car, field):
        self.car = car
        self.field = field

    def update(self):
        self.car.update()

    def update_stat(self, velocity_delta, angle_delta):
        self.car.update_stat(velocity_delta, angle_delta)


def play():
    field = (1600, 900)
    pygame.init()
    pygame.font.init()
    gr = Graphic(field)
    gl = GameLogic(Car(), field)

    vector_dict_down = {
        pygame.K_UP: (0.1, None),
        pygame.K_DOWN: (-0.1, None),
        pygame.K_LEFT: (None, 1),
        pygame.K_RIGHT: (None, -1),
    }
    vector_dict_up = {
        pygame.K_UP: (-0.1, None),
        pygame.K_LEFT: (None, None),
        pygame.K_RIGHT: (None, None),

    }
    clock = pygame.time.Clock()
    while 1:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.KEYDOWN:
                velocity_delta, angle_delta = vector_dict_down.get(e.key, (None, None))
                gl.update_stat(velocity_delta, angle_delta)
            if e.type == pygame.KEYUP:
                velocity_delta, angle_delta = vector_dict_up.get(e.key, (None, None))
                gl.update_stat(velocity_delta, angle_delta)
        gl.update()
        gr.redraw(gl.car)
        clock.tick(60)


if __name__ == '__main__':
    play()
