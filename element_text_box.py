import pygame

class TextBox():
	def __init__(self, color_header, outline_header, x, y, width, height, font_size, text_to_print):
		self.color_header = color_header
		self.outline_header = outline_header
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.font_size = font_size
		self.text_to_print = text_to_print

	def draw(self,screen):
		pygame.draw.rect(screen, self.outline_header, (self.x - 2,self.y - 2,self.width + 4,self.height + 4),0)
		pygame.draw.rect(screen, self.color_header, (self.x,self.y,self.width,self.height),0)
		font = pygame.font.SysFont("comicsans", self.font_size)
		text = font.render(self.text_to_print, 1, (255,255,255))
		screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))