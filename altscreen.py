import pygame, math, random, time

#this is the intro screen class
class HomeScreen:
    def __init__(self, wr, wr_holder, r, g, b):
        #initializes all the fonts and text and images
        self.Font = pygame.font.SysFont("freesans", 40)
        self.preview = pygame.image.load('GraphicsV3_Scroll.png')
        self.overlay = pygame.image.load('radial-gradient-gray.png')
        self.titleImage = pygame.image.load('RetroRush.png')
        self.iteration = 0
        self.r, self.g, self.b = r, g, b
        self.wr = wr
        self.text = self.Font.render("Press Enter to Start", 1, (200, 200, 200))
        self.text_shadow = self.Font.render("Press Enter to Start", 1, (0, 0, 0))
        self.text_wr = self.Font.render(("Current WR of " + wr + " Set by " + wr_holder), 1, (200, 100, 0))
        self.userName = ""

    def draw_screen(self, window, canvas, screen_w, screen_h):
        #this function is called 60 times a second, and draws everything on screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #checks if the user shut down the game
                exit()
            
            #saves the user's key imputs to be shown on screen as a username
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_RETURN:
                    return False
                elif event.key == pygame.K_BACKSPACE and len(self.userName) != '':
                    self.userName = self.userName[:-1]
                elif len(self.userName) < 40:
                    self.userName += event.unicode
        if self.userName == '':
            text_name = self.Font.render("Type in your Username", 1, (50, 50, 50))
        else:
            text_name = self.Font.render(self.userName, 1, (0, 0, 0))

        #calculates the rotation and scaling effects for some of the text using cosine functions
        self.rotate_motion = math.cos(self.iteration*0.05)*10
        self.scale_motion = math.cos(self.iteration*0.05)/10 +1, math.cos(self.iteration*0.05)/10 +1
        scaledTitle = pygame.transform.scale_by(self.titleImage, self.scale_motion)
        scaledText = pygame.transform.rotate(self.text, self.rotate_motion)
        scaledShadow = pygame.transform.rotate(self.text_shadow, self.rotate_motion)

        #draws everything onto the screen
        canvas.fill((self.r, self.g, self.b))
        canvas.blit(self.preview, (-4608 + screen_w + self.iteration*2, 0))
        canvas.blit(self.overlay, (0, 0))
        canvas.blit(scaledTitle, ((screen_w - scaledTitle.get_width())/2, (screen_h - scaledTitle.get_height())/4))
        canvas.blit(text_name, ((screen_w - text_name.get_width())/2, (screen_h - text_name.get_height())*7/16))
        canvas.blit(self.text_wr, ((screen_w - self.text_wr.get_width())/2, (screen_h - self.text_wr.get_height())*9/16))
        canvas.blit(scaledShadow, ((screen_w - scaledShadow.get_width())/2, (screen_h - scaledShadow.get_height())*3/4))
        canvas.blit(scaledText, ((screen_w - scaledText.get_width())/2 - 5, (screen_h - scaledText.get_height())*3/4 - 5))
        window.blit(canvas, (0,0))
        pygame.display.update()
        return True

#this is the screen that shows up when the player dies
class DeathScreen:
    def __init__(self):
        #initializes all the fonts and text and images
        self.Font = pygame.font.SysFont("freesans", 40)
        self.iteration = 0
        self.overlay = pygame.image.load('semi-opaque-red.png')
        self.deathMSG = ["You unalived", "You Died :(", "Try Not to Die", "Hint: Avoid Dying"]

    def newMSG(self):
        #randomizes a new death messsage
        self.text = self.Font.render(random.choice(self.deathMSG), 1, (200, 0, 0))

    def draw_screen(self, window, canvas, screen_w, screen_h, offset):
        for event in pygame.event.get(): #checks if the user shut down the game
            if event.type == pygame.QUIT:
                exit()

        if self.iteration > 180: #iteratiom increases by 1 every frame, after 3 seconds the value False is returned to end the temporary death screen
            self.iteration = 0
            return False
        
        #draws the game over text, and red overlay
        window.blit(canvas, (offset, 0))
        window.blit(self.overlay, (0, 0))
        if self.iteration%45 > 15: #makes the text on screen blink
            window.blit(self.text, ((screen_w - self.text.get_width())/2, (screen_h - self.text.get_height())/4))
        pygame.display.update()
        return True

#this is thes screen that shows up when the player loses all 10 health
class GameOverScreen:
    def __init__(self, birth):
        #saves variables for the font type, and the date the game started at
        self.Font = pygame.font.SysFont("freesans", 40)
        self.birth_date = birth
        
    def set_death(self):
        #creates a string showing the exact date and time the player started the game and ended the game
        self.death_date = time.asctime(time.localtime())
        self.text_date = self.Font.render((self.birth_date + " - " + self.death_date), 1, (255, 0, 0))

    def draw_screen(self, window, screen_w, screen_h, userName):
        #this function is called 60 times a second and draws everything onto the screen
        self.text_death = self.Font.render((userName + " Unalived Permanently"), 1, (255, 0, 0))   
        for event in pygame.event.get(): #checks if the user shut down the game
            if event.type == pygame.QUIT:
                exit()

        #draws the game_over text onto the screen
        window.blit(self.text_death, ((screen_w - self.text_death.get_width())/2, (screen_h - self.text_death.get_height())/4))
        window.blit(self.text_date, ((screen_w - self.text_date.get_width())/2, (screen_h - self.text_date.get_height())/2))
        pygame.display.update()