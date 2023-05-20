import pygame
import config_screens
from element_text_box import TextBox
from element_button import Button
from google_sheets_API import GoogleSheetsAPI

class Highscores():
    def __init__(self):
        self.color_header = (20, 108, 148)
        self.color = (175, 211, 226)
        self.outline_header = (20, 108, 148)
        self.outline = (25, 167, 206)
        self.width_col1 = 300
        self.width_col2 = 200
        self.height = 60
        self.font_size = 35
        self.col1_x = 250
        self.col2_x = 550
        self.y = [150, 210, 270, 330, 390, 450]

        self.go_back_btn = Button(250, 530, 200, 60, "Go Back")
        self.play_btn = Button(550, 530, 200, 60, "Play")

    def set(self, level):
        self.level = level
        if (pygame.display.Info().current_w != 800 or pygame.display.Info().current_h != 600):
            config_screens.set((800, 600))
        pygame.display.set_caption("High Scores")
        self.bg_image = pygame.image.load("img/bg/highscores-bg2-" + self.level + ".png")
        self.googleSheetsAPI = GoogleSheetsAPI()
        values = self.googleSheetsAPI.get_values_for_highscores(self.level)
        
        self.text_col1 = ["Nickname"]
        self.text_col2 = ["Score"]
        for i in range(5):
            self.text_col1.append(values[i][1])
            self.text_col2.append(values[i][2])

    def run(self):
        while (True):
            config_screens.screen.blit(self.bg_image, (0, 0))

            textBoxCol1 = TextBox(self.color_header, self.outline_header, self.col1_x, self.y[0], self.width_col1, self.height, self.font_size, self.text_col1[0])
            textBoxCol1.draw(config_screens.screen)
            textBoxCol2 = TextBox(self.color_header, self.outline_header, self.col2_x, self.y[0], self.width_col2, self.height, self.font_size, self.text_col2[0])
            textBoxCol2.draw(config_screens.screen)

            for i in range(1, 6):
                textBoxCol1 = TextBox(self.color, self.outline, self.col1_x, self.y[i], self.width_col1, self.height, self.font_size, self.text_col1[i])
                textBoxCol1.draw(config_screens.screen)
                textBoxCol2 = TextBox(self.color, self.outline, self.col2_x, self.y[i], self.width_col2, self.height, self.font_size, str("{:.2f}".format(float(self.text_col2[i])/100)))
                textBoxCol2.draw(config_screens.screen)

            self.go_back_btn.draw(config_screens.screen)
            self.play_btn.draw(config_screens.screen)

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

                if (event.type == pygame.QUIT):
                    pygame.quit()
                    exit(0)

                if (event.type == pygame.MOUSEBUTTONDOWN):
                    if self.go_back_btn.isOver(pos):
                        config_screens.choose_level.set("High Scores")
                        config_screens.choose_level.run()
                    if self.play_btn.isOver(pos):
                        config_screens.game_start.set(self.level)
                        config_screens.game_start.run()

                if (event.type == pygame.MOUSEMOTION):
                    self.go_back_btn.color = (20, 108, 148) if self.go_back_btn.isOver(pos) else (25, 167, 206)

            pygame.display.update()

            config_screens.clock.tick(config_screens.fps)