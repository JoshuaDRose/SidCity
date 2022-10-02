import pygame
from pygame.locals import *


class Button(pygame.sprite.Sprite):
    def __init__(self, image, position: tuple, groups) -> None:
        super().__init__(self, groups)
        try:
            self.image = pygame.image.load(image)
        except (FileNotFoundError, pygame.error):
            print(f"Error loading file: {image}")

