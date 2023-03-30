import pygame
from utils import transform


class BackgroundBase:
    ...
    def draw(self, surface):
        surface.blit(self.img, self.rect)


class ImageBackground(BackgroundBase):
    def __init__(self, img):
        # TODO: check for successfull loading
        self.img = pygame.image.load(img)
        self.img = self.img.convert()
        self.img, self.rect = transform(self.img)


class ShadowBackground(BackgroundBase):
    def __init__(self, opacity):
        self.opacity = opacity
        self.img = pygame.Surface(pygame.display.get_window_size(), pygame.SRCALPHA)
        self.img.set_alpha(opacity)
        self.img.fill('black')
        self.rect = self.img.get_rect()