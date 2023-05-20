import pygame
import os
import config_screens
import time


from game_board import Board
from game_solver import Solver

class GameStart:
    def __init__(self):
        self.pieceSize = (32, 32)
        self.loadPictures()
        self.top_margin = 75
        self.bottom_margin = 75

    def set(self, level):
        self.level = level
        self.score = 0
        self.penalty = 0
        self.start_time = None
        if (level == "easy"):
            self.size = 9, 9
            self.bomb_left = [10]
        elif (level == "medium"):
            self.size = 16, 16
            self.bomb_left = [40]
        elif (level == "hard"):
            self.size = 16, 30
            self.bomb_left = [99]
        self.bomb_count = self.bomb_left[0]
        self.sizeScreen = (self.pieceSize[0]*self.size[1], self.pieceSize[1]*self.size[0] + self.top_margin + self.bottom_margin)
        config_screens.set(self.sizeScreen)
    
    def set_board(self, mouse_pos):
        index = ( (mouse_pos[1] - self.top_margin) // self.pieceSize[1], mouse_pos[0] // self.pieceSize[0])
        self.board = Board()
        self.board.set(self.size, self.bomb_count, index)
        self.solver = Solver(self.board)
    
    def wait_for_start(self):
        self.game_started = False
        clicked = False

        while not clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (pygame.mouse.get_pos()[0] > 5 and pygame.mouse.get_pos()[0] < 50 and
                            pygame.mouse.get_pos()[1] > self.sizeScreen[1] - 60 and
                            pygame.mouse.get_pos()[1] < self.sizeScreen[1] - 15 and
                            pygame.mouse.get_pressed(num_buttons=3)[0]
                            ):
                        config_screens.choose_level.set("Choose Level")
                        config_screens.choose_level.run()
                    if (pygame.mouse.get_pos()[1] > self.top_margin and pygame.mouse.get_pos()[1] < self.sizeScreen[1] - self.bottom_margin):
                        leftClick = pygame.mouse.get_pressed(num_buttons=3)[0]
                        if (leftClick):
                            clicked = True
                            self.set_board(pygame.mouse.get_pos())                            
                            self.handleClick(pygame.mouse.get_pos(), False)
                
                config_screens.screen.fill((246,241,241))
                self.draw_header()

                topLeft = (0, self.top_margin)
                for row in range (self.size[0]):
                    for col in range (self.size[1]):
                        image = self.images["empty-block"]
                        config_screens.screen.blit(image, topLeft) 
                        topLeft = topLeft[0] + self.pieceSize[0], topLeft[1]
                    topLeft = (0, topLeft[1] + self.pieceSize[1])

                self.draw_footer()
                pygame.display.update()
                config_screens.clock.tick(config_screens.fps)

        self.game_started = True
        self.start_time = int(time.time() * 1000)


    def run(self):
        self.wait_for_start()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (pygame.mouse.get_pos()[0] > 5 and pygame.mouse.get_pos()[0] < 50 and
                            pygame.mouse.get_pos()[1] > self.sizeScreen[1] - 60 and
                            pygame.mouse.get_pos()[1] < self.sizeScreen[1] - 15 and
                            pygame.mouse.get_pressed(num_buttons=3)[0]
                            ):
                        config_screens.choose_level.set("Choose Level")
                        config_screens.choose_level.run()
                    if (pygame.mouse.get_pos()[0] > self.sizeScreen[0] - 50 and pygame.mouse.get_pos()[0] < self.sizeScreen[0] - 5 and
                            pygame.mouse.get_pos()[1] > self.sizeScreen[1] - 60 and
                            pygame.mouse.get_pos()[1] < self.sizeScreen[1] - 15 and
                            pygame.mouse.get_pressed(num_buttons=3)[0]
                            ):
                        if (self.solver.move()):
                            self.penalty += 1000
                    if not (self.board.getWon() or self.board.getLost()):
                        if (pygame.mouse.get_pos()[1] > self.top_margin and pygame.mouse.get_pos()[1] < self.sizeScreen[1] - self.bottom_margin):
                            rightClick = pygame.mouse.get_pressed(num_buttons=3)[2]
                            self.handleClick(pygame.mouse.get_pos(), rightClick)
                    
            config_screens.screen.fill((246,241,241))
            self.draw_header()
            self.draw_game()
            self.draw_footer()

            pygame.display.update()
            config_screens.clock.tick(config_screens.fps)

            if self.board.getWon():
                self.win()
                config_screens.game_win.set(self.level, self.score + self.penalty)
                config_screens.game_win.run()
            if self.board.getLost():
                bombSound = pygame.mixer.Sound("audio/bomb.wav")
                bombSound.play()
                time.sleep(3)
                config_screens.game_over.set(self.level)
                config_screens.game_over.run()
        

    
    def draw_header(self):
        # Draw timer
        cur_time = int(time.time() * 1000)   
        if (self.game_started and not self.board.getLost()):
            self.score = (cur_time - self.start_time) // 10
        
        self.images["timer"] = pygame.transform.scale(self.images["timer"], (45, 45))
        timer_pos = (self.sizeScreen[0] - 50, 15)
        config_screens.screen.blit(self.images["timer"], timer_pos)

        time_text = config_screens.font.render(str((self.score + self.penalty) // 100), True, (20,108,148))
        time_pos = (self.sizeScreen[0] - time_text.get_width() - 60, 15)
        config_screens.screen.blit(time_text, time_pos)

        # Draw bomb
        self.images["bomb"] = pygame.transform.scale(self.images["bomb"], (45, 45))
        bomb_pos = (5, 15)
        config_screens.screen.blit(self.images["bomb"], bomb_pos)

        bombs = self.bomb_left[0]

        if (self.game_started and not self.board.getLost()):
            bombs = self.bomb_left[0] - self.board.getBombLeft(self.size)

        bomb_text = config_screens.font.render(str(bombs), True, (20,108,148))
        bomb_pos = (60, 15)
        config_screens.screen.blit(bomb_text, bomb_pos)
        
        # Draw emodji
        self.images["smile"] = pygame.transform.scale(self.images["smile"], (45, 45))
        self.images["upset"] = pygame.transform.scale(self.images["upset"], (45, 45))
        emodji_pos = ((self.sizeScreen[0] - 45)//2, 15)
        
        if(self.game_started and self.board.getLost()):
            config_screens.screen.blit(self.images["upset"], emodji_pos)
        else:
            config_screens.screen.blit(self.images["smile"], emodji_pos)

    def draw_footer(self):
        self.images["prev"] = pygame.transform.scale(self.images["prev"], (45, 45))
        prev_pos = (5, self.sizeScreen[1] - 60)
        config_screens.screen.blit(self.images["prev"], prev_pos)

        if (self.game_started and not self.board.getLost()):
            self.images["help"] = pygame.transform.scale(self.images["help"], (45, 45))
            help_pos = (self.sizeScreen[0] - 50, self.sizeScreen[1] - 60)
            config_screens.screen.blit(self.images["help"], help_pos)

    def draw_game(self):
        topLeft = (0, self.top_margin)
        for row in self.board.getBoard():
            for piece in row:
                image = self.images[self.getImageString(piece)]
                config_screens.screen.blit(image, topLeft) 
                topLeft = topLeft[0] + self.pieceSize[0], topLeft[1]
            topLeft = (0, topLeft[1] + self.pieceSize[1])

    def getImageString(self, piece):
        if piece.getClicked():
            return str(piece.getNumAround()) if not piece.getHasBomb() else 'bomb-at-clicked-block'
        if (self.board.getLost()):
            if (piece.getHasBomb()):
                return 'unclicked-bomb'
            return 'wrong-flag' if piece.getFlagged() else 'empty-block'
        return 'flag' if piece.getFlagged() else 'empty-block'

    def handleClick(self, position, flag):
        index = ( (position[1] - self.top_margin) // self.pieceSize[1], position[0] // self.pieceSize[0])
        self.board.handleClick(self.board.getPiece(index), flag)

    def win(self):
        sound = pygame.mixer.Sound("audio/win.wav")
        sound.play()
        time.sleep(3)
    
    def loadPictures(self):
        self.images = {}
        imagesDirectory = "img"
        for fileName in os.listdir(imagesDirectory):
            if not fileName.endswith(".png"):
                continue
            path = imagesDirectory + r"/" + fileName 
            img = pygame.image.load(path)
            img = img.convert_alpha()
            img = pygame.transform.scale(img, (int(self.pieceSize[0]), int(self.pieceSize[1])))
            self.images[fileName.split(".")[0]] = img