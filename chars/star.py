from random import randint

import pygame
from pygame import math

from sprites.animations import Appear, Disappear, Wiggle
from sprites.sprite import Sprite


class Star(Sprite):
    SPRITE_GLOB = 'media/star_animated/Star*.png'
    animations = [
        Appear(),
        Disappear(),
        Wiggle()
    ]
    # sounds = [pygame.mixer.Sound('media/bounce.flac')]

    def __init__(self, visible=True, position=None):
        super().__init__(visible=visible)

        if position is not None:
            self.rect.center = position
        else:
            self.set_random_position()
        self.bounce = pygame.mixer.Sound('media/bounce.flac')


    # def catch(self, reappear=True):
    def catch(self, callback=None):
        if self.animations.disappear.running:
            return
        def _reappear():
            self.set_random_position()
            self.animations.appear()
            self.animations.wiggle()
        callbacks = [_reappear, callback]
        self.bounce.play()
        self.animations.wiggle.end()
        # self.animations.disappear(callback = _reappear if reappear else False)
        self.animations.disappear(callbacks=callbacks)

    def set_random_position(self):
        x, y = pygame.display.get_window_size()
        self.rect.topleft = randint(40, x - 80), randint(40, y - 80)
        # self.origin = self.rect.center

        # self.animations.wiggle.reset()
        # self.previous_point = self.rect.center
        # self.target_point = None
