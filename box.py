import pygame
from spritesheet import Spritesheet

#~~~~~~~The collisions/gravity code of the box is very similar to the player (with some important changes)~~~~~~~~~~~~~~~

#creates a box class
class Box(pygame.sprite.Sprite):
    def __init__(self, position):
        #loads in the boxes image and creates all its variables like its position, hitbox, acceleration, velocity, and gravity
        pygame.sprite.Sprite.__init__(self)
        self.on_ground = False, False
        self.gravity = .35
        self.image = Spritesheet('spritesheetTilesHorizontal.png').parse_sprite('tile_0009.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_rect = self.mask.get_rect()
        self.rect = self.image.get_rect()
        self.position, self.velocity = pygame.math.Vector2(position), pygame.math.Vector2(0,0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)
        self.name = 'box'

    #function that draws the box onto the canvas
    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))

    #updates the boxes position based off of gravity and collisions mainly
    def update(self, dt, tiles, boxes, player):
        self.horizontal_movement(player)
        self.checkCollisionsx(tiles, boxes)
        self.vertical_movement(dt)
        self.checkCollisionsy(tiles, boxes)

    #moves the box horizontal along the x axis if needed
    def horizontal_movement(self, player):
        if self.rect.colliderect(player.rect):
            if player.velocity.x > 0:
                self.position.x = player.rect.right
            elif player.velocity.x < 0:
                self.position.x = player.rect.left - self.rect.w
        self.velocity.x = player.velocity.x
        self.rect.x = self.position.x
    
    #moves the box vertically along the x axis if needed
    def vertical_movement(self, dt):
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 7: 
            self.velocity.y = 7
        self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
        self.rect.bottom = self.position.y

    #returns a list off all the tiles the box collides with
    def get_hits(self, tiles):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits

    #checks the collisions the box has made in the x axis
    def checkCollisionsx(self, tiles, boxes):
        collisions = self.get_hits(tiles)     
        for tile in collisions:
            if self.velocity.x > 0:  # Hit tile moving right
                self.position.x = tile.rect.left - self.rect.w
                self.rect.x = self.position.x
            elif self.velocity.x < 0:  # Hit tile moving left
                self.position.x = tile.rect.right
                self.rect.x = self.position.x

    #checks the collisions the box has made in the y axis
    def checkCollisionsy(self, tiles, boxes):
        self.on_ground = False
        self.rect.bottom += 1
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.y > 0:  # Hit tile from the top
                self.on_ground = True
                self.velocity.y = 0
                self.position.y = tile.rect.top
                self.rect.bottom = self.position.y
            elif self.velocity.y < 0:  # Hit tile from the bottom
                self.velocity.y = 0
                self.position.y = tile.rect.bottom + self.rect.h
                self.rect.bottom = self.position.y