import pygame


class ScoreBoard(pygame.sprite.Sprite):
    def __init__(self, get_score):
        super().__init__()
        self.get_score = get_score
        self.font = pygame.freetype.Font('media/fonts/SpaceMission.otf', 40)
        self.update()

    def update(self):
        self.image, self.rect = self.font.render(str(self.get_score()), pygame.Color(255,255,255, 200), (0,0,0,0))
        self.rect.centerx = pygame.display.get_window_size()[0] // 2
        self.rect.y = 20

