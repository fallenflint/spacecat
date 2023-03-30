from random import randint
import time

import pygame
from pygame import math


class Animation:
    running = False

    def __call__(self, *args, **kwargs):
        return self.start(*args, **kwargs)

    def start(self):
        raise NotImplementedError(f'You must implement `{self.__class__.__name__}.start`')

    def step(self, parent):
        raise NotImplementedError(f'You must implement `{self.__class__.__name__}.step`')

    def end(self):
        raise NotImplementedError(f'You must implement `{self.__class__.__name__}.end`')

    def update(self):
        self.step()

    def step(self):
        raise NotImplementedError(f'You must implement `{self.__class__.__name__}.step`')



class SpriteAnimation(Animation):
    def update(self):
        ...


class Appear(Animation):
    def start(self):
        self.alpha = 0
        self.running = True
        self.parent.visible = True

    def step(self):
        if self.running:
            self.alpha += 10
            if self.alpha > 250:
                self.alpha = 255
                self.end()
            surface = pygame.Surface((64,64), flags=pygame.SRCALPHA)
            surface.set_alpha(min(self.alpha, 255))
            surface.blit(self.parent.image, (0,0))
            self.parent.image = surface

    def end(self):
        self.running = False


class Disappear(Animation):
    def start(self, /, *, callbacks=None):
        self.alpha = 255 
        # self.alpha = self.parent.alpha
        self.callbacks = callbacks
        self.running = True

    def step(self):
        # self.end()
        # return
        if self.running:
            self.alpha -= 10
            if self.alpha < 0:
                self.alpha = 0
                self.end()
            surface = pygame.Surface((64,64), flags=pygame.SRCALPHA)
            surface.set_alpha(max(self.alpha, 0))
            surface.blit(self.parent.image, (0,0))
            self.parent.image = surface

    def end(self):
        self.running = False
        self.parent.visible = False
        for callback in getattr(self, 'callbacks', ()):
            callback()
        self.callbacks = None


class Wiggle(Animation):
    def __init__(self, duration=1000, run_always=True):
        super().__init__()
        self.duration = duration
        self.running = run_always
        self.target_point = None
        self.previous_point = None

    def reset(self):
        self.previous_point = self.parent.rect.center
        self.target_point = (self.previous_point[0] + randint(-10, 10), self.previous_point[1] + randint(-10, 10))
        self.current_wiggle_start = time.time()

    def start(self):
        self.reset()
        self.running = True

    def step(self):
        if not self.running:
            return
        if self.parent.animations.appear.running or self.parent.animations.disappear.running:
            self.current_wiggle_start = time.time()
            return

        # if not self.previous_point:
        #     self.previous_point = self.parent.rect.center
        # if not self.target_point:
        #     self.current_wiggle_start = time.time()
        #     return
        if self.parent.rect.center == self.target_point:
            self.reset()
            return

        weight = (time.time() - self.current_wiggle_start) * 1000 / self.duration
        self.parent.rect.center = (
            math.Vector2(self.previous_point).lerp(math.Vector2(self.target_point), weight),
        )

    def end(self): 
        self.running = False


class AnimationsContainer:
    def __init__(self, target):
        self._all = getattr(target, 'animations', dict())

        for animation in self._all:
            animation.parent = target
            setattr(self, animation.__class__.__name__.lower(), animation)

    def update(self):
        for animation in self._all:
            animation.update()
