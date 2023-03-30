from sprites.sprite import Sprite


class Cat(Sprite):
    SPRITE_GLOB = 'media/cat/Cat*.png'
    animations = [
        Appear(),
        Disappear(),
        Wiggle()
    ]

    def __init__(self, visible=True, position=None):
        super().__init__(visible=visible)
        