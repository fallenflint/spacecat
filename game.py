from random import randint

import pygame

from chars.star import Star
from utils import transform
from scoreboard import ScoreBoard


class Game:
    background = 'media/space_bg.png'
    sound = 'media/game_st.mp3'
    MAX_SCORE = 3

    def __init__(self, app):
        self.app = app
        self.running = False
        self.visible = False
        self.sound = pygame.mixer.Sound(self.sound)
        self.channel = pygame.mixer.find_channel()
        self.moving_sprites = pygame.sprite.Group()
        self.score = 0
        self.ui = pygame.sprite.Group()
        self.scoreboard = ScoreBoard(self.get_score)
        self.ui.add(self.scoreboard)
        self.bg = pygame.image.load(self.background).convert()
        self.bg, _ = transform(self.bg, self.app.screen.get_size())

    def run(self):
        self.score = 0
        self.running = True
        self.visible = True
        self.channel.play(self.sound)

        self.stars = [Star(visible=False) for i in range(1)]
        self.moving_sprites.add(*self.stars)
        for star in self.stars:
            # star.set_random_position()
            star.animations.appear()
            star.animations.wiggle()

    def update(self, events):
        if not self.app.running:
            self.channel.stop()
        if not self.running:
            return
        self.app.screen.blit(self.bg, (0,0))
        self.moving_sprites.draw(self.app.screen)
        self.moving_sprites.update()
        self.ui.draw(self.app.screen)
        self.ui.update()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for star in pygame.sprite.spritecollide(self.app.mouse_pointer, self.moving_sprites, False):
                    if star.animations.disappear.running:
                        continue
                    star.catch(callback=self.check_score)
                    self.score += 1

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