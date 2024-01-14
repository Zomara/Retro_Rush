import pygame

#class that just runs the music
class Jukebox:
    def __init__(self):
        #loads in the music on initialization and starts playing it in an infinite loop
        self.run = True
        self.Music = pygame.mixer.Sound('CML_Music.ogg')
        self.Music.play(loops=-1)

    def mute(self):
        self.Music.set_volume(0)

    def unmute(self):
        self.Music.set_volume(1)