from sprites.sprite import Sprite
from sprites.animations import Appear, Disappear, Wiggle, SpriteAnimation

import pygame
from pygame import math

import events


class Cat(Sprite):
    animations = [
        Appear(),
        Disappear(),
        Wiggle(),
        SpriteAnimation('media/cat/cat.png', animations=2, frames=10, names=('idle', 'catch'), size=(100, 100)),
    ]

    def __init__(self, visible=True, position=None):
        super().__init__(visible=visible)
        self.flying = pygame.mixer.Sound('media/snd/flying2.mp3')
        self.dammit = pygame.mixer.Sound('media/snd/dammit1.mp3')
        self.flying.set_volume(1)

    def move(self, target, callback=None):
        self.animations.wiggle.end()
        self.flying.play()
        self.state.moving = True
        self.state.target = target
        self.move_callback = callback

    def stop(self):
        self.state.moving = False
        self.state.target = None
        if self.move_callback is not None:
            self.move_callback()
            self.move_callback = None
        self.flying.fadeout(300)
        pygame.event.post(pygame.event.Event(events.CAT_DELIVERED, cat=self))
        self.animations.wiggle()

    def stab(self):
        self.animations.sprites.once('catch', callback=lambda: pygame.event.post(pygame.event.Event(events.CAT_STABBED)))

    def update(self):
        if self.state.moving:
            self.rect.topleft = math.Vector2(self.rect.topleft).move_towards(self.state.target, 10)
            if self.rect.topleft == self.state.target:
                self.stop()
        super().update()

    def missed(self):
        self.dammit.play()