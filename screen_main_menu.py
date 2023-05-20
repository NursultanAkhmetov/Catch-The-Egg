import pygame
import config_screens
from element_button import Button

class MainMenu():
    def __init__(self):
        pygame.mixer.music.load("audio/back.wav")
        pygame.mixer.music.play(-1)

        self.bg_image = pygame.image.load("img/bg/main-bg.png")
        self.play_btn = Button(250, 170, 300, 60, "Play")
        self.how_to_play_btn = Button(250, 250, 300, 60, "How To Play")
        self.highscores_btn = Button(250, 330, 300, 60, "High Scores")
        self.about_btn = Button(250, 410, 300, 60, "About The Game")
        self.quit_btn = Button(250, 490, 300, 60, "Quit")
        self.buttons = [self.play_btn, self.how_to_play_btn, self.highscores_btn, self.about_btn, self.quit_btn]

    def run(self):
        pygame.display.set_caption("Main Menu")
        if (pygame.display.Info().current_w != 800 or pygame.display.Info().current_h != 600):
            config_screens.set((800, 600))
        while (True):
            config_screens.screen.blit(self.bg_image, (0, 0))
            
            for button in self.buttons:
                button.draw(config_screens.screen)

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

                if (event.type == pygame.QUIT):
                    pygame.quit()
                    exit(0)

                if (event.type == pygame.MOUSEBUTTONDOWN):
                    if self.play_btn.isOver(pos):
                        config_screens.choose_level.set("Choose Level")
                        config_screens.choose_level.run()
                    elif self.how_to_play_btn.isOver(pos):
                        config_screens.show_info.set("How To Play", "img/bg/how-to-play-bg.png")
                        config_screens.show_info.run()
                    elif self.highscores_btn.isOver(pos):
                        config_screens.choose_level.set("High Scores")
                        config_screens.choose_level.run()
                    elif self.about_btn.isOver(pos):
                        config_screens.show_info.set("About The Game", "img/bg/about-bg.png")
                        config_screens.show_info.run()
                    elif self.quit_btn.isOver(pos):
                        pygame.quit()
                        exit(0)

                if (event.type == pygame.MOUSEMOTION):
                    for button in self.buttons:
                        button.color = (20, 108, 148) if button.isOver(pos) else (25, 167, 206)

            pygame.display.update()

            config_screens.clock.tick(config_screens.fps)