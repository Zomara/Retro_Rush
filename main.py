#importing all the class libraries I coded
from tiles import * 
from spritesheet import Spritesheet
from player import Player
from box import Box
from jukebox import Jukebox
from altscreen import *
import random, time

import asyncio #library that optimizes my code for when I compile it into a wasm

#initializing the pygame screen
pygame.init()
DISPLAY_W, DISPLAY_H = 1024, 512 
window = pygame.display.set_mode(((DISPLAY_W, DISPLAY_H)))
pygame.display.set_caption("Retro Rush")

#initialzing the spritesheet with all the tile graphics
spritesheet = Spritesheet('spritesheetTilesHorizontal.png')

#creating all the map objects and adding them to a list
mapNames = ["Intro", "Pathfinding", "Caves", "Waterfall", "GraphicsV3_Scroll"]
maps = []
for name in mapNames:
    maps.append(TileMap((name+".csv"), spritesheet, mapNames.index(name)))
level = 0
map = maps[level]

#creating the canvas which I display everything on which is then framed on the sscreen
CANVAS_W, CANVAS_H = map.map_w, map.map_h
canvas = pygame.Surface((CANVAS_W, CANVAS_H))

#importing the music and sound effects
jukebox = Jukebox()
MarioDeath = pygame.mixer.Sound('MarioDeath.ogg')
Ching = pygame.mixer.Sound('Ching.ogg')

#creating all the boxes as objects that the first level uses
boxes = []
for position in map.box_positions:
    boxes.append(Box(position))

#creating the player object and setting its start point on the map
player1 = Player()
player1.position.x, player1.position.y = map.respawn_x, map.respawn_y

#openning up the world record text file and saving it as a a variable
with open('FastestTime.txt', "r") as txt:
    wr_data = txt.read()
    fastest_time = str(round(float(wr_data.split(",")[0]), 1))
    wr_holder = wr_data.split(",")[1]

#initializing the rnadom background colors and different screens
r, g, b = random.randint(10, 80), random.randint(100, 180), random.randint(100, 240)
home = HomeScreen(fastest_time, wr_holder, r, g, b)
dead = DeathScreen()
game_over = GameOverScreen(time.asctime(time.localtime()))

#~~~~~~~~~~~~~~~~~~MAIN GAME LOOP~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
async def main(): #the entire game loop is actually stored as a special function that will optimize its performance
    #I have to globalize all the variables I initialized, they can't be initialized inside of the function in order for the asyncio optimization to work
    global canvas, CANVAS_W, CANVAS_H, DISPLAY_H, DISPLAY_W, level, boxes, player1, home, dead, game_over, maps, fastest_time, map, window, r, g, b
    #some more variable initialization
    running = True
    TARGET_FPS = 60
    sign_g = 1
    sign_b = 1
    sign_r = 1
    FONT = pygame.font.SysFont("freesans", 30)
    health = 10

    
    clock = pygame.time.Clock()
    #~~~~~~~~~~~~~mini game loop that loads the home screen at 60 fps~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    while home.draw_screen(window, canvas, DISPLAY_W, DISPLAY_H):
        clock.tick(60)
        home.iteration += 1
        await asyncio.sleep(0)
    userName = ("Player-"+str(random.randint(111, 999))) if home.userName == "" else home.userName
    name_text = FONT.render(userName, 1, (255, 255, 255))


    #~~~~~~~~~~~~~~~~~~~~~~Game loop that runs the actual game playthrough~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    speedrun_start = time.time()
    while running:
        dt = clock.tick(60) * 0.001 * TARGET_FPS #creates a coefficient (delta time) that determines how far off the physics need to be corrected for a 60 fps game

        #every 3 frames the background color changes randomly
        if random.randint(0, 3) == 0: 
                r, g, b  = (r + sign_r * random.randint(0, 2), g + sign_g * random.randint(0, 2), b + sign_b * random.randint(0, 2))
                if r > 80 or r < 10:
                    sign_r = -sign_r
                    r = r + sign_r * 2
                if g > 180 or g < 100:
                    sign_g = -sign_g
                    g = g + sign_g * 2
                if b > 240 or b < 100:
                    sign_b = -sign_b
                    b = b + sign_b * 2

        #accesses the player inputs
        for event in pygame.event.get():
            #checks if the user shut down the game
            if event.type == pygame.QUIT:
                running = False

            #checks the keys the user pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player1.LEFT_KEY = True
                if event.key == pygame.K_d:
                    player1.RIGHT_KEY = True
                if event.key == pygame.K_SPACE:
                    player1.SPACE_KEY = True

            #checks the keys the user released
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player1.LEFT_KEY = False
                if event.key == pygame.K_d:
                    player1.RIGHT_KEY = False
                if event.key == pygame.K_SPACE:
                    player1.SPACE_KEY = False
                    if player1.is_jumping:
                        player1.velocity.y *= .25
                        player1.is_jumping = False

        if player1.SPACE_KEY == True:
            player1.jump()
        
        #checks if the player made it to the end of the level
        if player1.position.x > CANVAS_W:
            Ching.play()
            level += 1
            #checks if they beat the last level and the world record
            if level+1 > len(maps): #level counts from 0
                speedrun_time = time.time()-speedrun_start
                if speedrun_time < float(fastest_time):
                    #updates world record if nessesary
                    with open('FastestTime.txt', "w") as txt:
                        txt.write((str(speedrun_time) + "," + userName))
                        fastest_time = str(round(speedrun_time, 1))
                        wr_holder = userName
                level = 0
                health = 10
                speedrun_start = time.time()
            #loads in the next map and resets the players positions
            map = maps[level]
            CANVAS_W, CANVAS_H = map.map_w, map.map_h
            canvas = pygame.Surface((CANVAS_W, CANVAS_H))
            player1.position.x, player1.position.y = map.respawn_x, map.respawn_y
            #loads in the new boxes
            boxes = []
            for position in map.box_positions:
                boxes.append(Box(position))

        #formats the text that is displayed in the top left
        statistics = FONT.render("Level "+str(level+1)+" | Health: "+str(health)+" | Time: "+str(round(time.time()-speedrun_start, 1))+"  | WR: "+fastest_time, 1, (255, 255, 255))
        #checks if the player died
        if player1.death == False:
            #this code runs if the player didn't die and updates their positoin and any checkpoints they reached (the red flags)
            player1.update(dt, map.tiles, boxes, CANVAS_H)
            if player1.checkpoint == True:
                map.respawn_x, map.respawn_y = player1.position.x, player1.position.y
                player1.checkpoint = False
        else: 
            #this code runs if the player died
            #the player loses a life, the music pauses, and a sound effect plays
            health -= 1
            jukebox.mute()
            MarioDeath.play()
            #checks if the player is out of health
            if health < 1:
                #shows the game over screen
                game_over.set_death()
                while True:
                    game_over.draw_screen(window, DISPLAY_W, DISPLAY_H, userName)
                    await asyncio.sleep(0)
            else:
                #shows the "you died" screen
                dead.newMSG()
                while dead.draw_screen(window, canvas, DISPLAY_W, DISPLAY_H, (map.camera_update(player1, CANVAS_W, DISPLAY_W))):
                    clock.tick(60)
                    dead.iteration += 1
                    await asyncio.sleep(0)
                #resets the players position
                player1.position.x, player1.position.y = map.respawn_x, map.respawn_y
                player1.LEFT_KEY, player1.RIGHT_KEY, player1.SPACE_KEY = False, False, False
                player1.death = False
                jukebox.unmute()
        
        #draws the backgound, the map, the boxes, and the player
        canvas.fill((r, g, b))
        map.draw_map(canvas)
        for box in boxes:
            box.update(dt, map.tiles, boxes, player1)
            box.draw(canvas)
        player1.draw(canvas)
        #draws the canvas onto the screen at a specific location that always shows the player and doesn't show off screen
        window.blit(canvas, (map.camera_update(player1, CANVAS_W, DISPLAY_W), 0))
        #draws the text that's in the top left
        window.blit(statistics, (DISPLAY_W - 10 - statistics.get_width(), 20))
        window.blit(name_text, (20, 20))
        #updates the screen
        pygame.display.update()
        await asyncio.sleep(0)

#runs the main game loop function with the special library that optimizes its performance
asyncio.run(main())