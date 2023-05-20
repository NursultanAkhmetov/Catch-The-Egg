import pygame
import config_screens
from element_button import Button

class ChooseLevel():
    def __init__(self):
        self.level1_btn = Button(250, 170, 300, 60, "Easy Level")
        self.level2_btn = Button(250, 250, 300, 60, "Medium Level")
        self.level3_btn = Button(250, 330, 300, 60, "Hard Level")
        self.go_back_btn = Button(250, 410, 300, 60, "Go Back")
        self.buttons = [self.level1_btn, self.level2_btn, self.level3_btn, self.go_back_btn]
    
    def set(self, caption):
        if (pygame.display.Info().current_w != 800 or pygame.display.Info().current_h != 600):
            config_screens.set((800, 600))
        self.caption = caption
        pygame.display.set_caption(caption)
        if (caption == "Choose Level"):
            self.bg_image = pygame.image.load("img/bg/choose-level-bg.png")
        elif (caption == "High Scores"):
            self.bg_image = pygame.image.load("img/bg/highscores-bg.png")
	
    def run(self):
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
                    if self.level1_btn.isOver(pos):
                        if self.caption == "Choose Level":
                            config_screens.game_start.set("easy")
                            config_screens.game_start.run()
                        elif self.caption == "High Scores":
                            config_screens.highscores.set("easy")
                            config_screens.highscores.run()
                    elif self.level2_btn.isOver(pos):
                        if self.caption == "Choose Level":
                            config_screens.game_start.set("medium")
                            config_screens.game_start.run()
                        elif self.caption == "High Scores":
                            config_screens.highscores.set("medium")
                            config_screens.highscores.run()
                    elif self.level3_btn.isOver(pos):
                        if self.caption == "Choose Level":   
                            config_screens.game_start.set("hard")
                            config_screens.game_start.run()
                        elif self.caption == "High Scores":
                            config_screens.highscores.set("hard")
                            config_screens.highscores.run()
                    elif self.go_back_btn.isOver(pos):
                        config_screens.main_menu.run()

                if (event.type == pygame.MOUSEMOTION):
                    for button in self.buttons:
                        button.color = (20, 108, 148) if button.isOver(pos) else (25, 167, 206)
        
            pygame.display.update()

            config_screens.clock.tick(config_screens.fps)