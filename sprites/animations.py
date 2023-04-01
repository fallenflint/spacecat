from functools import partial
import re
import pathlib
from glob import glob
from collections import OrderedDict
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
        # print(f'{self.parent.__class__.__name__}.{self.__class__.__name__}.update() for id {str(id(self))[-5:]}')
        self.step()

    @classmethod
    def get_readable_name(cls):
        return cls.__name__.lower()


class SpriteAnimation(Animation):
    INDEX_RE = re.compile(r'(\d+)')

    def __init__(
            self,
            spritesheet,
            animations=1,
            frames=None,
            names=None,
            size=None):
        if isinstance(spritesheet, list):
            self.animations = self.load_separate_sprites(
                spritesheet,
                names,
                size)
        else:
            self.animations = self.load_sprite_sheet(
                spritesheet,
                animations,
                frames,
                names,
                size)
        for name in self.animations:
            setattr(self, name, partial(self.start, name))

    def start(self, animation='idle'):
        self.current_animation = animation
        self.current_frame = 0
        self.running = True
        self.parent.visible = True

    def once(self, animation, next_animation=None, callback=None):
        self.parent.state.once = True
        if next_animation is None:
            next_animation = self.current_animation
        self.parent.state.next_animation = next_animation
        self.parent.state.callback = callback
        self.start(animation)

    def toggle(self):
        self.current_frame = 0
        keys = list(self.animations.keys())
        next_index = keys.index(self.current_animation) + 1
        if next_index > len(keys) - 1:
            next_index = 0
        self.current_animation = keys[next_index]

    def step(self):
        if self.running:
            current_animation = self.animations[self.current_animation]
            self.current_frame += 0.2
            if self.current_frame > len(current_animation) - 1:
                self.current_frame = 0
                if self.parent.state.once:
                    self.current_animation = self.parent.state.next_animation
                    self.parent.state.once = False
                    self.parent.state.next_animation = None
                    self.parent.state.callback()
                    self.parent.state.callback = None
            self.parent.image = current_animation[int(self.current_frame)]

    def end(self):
        self.running = False

    # @classmethod
    def load_sprite_sheet(cls, path, animations, frames, names, size=None):
        top_surf = pygame.image.load(path).convert_alpha()
        width, height = top_surf.get_size()
        frame_width = size[0] if size is not None else (width // frames)
        frame_height = size[1] if size is not None else (height // animations)
        assert frame_width == frame_height == 100
        sprites = OrderedDict()
        for i in range(animations):
            name = names[i] if i < len(names) else i
            sprites[name] = [
                    top_surf.subsurface(frame*frame_width, i*frame_height, frame_width, frame_height)
                    for frame in range(frames)
                ]
        cls._spritesheet = sprites
        return cls._spritesheet

    # @classmethod
    def load_separate_sprites(cls, path, name='idle', size=None):
        sprites = OrderedDict()
        sprites[name] = []
        for i, f in enumerate(path):
            path = pathlib.Path(f)
            index = cls.INDEX_RE.findall(path.name)
            if not index:
                continue
            try:
                index = int(index[0])
            except ValueError:
                print(f"Couldn't load resource: {cls.__name__} @ {f}")
                continue
            img = pygame.image.load(f).convert_alpha()
            sprites[name].append(pygame.transform.smoothscale(img, size))
        cls._spritesheet = sprites
        return cls._spritesheet

    @classmethod 
    def get_readable_name(cls):
        return 'sprites'

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
        self.callbacks = callbacks
        self.running = True

    def step(self):
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
        # print(f'{self.parent.__class__.__name__} wiggles from {self.previous_point} to {self.target_point}')

    def start(self):
        self.reset()
        self.running = True

    def step(self):
        if not self.running:
            return
        if self.parent.animations.appear.running or self.parent.animations.disappear.running:
            self.current_wiggle_start = time.time()
            return

        if self.parent.rect.center == self.target_point:
            self.reset()
            return

        weight = (time.time() - self.current_wiggle_start) * 1000 / self.duration
        self.parent.rect.center = (
            math.Vector2(self.previous_point).lerp(math.Vector2(self.target_point), weight),
        )

    def end(self):
        self.reset()
        self.running = False


class AnimationsContainer:
    def __init__(self, target):
        self._all = getattr(target, 'animations', dict())

        for animation in self._all:
            animation.parent = target
            # if isinstance(animation, SpriteAnimation):
            #     for name, subanimation in animation.animations.items():
            #         setattr(self, name, subanimation)
            # else:
            # setattr(self, animation.__class__.__name__.lower(), animation)
            setattr(self, animation.get_readable_name(), animation)

    def update(self):
        self.sprites.update()
        for animation in self._all:
            if isinstance(animation, SpriteAnimation):
                continue
            animation.update()
