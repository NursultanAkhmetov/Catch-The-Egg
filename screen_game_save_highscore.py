import pygame
import config_screens

from element_button import Button
from element_input_box import InputBox
from google_sheets_API import GoogleSheetsAPI

class GameSaveHighscores:
	def __init__(self):
		self.save_button = Button(250, 310, 300, 70, "Save", 35)

	def set(self, id, level, score):
		self.nickname_box = InputBox(250, 220, 300, 70)
		self.bg_image = pygame.image.load("img/bg/save-highscore-bg.png")
		self.googleSheetsAPI = GoogleSheetsAPI()

		self.id = id
		self.level = level
		self.score = score

		self.saved = [False]

	def run(self):
		while True:
			config_screens.screen.blit(self.bg_image, (0, 0))

			self.save_button.draw(config_screens.screen)

			for event in pygame.event.get():
				pos = pygame.mouse.get_pos()

				if (event.type == pygame.QUIT):
					pygame.quit()
					exit(0)

				if (event.type == pygame.MOUSEBUTTONDOWN):
					if self.save_button.isOver(pos):
						self.saved[0] = True

				if (event.type == pygame.MOUSEMOTION):
					self.save_button.color = (20, 108, 148) if self.save_button.isOver(pos) else (25, 167, 206)

				self.nickname_box.handle_event(event, self.saved)

			if (self.saved[0]):
				self.googleSheetsAPI.save_score(self.id - 2, self.level, self.score, self.nickname_box.text)
				#self.nickname_box.text = ""
				config_screens.highscores.set(self.level)
				config_screens.highscores.run()

			self.nickname_box.update()
			self.nickname_box.draw(config_screens.screen)

			pygame.display.update()
			config_screens.clock.tick(config_screens.fps)