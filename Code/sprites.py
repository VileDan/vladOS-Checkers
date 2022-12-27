import pygame


class Checker(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.small_image = pygame.image.load(filename).convert_alpha()
        self.size = self.small_image.get_size()
        self.image = pygame.transform.scale(self.small_image, (int(self.size[0] * 4), int(self.size[1] * 4)))
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y
    def update(self, *args):
        self.rect.x = self.x
        self.rect.y = self.y

class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.size = self.image.get_size()
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0] * 4), int(self.size[1] * 4)))