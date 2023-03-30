from math import ceil
import pygame

import time


class Menu:
    parent = None

    def __init__(
            self, 
            parent,
            logo=None,
            items=None,
            caption=None,
            background=None,
            sound=None,
            item_sound=None,
            select_sound=None,
            active_effect=None
        ):
        self.parent = parent
        self.logo = logo
        self.caption = caption,
        self.visible = False
        self.active_effect = active_effect
        self.background = background
        self.sound = sound
        self.item_sound = item_sound
        if self.item_sound is not None:
            self.item_sound = pygame.mixer.Sound(self.item_sound)
        self.select_sound = select_sound
        if self.select_sound is not None:
            self.select_sound = pygame.mixer.Sound(self.select_sound)
        self.items = items

        for i, item in enumerate(self.items):
            item.menu = self
            item.index = i

    def run(self):
        if self.logo is not None:
            logo_font = pygame.freetype.Font('media/fonts/SpaceMission.otf', 150)
            self.logo, logo_rect = logo_font.render('Space Cat', 'white', pygame.Color(0,0,0,0))
            self.logo_x = self.parent.screen.get_size()[0] - logo_rect.width - 50
        self.item_font = pygame.freetype.Font('media/fonts/SpaceMission.otf', 72)

        self.current = 0
        self.item_group = pygame.sprite.Group()
        font_height = self.item_font.get_sized_glyph_height()
        for i, item in enumerate(self.items):
            item.position = (50, self.parent.screen.get_height() - font_height - (80 * (len(self.items)-i)))
            self.item_group.add(item)

        if self.sound is not None:
            self.sound = pygame.mixer.Sound(self.sound)
            self.sound.play(-1)
        self.visible = True

    def update(self, events):
        if not self.visible:
            return
        self.background.draw(self.parent.screen)
        if self.logo:
            self.parent.screen.blit(self.logo, (self.logo_x, 20))
        self.item_group.update()
        self.item_group.draw(self.parent.screen)
        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.change_selected(-1)
                if event.key == pygame.K_DOWN:
                    self.change_selected(1)
                if event.key == pygame.K_RETURN:
                    self.items[self.current].action()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.select_sound.play()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_click(event)

    def change_selected(self, value):
        self.items[self.current].color = pygame.Color('white')
        self.current += value
        if self.current < 0:
            self.current = len(self.items) + self.current
        if self.current > len(self.items) - 1:
            self.current = self.current - len(self.items)
        # self.current = pygame.math.clamp(self.current, 0, len(self.items)-1)
        # TODO: move this to general method `select(index)`
        if self.active_effect is not None:
            self.active_effect.reset()
        if self.item_sound is not None:
            self.item_sound.play()

    def stop(self):
        if self.sound is not None:
            self.sound.fadeout(200)
        self.visible = False

    def toggle_pause(self):
        self.visible ^= True
        if self.sound is not None:
            if self.sound.get_num_channels():
                self.sound.stop()
            else:
                self.sound.play(-1)

    def mouse_click(self, event):
        item_sprites = pygame.sprite.spritecollide(self.parent.mouse_pointer, self.item_group, False)
        if item_sprites:
            item_selected = item_sprites[0]
            # TODO: move this to genereal method `select(index)`
            self.current = item_selected.index
            if self.active_effect is not None:
                self.active_effect.reset()
            if self.item_sound is not None:
                self.item_sound.play()
            self.items[self.current].action()

class MenuItem(pygame.sprite.Sprite):
    def __init__(self, text, action=None, *, color='white', bg_color=pygame.Color(0,0,0,0)):
        super().__init__()
        self.text = text
        if action is None:
            action = self._noop
        self.action = action
        self.color = color
        self.bg_color = bg_color

    def _noop(sefl):
        ...

    def update(self):
        # TODO: don't render every time
        color = self.color
        if self.menu.current == self.index:
            color = pygame.Color('red')
            if self.menu.active_effect:
                self.menu.active_effect(color)
        self.image, self.rect = self.menu.item_font.render(self.text, color, self.bg_color)
        self.rect.topleft = self.position
        ...
