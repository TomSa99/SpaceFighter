import pygame
import sys

from button import Button
from models2 import Spaceship, Spaceship2
from utils2 import load_sprite, print_text


class SpaceFighter:

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.background = pygame.transform.scale(load_sprite('space2', False), self.screen.get_size())
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ''

        self.bullets = []
        self.bullets2 = []
        self.spaceship = Spaceship((self.screen.get_size()[0] - 100, self.screen.get_size()[1] / 2),
                                   self.bullets.append)
        self.spaceship2 = Spaceship2((100, self.screen.get_size()[1] / 2), self.bullets2.append)

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self) -> None:
        pygame.init()
        pygame.display.set_caption("Space Fighter")

    def _handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                main()

            elif (
                    self.spaceship
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_SPACE
            ):
                self.spaceship.shoot()

            elif (
                    self.spaceship2
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_q
            ):
                self.spaceship2.shoot()

        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            # if the spaceship is not None
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()
            elif is_key_pressed[pygame.K_DOWN]:
                self.spaceship.deaccelerate()

        if self.spaceship2:
            # if the spaceship is not None
            if is_key_pressed[pygame.K_d]:
                self.spaceship2.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_a]:
                self.spaceship2.rotate(clockwise=False)
            if is_key_pressed[pygame.K_w]:
                self.spaceship2.accelerate()
            elif is_key_pressed[pygame.K_s]:
                self.spaceship2.deaccelerate()
    def get_game_objects(self):
        game_objects = [*self.bullets, *self.bullets2]

        if self.spaceship:
            game_objects.append(self.spaceship)

        if self.spaceship2:
            game_objects.append(self.spaceship2)

        return game_objects

    def _process_game_logic(self):
        for game_object in self.get_game_objects():
            game_object.move(self.screen)

        # If both spaceships collide, the game is over
        if self.spaceship and self.spaceship2:
            if self.spaceship.collides_with(self.spaceship2):
                self.spaceship = None
                self.spaceship2 = None

        # when the bullet from the spaceship collides with the spaceship2, the spaceship2 is destroyed
        for bullet in self.bullets[:]:
            if bullet.collides_with(self.spaceship2):
                self.bullets.remove(bullet)
                self.spaceship2 = None
                break

        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        # when the bullet from the spaceship2 collides with the spaceship, the spaceship is destroyed
        for bullet2 in self.bullets2[:]:
            if bullet2.collides_with(self.spaceship):
                self.bullets2.remove(bullet2)
                self.spaceship = None
                break

        for bullet2 in self.bullets2[:]:
            if not self.screen.get_rect().collidepoint(bullet2.position):
                self.bullets2.remove(bullet2)

        if not self.spaceship2 and self.spaceship:
            self.message = 'Player1 won!'
        elif not self.spaceship and self.spaceship2:
            self.message = 'Player2 won!'
        elif not self.spaceship and not self.spaceship2:
            self.message = 'Game Over!'

    def _draw(self):
        self.screen.blit(self.background, (0, 0))

        for game_object in self.get_game_objects():
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)  # (surface, message, font) font will be default

        pygame.display.flip()
        self.clock.tick(60)

def main():
    game = SpaceFighter()
    game.main_loop()

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    background = pygame.transform.scale(load_sprite('space2', False), screen.get_size())

    SCREEN = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Menu")

    def get_font(size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("assets/sprites/font.ttf", size)

    while True:
        SCREEN.blit(background, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(90).render("SPACE FIGHTER", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/sprites/play_rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        QUIT_BUTTON = Button(image=pygame.image.load("assets/sprites/quit_rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main()

                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
