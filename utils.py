import pygame


def transform(image, size=None):
    image_width, image_height = image.get_size()
    size = size or pygame.display.get_surface().get_size()
    screen_size = pygame.display.get_surface().get_size()
    scale = max(size[0] / image_width, size[1] / image_height)
    new_size = (round(image_width * scale), round(image_height * scale))
    scaled_image = pygame.transform.smoothscale(image, new_size)
    bg_rect = scaled_image.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))
    return scaled_image, bg_rect
