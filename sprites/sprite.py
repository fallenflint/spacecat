import glob
import pathlib
import re

import pygame as pg

from .animations import Animation, AnimationsContainer


class Animated:
    def __init__(self, *args, **kwargs):
        self.animations = AnimationsContainer(self)
        
    def update(self):
        self.animations.update()


class Voicy:
    def __init__(self, *args, **kwargs):
        for sound in getattr(self, 'sounds', []):
            ...


class Sprite(Animated, Voicy, pg.sprite.Sprite):
    INDEX_RE = re.compile(r'(\d+)')
    SPRITE_SIZE = (64, 64)
    
    def __init__(self, visible=True):
        pg.sprite.Sprite.__init__(self)
        super().__init__()

        if not hasattr(self.__class__, '_sprites'):
            setattr(self.__class__, '_sprites', list((i[1] for i in sorted(self.load_sprites()))))
        self.sprites = self.__class__._sprites

        self.current = 0
        self.image = self.sprites[self.current]
        self.rect = self.image.get_rect()

        self.visible = visible

    def load_sprites(self):
        for f in glob.glob(self.SPRITE_GLOB):
            path = pathlib.Path(f)
            index = self.INDEX_RE.findall(path.name)
            if not index:
                continue
            try:
                index = int(index[0])
            except ValueError:
                print(f"Couldn't load resource: {self.__class__.__name__} @ {f}")
                continue
            img = pg.image.load(f).convert_alpha()
            yield (index, pg.transform.smoothscale(img, self.SPRITE_SIZE))

    def update(self):
        if not self.visible:
            return
        self.current += 0.2
        if self.current > len(self.sprites) - 1:
            self.current = 0
        self.image = self.sprites[int(self.current)]
        pg.sprite.Sprite.update(self)
        super().update()

