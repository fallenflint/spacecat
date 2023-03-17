import pygame


def transform(image, size=None):
        image_width, image_height = image.get_size()
        size = size or Application.screen.get_size()
        screen_size = Application.screen.get_size()
        scale = max(size[0] / image_width, size[1] / image_height)
        new_size = (round(image_width * scale), round(image_height * scale))
        scaled_image = pygame.transform.smoothscale(image, new_size)
        bg_rect = scaled_image.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))
        return scaled_image, bg_rect


class Application:
    def __init__(self):
        self.time = 0
        pygame.init()
        Application.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        pygame.display.set_caption('Space cat')
        Application.running = True
        Application.clock = pygame.time.Clock()
        font = pygame.font.Font('media/fonts/SpaceMission.otf', 150)
        self.logo = font.render('Space Cat', True, 'white')
        self.logo_x = Application.screen.get_size()[0] - self.logo.get_rect().width - 50
        self.menu = {
            'items': ['Start Game', 'Settings', 'Exit'],
            'current': 0,
            'font': pygame.font.Font('media/fonts/SpaceMission.otf', 72)
        }


    def run(self):
        img = pygame.image.load('media/mainmenu.png')
        img.convert()
        self.img, self.rect = transform(img)
        self.keys = {}
        pygame.mixer.music.load('media/space.mp3')
        pygame.mixer.music.play(-1)

        while Application.running:
            time_delta = Application.clock.tick(60) / 1000.
            self.time += time_delta
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    Application.running = False
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                # if keys[pygame.K_ESCAPE]:
                #     Application.running = False
                if keys[pygame.K_UP]:
                    # self.menu['current'] = max(self.menu['current'] - 1, 0)
                    self.menu['current'] = max(self.menu['current'] - 1, 0)
                if keys[pygame.K_DOWN]:
                    self.menu['current'] = min(self.menu['current'] + 1, len(self.menu['items']) - 1)
                if keys[pygame.K_RETURN]:
                    if self.menu['current'] == len(self.menu['items'])-1:
                        Application.running = False


            self.update()
            pygame.display.update()
        pygame.quit()

    def update(self):
        self.screen.blit(self.img, self.rect)
        self.screen.blit(self.logo, (self.logo_x, 20))
        # self.menu_items = [menu_font.render(text, True, 'white') for text in ('Start Game', 'Exit')]
        for i, text in enumerate(self.menu['items']):
            color = 'white'
            if i == self.menu['current']:
                color = 'red'
            menu_item = self.menu['font'].render(text, True, color)
            self.screen.blit(
                menu_item, 
                (
                    50, 
                    Application.screen.get_size()[1] - menu_item.get_rect().height - (80 * (3-i))
                ))
