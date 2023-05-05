import pygame
from pygame import mixer
import time

import random
import math

import bisect
from googleapiclient.discovery import build
from google.oauth2 import service_account

class Button():
    def __init__(self, color, outline, x,y,width,height, text="", font_size = 60):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.outline = outline

    def draw(self,screen):
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

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.w = w
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event, level, saved):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    saved[0] = True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(self.w, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

class Player():
	def __init__(self, path = "img/basket.png", width = 64, height = 64, x_change = 0):
		self.img = pygame.image.load(path)
		self.img = pygame.transform.scale(self.img, (width, height))
		self.width = width
		self.height = height
		self.x = (screen_width - width) / 2
		self.y = screen_height - height - 100
		self.x_change = x_change
		self.last_frame_key_left = False
		self.last_frame_key_right = False
		self.key_left = False
		self.key_right = False
		self.go_left = False
		self.go_right = False

	def draw(self):
		if(self.key_left and (not self.last_frame_key_left)):
		    self.go_left = True;
		    self.go_right = False;
		elif((not self.key_left) and self.last_frame_key_left):
		    self.go_left = False;
		self.last_frame_key_left = self.key_left;

		if(self.key_right and (not self.last_frame_key_right)):
		    self.go_right = True;
		    self.go_left = False;
		elif((not self.key_right) and self.last_frame_key_right):
		    self.go_right = False;
		self.last_frame_key_right = self.key_right;

		if (self.go_left == False and self.go_right == False):
			self.x_change = 0
		elif self.go_left:
			self.x_change = -10
		elif self.go_right:
			self.x_change = 10

		self.x += self.x_change

		if (self.x <= 0):
			self.x = 0
		elif (self.x >= screen_width - self.width):
			self.x = screen_width - self.width

		screen.blit(self.img, (self.x, self.y))		

class Items():
	x = {}
	y = {}
	model = {}

	def __init__(self, width = 32, height = 32):
		self.width = width
		self.height = height
		self.img1 = pygame.transform.scale(pygame.image.load("img/item1.png"), (width, height))
		self.img2 = pygame.transform.scale(pygame.image.load("img/item2.png"), (width, height))
		self.img3 = pygame.transform.scale(pygame.image.load("img/item3.png"), (width, height))
		self.fall_speed = 5
		self.min_frequency_initial = 1200
		self.max_frequency_initial = 1600
		self.min_frequency_final = 800
		self.max_frequency_final = 1100
		self.frequency_change = 0	
		self.last_x_pos = 400

	def configure_speed(self, level):
		self.min_frequency_initial = self.min_frequency_initial - (level == "medium")*200 - (level == "hard")*200
		self.max_frequency_initial = self.max_frequency_initial - (level == "medium")*200 - (level == "hard")*200
		self.min_frequency_final = self.min_frequency_final - (level == "medium")*200 - (level == "hard")*200
		self.max_frequency_final = self.max_frequency_final - (level == "medium")*200 - (level == "hard")*200

	def reset(self):
		self.x.clear()
		self.y.clear()
		self.model.clear()
		self.frequency_change = 0

	def draw(self, player, level):
		global cur_item, lives, score, frequency, cur_time, last_spawn_time, last_move_time
		
		if(cur_time - last_spawn_time > frequency):
			cur_item += 1
			xx = random.randint(0, screen_width - self.width)
			while (abs(xx - self.last_x_pos) > 550):
				xx = random.randint(0, screen_width - self.width)
			self.x[cur_item] = xx
			self.last_x_pos = xx
			self.y[cur_item] = -self.height
			self.model[cur_item] = 1
			n = random.randint(1, 10)
			if (level != "easy" and n >= 8):
				self.model[cur_item] = 2
			elif (level == "hard"): 
				if (n >= 5):
					self.model[cur_item] = 3
			frequency = random.randint(
					max(self.min_frequency_final, self.min_frequency_initial - self.frequency_change),
					max(self.max_frequency_final, self.max_frequency_initial - self.frequency_change)
				)
			self.frequency_change += 50
			last_spawn_time = cur_time
		
		keys_to_delete = []
		for item in self.model:
			self.y[item] += self.fall_speed
			img = self.img1
			if (self.model[item] == 1):
				img = self.img1
			elif (self.model[item] == 2):
				img = self.img2
			elif (self.model[item] == 3):
				img = self.img3
			screen.blit(img, (self.x[item], self.y[item]))
			
			player_mid = player.x + player.width/2
			item_mid = self.x[item] + self.width/2

			if (abs(player_mid - item_mid) <= player.width/2):
				if(screen_height - player.width - self.width/2 - 100
				   <= self.y[item] <=
				   screen_height - player.width - 100):
					keys_to_delete.append(item)
					if (self.model[item] == 2):
						lives -= 1
						bombSound = mixer.Sound("audio/bomb.wav")
						bombSound.play()
					else:
						pointSound = mixer.Sound("audio/point.wav")
						pointSound.play()
			else:
				if(screen_height - player.width + self.width < self.y[item]):
					keys_to_delete.append(item)
					if (self.model[item] != 2):
						lives -= 1

		for key in keys_to_delete:
			del self.x[key]
			del self.y[key]
			del self.model[key]

def draw_cell(screen, color_header, outline_header, x, y, width, height, font_size, text_to_print):
	pygame.draw.rect(screen, outline_header, (x - 2,y - 2,width + 4,height + 4),0)
	pygame.draw.rect(screen, color_header, (x,y,width,height),0)
	font = pygame.font.SysFont("comicsans", font_size)
	text = font.render(text_to_print, 1, (255,255,255))
	screen.blit(text, (x + (width/2 - text.get_width()/2), y + (height/2 - text.get_height()/2)))

def show_message(x, y, message, color):
	font = pygame.font.SysFont("comicsans", 30)
	text = font.render(message, True, color)
	screen.blit(text, (x, y))

def main_menu():
	pygame.display.set_caption("Main Menu")
	bg_image = pygame.image.load("img/bg/main-bg.png")

	play_btn = Button((25, 167, 206), (20, 108, 148), 250, 170, 300, 60, "Play", 30)
	how_to_play_btn = Button((25, 167, 206), (20, 108, 148), 250, 250, 300, 60, "How To Play", 30)
	highscores_btn = Button((25, 167, 206), (20, 108, 148), 250, 330, 300, 60, "High Scores", 30)
	about_btn = Button((25, 167, 206), (20, 108, 148), 250, 410, 300, 60, "About The Game", 30)
	quit_btn = Button((25, 167, 206), (20, 108, 148), 250, 490, 300, 60, "Quit", 30)
	buttons = [play_btn, how_to_play_btn, highscores_btn, about_btn, quit_btn]

	running = True
	while (running):
		screen.fill((255, 255, 255))
		screen.blit(bg_image, (0, 0))
		
		for button in buttons:
			button.draw(screen)

		for event in pygame.event.get():
			pos = pygame.mouse.get_pos()

			if (event.type == pygame.QUIT):
				running = False
				pygame.quit();
				quit()

			if (event.type == pygame.MOUSEBUTTONDOWN):
				if play_btn.isOver(pos):
					choose_level("Choose Level")
				elif how_to_play_btn.isOver(pos):
					show_info("How To Play", "img/bg/how-to-play-bg.png")
				elif highscores_btn.isOver(pos):
					choose_level("High Scores")
				elif about_btn.isOver(pos):
					show_info("About The Game", "img/bg/about-bg.png")
				elif quit_btn.isOver(pos):
					running = False
					pygame.quit();
					quit()

			if (event.type == pygame.MOUSEMOTION):
				for button in buttons:
					button.color = (20, 108, 148) if button.isOver(pos) else (25, 167, 206)

		pygame.display.update()

		clock.tick(60)

def choose_level(caption):
	pygame.display.set_caption(caption)
	if (caption == "Choose Level"):
		bg_image = pygame.image.load("img/bg/choose-level-bg.png")
	elif (caption == "High Scores"):
		bg_image = pygame.image.load("img/bg/highscores-bg.png")

	level1_btn = Button((25, 167, 206), (20, 108, 148), 250, 170, 300, 60, "Easy Level", 30)
	level2_btn = Button((25, 167, 206), (20, 108, 148), 250, 250, 300, 60, "Medium Level", 30)
	level3_btn = Button((25, 167, 206), (20, 108, 148), 250, 330, 300, 60, "Hard Level", 30)
	go_back_btn = Button((25, 167, 206), (20, 108, 148), 250, 410, 300, 60, "Go Back", 30)
	buttons = [level1_btn, level2_btn, level3_btn, go_back_btn]

	running = True
	while (running):
		screen.fill((255, 255, 255))
		screen.blit(bg_image, (0, 0))
		
		for button in buttons:
			button.draw(screen)

		for event in pygame.event.get():
			pos = pygame.mouse.get_pos()

			if (event.type == pygame.QUIT):
				running = False
				pygame.quit();
				quit()

			if (event.type == pygame.MOUSEBUTTONDOWN):
				if level1_btn.isOver(pos):
					if caption == "Choose Level":
						game("easy")
					elif caption == "High Scores":
						highscores("easy")
				elif level2_btn.isOver(pos):
					if caption == "Choose Level":
						game("medium")
					elif caption == "High Scores":
						highscores("medium")
				elif level3_btn.isOver(pos):
					if caption == "Choose Level":
						game("hard")
					elif caption == "High Scores":
						highscores("hard")
				elif go_back_btn.isOver(pos):
					main_menu()

			if (event.type == pygame.MOUSEMOTION):
				for button in buttons:
					button.color = (20, 108, 148) if button.isOver(pos) else (25, 167, 206)

		pygame.display.update()

		clock.tick(60)

def show_info(caption, path):
	pygame.display.set_caption(caption)
	bg_image = pygame.image.load(path)

	go_back_btn = Button((25, 167, 206), (20, 108, 148), 25, 520, 300, 60, "Go Back", 30)

	running = True
	while (running):
		screen.fill((255, 255, 255))
		screen.blit(bg_image, (0, 0))
		
		go_back_btn.draw(screen)

		for event in pygame.event.get():
			pos = pygame.mouse.get_pos()

			if (event.type == pygame.QUIT):
				running = False
				pygame.quit();
				quit()

			if (event.type == pygame.MOUSEBUTTONDOWN):
				if go_back_btn.isOver(pos):
					main_menu()

			if (event.type == pygame.MOUSEMOTION):
				go_back_btn.color = (20, 108, 148) if go_back_btn.isOver(pos) else (25, 167, 206)

		pygame.display.update()

		clock.tick(60)

def highscores(level):
	color_header = (20, 108, 148)
	color = (175, 211, 226)
	outline_header = (20, 108, 148)
	outline = (25, 167, 206)
	width_col1 = 300
	width_col2 = 200
	height = 60
	font_size = 35
	col1_x = 250
	col2_x = 550
	y = [150, 210, 270, 330, 390, 450]
	text_col1 = ["Nickname"]
	text_col2 = ["Score"]

	total_scores = int(sheet.values().get(spreadsheetId=SPREADSHEET_ID,
	                            range=level+"!A1").execute().get('values', [])[0][0])
	res = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
	                            range=level+"!A2:D10000").execute()
	values = res.get('values', [])

	values.sort(key=lambda row: (int(row[2]), -int(row[0])), reverse=True)

	for i in range(5):
		text_col1.append(values[i][1])
		text_col2.append(values[i][2])

	pygame.display.set_caption("High Scores")
	bg_image = pygame.image.load("img/bg/highscores-bg2-" + level + ".png")

	go_back_btn = Button((25, 167, 206), (20, 108, 148), 250, 530, 200, 60, "Go Back", 30)
	play_btn = Button((25, 167, 206), (20, 108, 148), 550, 530, 200, 60, "Play", 30)

	running = True
	while (running):
		screen.fill((255, 255, 255))
		screen.blit(bg_image, (0, 0))

		draw_cell(screen, color_header, outline_header, col1_x, y[0], width_col1, height, font_size, text_col1[0])
		draw_cell(screen, color_header, outline_header, col2_x, y[0], width_col2, height, font_size, text_col2[0])

		for i in range(1, 6):
			draw_cell(screen, color, outline, col1_x, y[i], width_col1, height, font_size, text_col1[i])
			draw_cell(screen, color, outline, col2_x, y[i], width_col2, height, font_size, str("{:.2f}".format(float(text_col2[i])/100)))

		go_back_btn.draw(screen)
		play_btn.draw(screen)

		for event in pygame.event.get():
			pos = pygame.mouse.get_pos()

			if (event.type == pygame.QUIT):
				running = False
				pygame.quit();
				quit()

			if (event.type == pygame.MOUSEBUTTONDOWN):
				if go_back_btn.isOver(pos):
					choose_level("High Scores")
				if play_btn.isOver(pos):
					game(level)

			if (event.type == pygame.MOUSEMOTION):
				go_back_btn.color = (20, 108, 148) if go_back_btn.isOver(pos) else (25, 167, 206)

		pygame.display.update()

		clock.tick(60)

def game(level):
	
	pygame.display.set_caption("Catch The Egg")

	global cur_item, lives, score, frequency, cur_time, last_spawn_time, last_move_time
	cur_item = 0
	lives = 5
	score = 0
	frequency = 1000
	last_spawn_time = int(time.time() * 1000)
	last_move_time = int(time.time() * 1000)

	start_time = int(time.time() * 1000)
	player = Player()
	items = Items()
	items.configure_speed(level)
	
	bg_image = pygame.image.load("img/bg/game-bg.png")

	while (lives):
		screen.fill((0, 0, 255))
		screen.blit(bg_image, (0, 0))
		
		for event in pygame.event.get():

			if (event.type == pygame.QUIT):
				running = False
				pygame.quit();
				quit()

			if (event.type == pygame.KEYDOWN):
				if event.key == pygame.K_LEFT:
					player.key_left = True
				if event.key == pygame.K_RIGHT:
					player.key_right = True
			
			if (event.type == pygame.KEYUP):
				if event.key == pygame.K_LEFT:
					player.key_left = False
				if (event.key == pygame.K_RIGHT):
					player.key_right = False
		
		cur_time = int(time.time() * 1000)
		score = int((cur_time - start_time) / 10)
		
		items.draw(player, level)

		player.draw()

		show_message(10, 10, "Score : " + str("{:.2f}".format(score / 100.0)), (255, 255, 255))

		show_message(680, 10, "Lives: " + str(lives), (255, 255, 255))

		pygame.display.update()

		clock.tick(fps)

	items.reset()
	game_over(level)

def game_over(level):
	global score
	total_scores = int(sheet.values().get(spreadsheetId=SPREADSHEET_ID,
	                            range=level+"!A1").execute().get('values', [])[0][0])
	res = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
	                            range=level+"!A2:D10000").execute()
	values = res.get('values', [])

	values.sort(key=lambda row: (int(row[2])))

	aoa = [[total_scores + 1, "Unknown", score]]
	request = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
	                        range=level+"!A" + str(total_scores + 2), valueInputOption="USER_ENTERED", body={"values":aoa}).execute()
	scores = []
	for row in values:
	    scores.append(int(row[2]))

	higher_than = bisect.bisect_left(scores, score)

	new_record = False
	if(total_scores - higher_than <= 4):
	    new_record = True

	pygame.display.set_caption("Gave Over")
	save_highscore_button = Button((25, 167, 206), (20, 108, 148), 250, 150, 300, 70, "Save The Result", 35)
	restart_button = Button((25, 167, 206), (20, 108, 148), 25, 520, 300, 60, "Play Again", 30)
	main_button = Button((25, 167, 206), (20, 108, 148), 475, 520, 300, 60, "Main Menu", 30)
	
	bg_image = pygame.image.load("img/bg/game-over-bg.png")

	running = True
	while (running):
		screen.fill((255, 255, 255))
		screen.blit(bg_image, (0, 0))

		if (new_record):
			save_highscore_button.draw(screen)
		restart_button.draw(screen)
		main_button.draw(screen)

		for event in pygame.event.get():
			pos = pygame.mouse.get_pos()

			if (event.type == pygame.QUIT):
				running = False
				pygame.quit();
				quit()

			if (event.type == pygame.MOUSEBUTTONDOWN):
				if new_record and save_highscore_button.isOver(pos):
					save_highscore(level)
				elif restart_button.isOver(pos):
					game(level)
				elif main_button.isOver(pos):
					main_menu()

			if (event.type == pygame.MOUSEMOTION):
				restart_button.color = (20, 108, 148) if restart_button.isOver(pos) else (25, 167, 206)
				main_button.color = (20, 108, 148) if main_button.isOver(pos) else (25, 167, 206)
				if (new_record):
					save_highscore_button.color = (20, 108, 148) if save_highscore_button.isOver(pos) else (25, 167, 206)

		show_message(100, 250, "Your earned " + str(score/100.0) + " points", (20, 108, 148))
		show_message(100, 350, "Your result is better than " + str("{:.2f}".format((higher_than)*100.0/(total_scores))) + "% results", (20, 108, 148))

		pygame.display.update()

		clock.tick(60)

def save_highscore(level):
	global score
	total_scores = int(sheet.values().get(spreadsheetId=SPREADSHEET_ID,
	                            range=level+"!A1").execute().get('values', [])[0][0])

	nickname_box = InputBox(250, 220, 300, 70)
	save_button = Button((25, 167, 206), (20, 108, 148), 250, 310, 300, 70, "Save", 35)
	bg_image = pygame.image.load("img/bg/save-highscore-bg.png")
	saved = [False]
	
	running = True
	while running:
		screen.fill((255, 255, 255))
		screen.blit(bg_image, (0, 0))

		save_button.draw(screen)

		for event in pygame.event.get():
			pos = pygame.mouse.get_pos()

			if (event.type == pygame.QUIT):
				running = False
				pygame.quit();
				quit()

			if (event.type == pygame.MOUSEBUTTONDOWN):
				if save_button.isOver(pos):
					saved[0] = True

			if (event.type == pygame.MOUSEMOTION):
				save_button.color = (20, 108, 148) if save_button.isOver(pos) else (25, 167, 206)

			nickname_box.handle_event(event, level, saved)

		if (saved[0]):
			aoa = [[total_scores, nickname_box.text, score]]
			request = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
								range=level+"!A" + str(total_scores + 1), valueInputOption="USER_ENTERED", body={"values":aoa}).execute()
			highscores(level)

		nickname_box.update()
		nickname_box.draw(screen)

		pygame.display.update()
		clock.tick(60)

pygame.init()

#icon = pygame.image.load("img/bg/icon.png")
#pygame.display.set_icon(icon)
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
fps = 60
clock = pygame.time.Clock()

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.SysFont("comicsans", 30)

SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SPREADSHEET_ID = '1p_tF8A1rb8-XdkDFXPBhBM3dW2sDAzFTdbOyX3-umWo'
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

mixer.music.load("audio/back.wav")
mixer.music.play(-1)
main_menu()