import glob
import pathlib
import re

import pygame as pg

from .animations import Animation, AnimationsContainer, SpriteAnimation
from chars.state import State


class Animated:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.animations = AnimationsContainer(self)
        self.image = self.animations.sprites._spritesheet['idle'][0]
        self.rect = self.image.get_rect()
        self.state = State()
        
    def update(self):
        self.animations.update()



class Voicy:
    def __init__(self, *args, **kwargs):
        for sound in getattr(self, 'sounds', []):
            ...


class Sprite(Animated, Voicy, pg.sprite.Sprite):
    
    def __init__(self, visible=True):
        pg.sprite.Sprite.__init__(self)
        super().__init__()
        self.visible = visible

    def update(self):
        if not self.visible:
            return
        pg.sprite.Sprite.update(self)
        super().update()

