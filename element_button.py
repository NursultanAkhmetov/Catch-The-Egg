import pygame

class Button():
    def __init__(self, x, y, width, height, text="", font_size = 30, color = (25, 167, 206), outline = (20, 108, 148)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.color = color
        self.outline = outline

    def draw(self, screen):
        pygame.draw.rect(screen, self.outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height),0)
        
        if (self.text != ""):
            font = pygame.font.SysFont("comicsans", self.font_size)
            text = font.render(self.text, 1, (246,241,241))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if (pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height):
                return True
        return False