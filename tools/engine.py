import pygame
import glob
from pathlib import Path

import sys
sys.path.insert(0, Path('.').parent.absolute().as_posix())
from chars.cat import Cat


class EngineApplication:
    def __init__(self):
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.sprite_group = pygame.sprite.Group()
        self.cat = Cat()
        self.sprite_group.add(self.cat)
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)

    def run(self):
        while self.running or pygame.mixer.get_busy():
            time_delta = self.clock.tick(60) / 1000.
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    self.dispatch_keys(event)
                if event.type == pygame.MOUSEMOTION:
                    self.mouse_pointer.update(event)
            self.update(events)
            pygame.display.update()
        pygame.quit()

    def update(self, events):
        self.sprite_group.update()
        self.sprite_group.draw(self.screen)


if __name__ == '__main__':
    EngineApplication().run()