import pygame
import config_screens
from element_button import Button

class GameOver():
	def __init__(self):
		self.restart_button = Button(25, 520, 300, 60, "Play Again")
		self.choose_level = Button(475, 520, 300, 60, "Choose Level")

	def set(self, level):
		self.level = level
		if (pygame.display.Info().current_w != 800 or pygame.display.Info().current_h != 600):
			config_screens.set((800, 600))
		pygame.display.set_caption("Gave Over")
		self.bg_image = pygame.image.load("img/bg/game-over-bg.png")
	
	def run(self):
		while (True):
			config_screens.screen.blit(self.bg_image, (0, 0))

			self.restart_button.draw(config_screens.screen)
			self.choose_level.draw(config_screens.screen)
			
			for event in pygame.event.get():
				pos = pygame.mouse.get_pos()

				if (event.type == pygame.QUIT):
					pygame.quit()
					exit(0)

				if (event.type == pygame.MOUSEBUTTONDOWN):
					if self.restart_button.isOver(pos):
						config_screens.game_start.set(self.level)
						config_screens.game_start.run()
					elif self.choose_level.isOver(pos):
						config_screens.choose_level.set("Choose Level")
						config_screens.choose_level.run()

				if (event.type == pygame.MOUSEMOTION):
					self.restart_button.color = (20, 108, 148) if self.restart_button.isOver(pos) else (25, 167, 206)
					self.choose_level.color = (20, 108, 148) if self.choose_level.isOver(pos) else (25, 167, 206)

			text = config_screens.font.render("Good Luck Next Time", True, (20, 108, 148))
			config_screens.screen.blit(text, ((800 - text.get_width())//2, 250))
						
			pygame.display.update()

			config_screens.clock.tick(config_screens.fps)