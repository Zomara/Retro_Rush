import pygame
from spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        #initializes all the varibles such as the player image, sound effects, velocity, acceleraion, checkpoints, hitboxes, direction, friction, and gravity
        pygame.sprite.Sprite.__init__(self)
        self.LEFT_KEY, self.RIGHT_KEY, self.SPACE_KEY = False, False, False
        self.is_jumping, self.on_ground = False, False
        self.gravity, self.friction = .35, -.12
        self.image = Spritesheet('spritesheetTilesHorizontal.png').parse_sprite('tile_0145.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_rect = self.mask.get_rect()
        self.rect = self.image.get_rect()
        self.position, self.velocity = pygame.math.Vector2(0,0), pygame.math.Vector2(0,0)
        self.last_direction = "Right"
        self.acceleration = pygame.math.Vector2(0,self.gravity)
        self.death = False
        self.MarioJump = pygame.mixer.Sound('MarioJump.ogg')
        self.MarioJump.set_volume(0.1)
        self.checkpoint = False

    def draw(self, display):
        #draws the player on screen making sure to face the player the right way
        if self.velocity.x > 0 or (self.last_direction == "Right" and self.velocity.x == 0):
            display.blit(pygame.transform.flip(self.image, True, False), (self.rect.x, self.rect.y))
            self.last_direction = "Right"
        elif self.velocity.x < 0 or (self.last_direction == "Left" and self.velocity.x == 0):
            display.blit(self.image, (self.rect.x, self.rect.y))
            self.last_direction = "Left"
        
    def update(self, dt, tiles, boxes, void):
        #updates the players movement and collisions
        self.horizontal_movement(dt)
        self.checkCollisionsx(tiles)
        self.vertical_movement(dt)
        self.checkCollisionsy(tiles, boxes)
        if self.position.y > void: #checks if the player fell off the map
            self.death = True

    def horizontal_movement(self,dt):
        #updates the players movement along the x axis
        self.acceleration.x = 0
        if self.LEFT_KEY:
            self.acceleration.x -= .3
        if self.RIGHT_KEY:
            self.acceleration.x += .3
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(4)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
        self.rect.x = self.position.x

    def vertical_movement(self,dt):
        #updates the players movement along the y axis
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 7: 
            self.velocity.y = 7
        self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
        self.rect.bottom = self.position.y

    def limit_velocity(self, max_vel):
        #limits the velocity to prevent infinite acceleration
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel)) #fancy max/min limits velocity in both positive and negative direction
        if abs(self.velocity.x) < .01:
            self.velocity.x = 0

    def jump(self):
        #checks if the plaeyr is able to jump, if so accelerates them upwards
        if self.on_ground:
            self.is_jumping = True
            self.velocity.y -= 8
            self.on_ground = False
            self.MarioJump.play()

    def get_hits(self, tiles):
        #retruns a list of all the tiles the player has collided with
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile) and tile.name != 'tile_0087.png' and tile.name != 'tile_0088.png':
                hits.append(tile)
        return hits

    def checkCollisionsx(self, tiles):
        #checks and updates the player to any collisions on the x axis
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if tile.name == "tile_0068.png" or tile.name == "tile_0053.png": #checks if the player is in the hitbox of a spike or water
                offset = int(tile.rect.x - self.rect.x), int(tile.rect.y - self.rect.y)
                if self.mask.overlap(tile.mask, offset): #does a pixel perfect mask collision detection to determine if the player should die
                    self.death = True
                    break
            elif self.velocity.x > 0:  # Hit tile moving right
                self.position.x = tile.rect.left - self.rect.w
                self.rect.x = self.position.x
            elif self.velocity.x < 0:  # Hit tile moving left
                self.position.x = tile.rect.right
                self.rect.x = self.position.x
            if tile.name == 'tile_0112.png':
                self.checkpoint = True

    def checkCollisionsy(self, tiles, boxes):
        #checks and updates the player to any collisions on the y axis
        self.on_ground = False
        self.rect.bottom += 1
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if tile.name == "tile_0068.png" or tile.name == "tile_0053.png": #checks if the player is in the hitbox of a spike or water
                offset = int(tile.rect.x - self.rect.x), int(tile.rect.y - self.rect.y)
                if self.mask.overlap(tile.mask, offset): #does a pixel perfect mask collision detection to determine if the player should die
                    self.death = True
                    break
            elif self.velocity.y > 0:  # Hit tile from the top
                self.on_ground = True
                self.is_jumping = False
                self.velocity.y = 0
                self.position.y = tile.rect.top
                self.rect.bottom = self.position.y
            elif self.velocity.y < 0:  # Hit tile from the bottom
                self.velocity.y = 0
                self.position.y = tile.rect.bottom + self.rect.h
            if tile.name == 'tile_0112.png':
                self.checkpoint = True
                
        self.rect.bottom += 1
        collisions = self.get_hits(boxes)
        for box in collisions:
            if self.velocity.y > 0:  # Hit box from the top
                self.velocity.y = 0
                self.position.y = box.rect.top
                self.on_ground = True
        self.rect.bottom = self.position.y