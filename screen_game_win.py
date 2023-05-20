import pygame
import bisect

import config_screens

from google_sheets_API import GoogleSheetsAPI
from element_button import Button

class GameWin():
	def __init__(self):
		self.save_highscore_button = Button(250, 150, 300, 70, "Save The Result")
		self.restart_button = Button(25, 520, 300, 60, "Play Again")
		self.main_button = Button(475, 520, 300, 60, "Main Menu")

	def set(self, level, score):
		if (pygame.display.Info().current_w != 800 or pygame.display.Info().current_h != 600):
			config_screens.set((800, 600))
		pygame.display.set_caption("Gave Over")
		self.bg_image = pygame.image.load("img/bg/game-over-bg.png")

		self.level = level
		self.score = score

		self.googleSheetsAPI = GoogleSheetsAPI()
		self.total_scores = self.googleSheetsAPI.get_total_scores(self.level)
		self.values = self.googleSheetsAPI.get_values_for_top_score(self.level)
		
		self.id = self.googleSheetsAPI.save_score(self.total_scores, self.level, self.score)
		
		scores = []
		for row in self.values:
			scores.append(int(row[2]))

		self.higher_than = bisect.bisect_left(scores, self.score)

		self.new_record = False
		if(self.higher_than <= 4):
			self.new_record = True
	
	def run(self):
		while (True):
			config_screens.screen.blit(self.bg_image, (0, 0))

			self.restart_button.draw(config_screens.screen)
			self.main_button.draw(config_screens.screen)
			if (self.new_record):
				self.save_highscore_button.draw(config_screens.screen)

			for event in pygame.event.get():
				pos = pygame.mouse.get_pos()

				if (event.type == pygame.QUIT):
					pygame.quit()
					exit(0)

				if (event.type == pygame.MOUSEBUTTONDOWN):
					if self.new_record and self.save_highscore_button.isOver(pos):
						config_screens.game_save_highscore.set(self.id, self.level, self.score)
						config_screens.game_save_highscore.run()
					elif self.restart_button.isOver(pos):
						config_screens.game_start.set(self.level)
						config_screens.game_start.run()
					elif self.main_button.isOver(pos):
						config_screens.main_menu.run()

				if (event.type == pygame.MOUSEMOTION):
					self.restart_button.color = (20, 108, 148) if self.restart_button.isOver(pos) else (25, 167, 206)
					self.main_button.color = (20, 108, 148) if self.main_button.isOver(pos) else (25, 167, 206)
					if (self.new_record):
						self.save_highscore_button.color = (20, 108, 148) if self.save_highscore_button.isOver(pos) else (25, 167, 206)

			text = config_screens.font.render("Your earned " + str(self.score/100.0) + " points", True, (20, 108, 148))
			config_screens.screen.blit(text, (100, 250))

			text = config_screens.font.render("Your result is better than " + str("{:.2f}".format((self.total_scores - self.higher_than)*100.0/(self.total_scores))) + "% results", True, (20, 108, 148))
			config_screens.screen.blit(text, (100, 350))	
			
			pygame.display.update()

			config_screens.clock.tick(config_screens.fps)