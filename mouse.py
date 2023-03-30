import pygame.mouse


class MousePointer(pygame.sprite.Sprite):
    def update(self, event=None):
        if event is not None:
            self.rect.topleft = pygame.mouse.get_pos()
