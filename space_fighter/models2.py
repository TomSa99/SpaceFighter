import pygame
from pygame.math import Vector2
from pygame.transform import rotozoom

from utils2 import load_sprite, load_sound, wrap_position, get_random_velocity


class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


UP = Vector2(0, -1)


class Spaceship(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.1
    DEACCCELERATION = -0.1
    BULLET_SPEED = 3

    def __init__(self, position, create_bullet_callback):
        self.direction = Vector2(UP)
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")

        img = load_sprite('ship_green')
        img = pygame.transform.scale(img, (50, 50))

        super().__init__(position, img, Vector2(0))
        # these are the arguments for the GameObject class

    def rotate(self, clockwise=True):
        rotation_direction = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * rotation_direction
        self.direction.rotate_ip(angle)

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION
        # this is the maximum speed of the spaceship
        if self.velocity.length() > 3:
            self.velocity.scale_to_length(3)

    def deaccelerate(self):
        self.velocity += self.direction * self.DEACCCELERATION
        if self.velocity.length() > 3:
            self.velocity.scale_to_length(3)

    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)


class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite('bullet'), velocity)

    def move(self, surface):
        self.position += self.velocity


class Spaceship2(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.1
    DEACCCELERATION = -0.1
    BULLET_SPEED = 3

    def __init__(self, position, create_bullet_callback):
        self.direction = Vector2(UP)
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")

        img = load_sprite('ship_red')
        img = pygame.transform.scale(img, (50, 50))

        super().__init__(position, img, Vector2(0))
        # these are the arguments for the GameObject class

    def rotate(self, clockwise=True):
        rotation_direction = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * rotation_direction
        self.direction.rotate_ip(angle)

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION
        if self.velocity.length() > 3:
            self.velocity.scale_to_length(3)

    def deaccelerate(self):
        self.velocity += self.direction * self.DEACCCELERATION
        if self.velocity.length() > 3:
            self.velocity.scale_to_length(3)

    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet2 = Bullet2(self.position, bullet_velocity)
        self.create_bullet_callback(bullet2)
        self.laser_sound.play()

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)


class Bullet2(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite('bullet'), velocity)

    def move(self, surface):
        self.position += self.velocity


class Asteroid(GameObject):
    def __init__(self, position):
        super().__init__(position, load_sprite('Asteroid'), get_random_velocity(1,3))