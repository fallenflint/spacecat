import time
from random import randint
from glob import glob

import pygame
from pygame import math

from sprites.animations import Appear, Disappear, Wiggle, SpriteAnimation
from sprites.sprite import Sprite
from events import STAR_DISAPPEARS, STAR_DISAPPEARED

DEFAULT_STAR_LIFETIME = 3


class Star(Sprite):

    def __init__(self, lifetime=DEFAULT_STAR_LIFETIME, visible=True, position=None):
        self.animations = [
            Appear(),
            Disappear(),
            Wiggle(),
            SpriteAnimation(glob('media/star_animated/Star*.png'), names='idle', size=(64,64)),
        ]
        super().__init__(visible=visible)
        self.lifetime = lifetime

        self.bounce = pygame.mixer.Sound('media/snd/bounce.flac')

    def update(self):
        if self.disappear_time is not None:
            if time.time() >= self.disappear_time:
                pygame.event.post(pygame.event.Event(STAR_DISAPPEARS, star=self, producer = f'Star{id(self)}.update'))
        super().update()

    def catch(self, callback=None):
        if self.animations.disappear.running:
            return False
        self.bounce.play()
        self.animations.wiggle.end()
        self.animations.disappear(callbacks=[lambda: pygame.event.post(pygame.event.Event(STAR_DISAPPEARED, star=self))])
        return True

    def set_random_position(self):
        x, y = pygame.display.get_window_size()
        self.rect.topleft = randint(40, x - 80), randint(40, y - 80)

    def appear(self, position=None):
        if position is None:
            self.set_random_position()
        else:
            self.rect.center = position
        self.animations.sprites.idle()
        self.animations.wiggle()
        self.animations.appear()
        self.disappear_time = time.time() + self.lifetime + randint(0, 3000) / 1000

    def disappear(self):
        self.disappear_time = None
        self.animations.wiggle.end()
        self.animations.disappear(callbacks=[lambda: pygame.event.post(pygame.event.Event(STAR_DISAPPEARED, star=self))])