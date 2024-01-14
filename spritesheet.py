import pygame
import json #library to read/access json files

class Spritesheet:
    def __init__(self, filename):
        #loads in the json file and spritesheet
        #the json file has all the coordinates of all the smaller images in the spritesheet
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.meta_data = self.filename.replace("png", "json")
        with open(self.meta_data) as f:
            self.data = json.load(f)

    #function that cuts out a smaller image from the spritesheet image
    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

    #function that returns the image of the parsed name
    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h, = sprite['x'], sprite['y'], sprite['w'], sprite['h']
        image = self.get_sprite(x, y, w, h)
        return image