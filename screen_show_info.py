import pygame
import config_screens
from element_button import Button

class ShowInfo():
    def __init__(self):
        self.go_back_btn = Button(25, 520, 300, 60, "Go Back")
        
    def set(self, caption, path):
        if (pygame.display.Info().current_w != 800 or pygame.display.Info().current_h != 600):
            config_screens.set((800, 600))
        pygame.display.set_caption(caption)
        self.bg_image = pygame.image.load(path)

    def run(self):
        while (True):
            config_screens.screen.blit(self.bg_image, (0, 0))
		
            self.go_back_btn.draw(config_screens.screen)

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

                if (event.type == pygame.QUIT):
                    pygame.quit();
                    exit(0)

                if (event.type == pygame.MOUSEBUTTONDOWN):
                    if self.go_back_btn.isOver(pos):
                        config_screens.main_menu.run()

                if (event.type == pygame.MOUSEMOTION):
                    self.go_back_btn.color = (20, 108, 148) if self.go_back_btn.isOver(pos) else (25, 167, 206)

            pygame.display.update()

            config_screens.clock.tick(config_screens.fps)