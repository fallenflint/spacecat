import traceback
import pygame

from menu import Menu, MenuItem
from effects import FadeAlpha
from backgrounds import ImageBackground, ShadowBackground
from game import Game
from mouse import MousePointer


class Application:

    def __init__(self):
        self.time = 0

        pygame.init()
        self.set_mouse()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        pygame.display.set_caption('Space cat')
        self.running = True
        self.clock = pygame.time.Clock()
        self.game = Game(self)
        self.main_menu = Menu(
            self,
            logo=True,
            background = ImageBackground('media/mainmenu.png'),
            sound = 'media/space.mp3',
            item_sound = 'media/menuitem.mp3',
            select_sound = 'media/menu_select.mp3',
            items = [
                MenuItem('Start game', self.start_game),
                MenuItem('Settings', ),
                MenuItem('Exit', action=self.stop),
            ],
            active_effect = FadeAlpha(from_=255, to=0, duration=400)
        )
        self.ingame_menu = Menu(
            self,
            background = ShadowBackground(opacity=128),
            caption = 'Paused',
            item_sound = 'media/menuitem.mp3',
            select_sound = 'media/menu_select.mp3',
            items = [
                MenuItem('Resume game', self.resume_game),
                MenuItem('Settings'),
                MenuItem('Exit to main menu', self.stop_game),
                MenuItem('Exit to OS', self.stop),
            ],
            active_effect = FadeAlpha(from_=255, to=0, duration=400)
        )

    def run(self, skip_menu=False):
        self.main_menu.run()

        if skip_menu:
            self.start_game()

        while self.running or pygame.mixer.get_busy():
            time_delta = self.clock.tick(60) / 1000.
            self.time += time_delta
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    self.dispatch_keys(event)
                if event.type == pygame.MOUSEMOTION:
                    self.mouse_pointer.update(event)
            self.update(events)
            pygame.display.update()
        pygame.quit()

    def update(self, events):
        try:
            self.game.update(events)
            self.main_menu.update(events)
            self.ingame_menu.update(events)
            self.mouse_pointer_group.update()
            self.mouse_pointer_group.draw(self.screen)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            traceback.print_exc()

    def start_game(self):
        self.main_menu.stop()
        self.ingame_menu.run()
        self.ingame_menu.stop()
        self.game.run()

    def stop_game(self):
        self.ingame_menu.stop()
        self.main_menu.run()
        self.game.stop()

    def resume_game(self):
        self.ingame_menu.stop()
        self.game.toggle_pause()

    def dispatch_keys(self, event):
        if event.key == pygame.K_ESCAPE:
            self.game.toggle_pause()
            self.ingame_menu.toggle_pause()

    def stop(self):
        pygame.mixer.fadeout(300)
        self.game.stop()
        self.running = False

    def set_mouse(self):
        mouse_surf = pygame.image.load('media/cursor.cur')
        mouse_surf = pygame.transform.smoothscale_by(mouse_surf, 2)
        pygame.mouse.set_visible(False)
        self.mouse_pointer_group = pygame.sprite.Group()
        self.mouse_pointer = MousePointer()
        self.mouse_pointer.image = mouse_surf
        self.mouse_pointer.rect = mouse_surf.get_rect()
        self.mouse_pointer_group.add(self.mouse_pointer)

