from random import randint

import pygame

from utils import transform
from scoreboard import ScoreBoard
from events import STAR_APPEARS, STAR_DISAPPEARS, STAR_DISAPPEARED, STAR_CAUGHT, CAT_DELIVERED, CAT_STABBED
from utils import log


PRINT = pygame.event.custom_type()

class Game:
    background = 'media/space_bg.png'
    sound = 'media/game_st.mp3'
    MAX_SCORE = 5
    STARS_ON_SCREEN = 3

    def __init__(self, app):
        self.app = app
        self.running = False
        self.visible = False
        self.sound = pygame.mixer.Sound(self.sound)
        self.sound.set_volume(0.5)
        self.channel = pygame.mixer.find_channel()
        self.moving_sprites = pygame.sprite.Group()
        self.score = 0
        self.ui = pygame.sprite.Group()
        self.scoreboard = ScoreBoard(self.get_score)
        self.ui.add(self.scoreboard)
        self.bg = pygame.image.load(self.background).convert()
        self.bg, _ = transform(self.bg, self.app.screen.get_size())


    def run(self):
        from chars.star import Star
        from chars.cat import Cat
        self.score = 0
        self.running = True
        self.visible = True
        self.channel.play(self.sound)

        self.stars = [Star(visible=False) for i in range(self.STARS_ON_SCREEN)]
        self.cat = Cat()
        self.cat.rect.center = (100, 100)
        self.moving_sprites.add(self.cat)
        self.star_group = pygame.sprite.Group()
        self.cat.animations.appear()
        self.cat.animations.sprites.idle()
        self.cat.animations.wiggle()
        for star in self.stars:
            pygame.event.post(
                pygame.event.Event(STAR_APPEARS, {'star': star}),
            )
        
    def update(self, events):
        if not self.app.running:
            self.channel.stop()
        if not self.running:
            return
        self.app.screen.blit(self.bg, (0,0))
        self.star_group.draw(self.app.screen)
        self.star_group.update()
        self.moving_sprites.draw(self.app.screen)
        self.moving_sprites.update()
        self.ui.draw(self.app.screen)
        self.ui.update()

        if self.visible:
            for event in events:
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_SPACE:
                #         self.cat.animations.sprites.toggle()
                #     if event.key == pygame.K_RETURN:
                #         self.cat.animations.sprites.once('catch')
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.cat.move(event.pos)
                if event.type == STAR_APPEARS:
                    self.put_star(event.star)
                if event.type == STAR_DISAPPEARS:
                    self.hide_star(event.star)
                if event.type == STAR_DISAPPEARED:
                    self.put_star(event.star)
                if event.type == STAR_CAUGHT:
                    self.catch_star(event)
                if event.type == CAT_DELIVERED:
                    self.try_catch()
                if event.type == CAT_STABBED:
                    self.stabbed()

    def try_catch(self):
        stars = pygame.sprite.spritecollide(self.cat, self.star_group, False)
        if not stars:
            self.cat.animations.wiggle()
            return
        self.cat.stab()

    def stabbed(self):
        stars = pygame.sprite.spritecollide(self.cat, self.star_group, False)
        for star in stars:
            if star.catch():
                self.score += 1
        if not stars:
            self.cat.missed()
        self.check_score()

    def toggle_pause(self):
        self.visible ^= True
        if self.visible:
            self.channel.unpause()
        else:
            self.channel.pause()

    def stop(self):
        self.visible = False
        self.running = False
        self.moving_sprites.empty()
        self.channel.fadeout(300)

    def get_score(self):
        return self.score

    def check_score(self):
        if self.score == self.MAX_SCORE:
            self.app.stop_game()

    def put_star(self, star):
        self.star_group.add(star)
        star.appear()

    def hide_star(self, star):
        star.disappear()
