import pygame, csv
#csv library used to read csv files

class Tile(pygame.sprite.Sprite):
    #each individual tile on screen is its own object
    def __init__(self, image, x, y, spritesheet):
        #sets all the varibles like the tiles size, image, name, and hitbox
        pygame.sprite.Sprite.__init__(self)
        self.name = image
        self.image = spritesheet.parse_sprite(image)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        #draws the tile onto a canvas
        surface.blit(self.image, (self.rect.x, self.rect.y))

#each level has its own map, each map is compiled into 1 image
class TileMap():
    def __init__(self, filename, spritesheet, level):
        #sets the variables like the players spawn point, level number, camera offset, text font
        self.tile_size = 18
        self.respawn_x, self.respawn_y = 0, 0
        self.camera_x_offset = 0
        self.spritesheet = spritesheet
        self.box_positions = []
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.FONT = pygame.font.SysFont("calibri", 30)
        self.info_text = self.FONT.render("SpaceBar: Jump | A: Move Left | D: Move Right", 1, (255, 255, 255))
        self.level = level
        self.load_map() #calls a function to compile map into 1 image

    def draw_map(self, surface):
        #function that draws the map onto the screen
        surface.blit(self.map_surface, (0, 0))
        if self.level == 0: #only draws the tutorial text on level 1
            surface.blit(self.info_text, (160, 450))

    def load_map(self):
        #draws all the tile onto 1 surface
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def read_csv(self, filename):
        #takes a comma seperated value (csv) file and returns it as a list of lists
        map = []
        with open(filename) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map 

    def load_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)
        x, y = 0, 0
        for row in map:
            x = 0
            #for every value in the csv file, turns the number into a corresponding image
            for tile in row:
                if tile == '145': #player tile
                    #sets respawn poin to that tiles coordinates
                    self.respawn_x, self.respawn_y = x * self.tile_size, y * self.tile_size
                    self.camera_x_offset = x * self.tile_size
                elif tile == '9': #box tile
                    #sets a box to be created at the tile coordinates 
                    self.box_positions.append((x * self.tile_size, y * self.tile_size))
                elif tile != '-1': #values of -1 are empty space
                    #converts a number into an image to be parsed to spritsheet.py which was initialized in the main code branch
                    if len(tile) == 3:
                        tiles.append(Tile('tile_0' + tile + '.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    elif len(tile) == 2:
                        tiles.append(Tile('tile_00' + tile + '.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    elif len(tile) == 1:
                        tiles.append(Tile('tile_000' + tile + '.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                # Move to next tile in current row
                x += 1

            # Move to next row
            y += 1
        # Store the size of the tile map
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles
    
    def camera_update(self, player, CANVAS_W, DISPLAY_W):
        #offsets the canvas from the screen so that the map scrolls and is always on screen
        if player.position.x > CANVAS_W + self.camera_x_offset - DISPLAY_W:
            return -(CANVAS_W - DISPLAY_W)
        elif player.position.x < self.camera_x_offset:
            return 0
        else:
            return self.camera_x_offset - player.position.x