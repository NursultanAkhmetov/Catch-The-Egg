from game_piece import Piece
import random
import pygame

class Board:
    def __init__(self):
        pass

    def set(self, size, bomb_count, index):
        self.size = size
        self.won = False
        self.lost = False
        
        bomb_field = [[False for j in range(size[1])] for i in range(size[0])]
        while (bomb_count):
            for row in range(size[0]):
                for col in range(size[1]):
                    if(row == index[0] and col == index[1]):
                        continue
                    bomb = random.random() < 0.1
                    if(bomb and bomb_count):
                        bomb_field[row][col] = True
                        bomb_count -= 1
                        break
                if(not bomb_count):
                    break

        self.board = []
        for row in range(size[0]):
            r = []
            for col in range(size[1]):
                piece = Piece(bomb_field[row][col])
                r.append(piece)
            self.board.append(r)

        self.setNeighbors()
        self.setNumAround()

    def print(self):
        for row in self.board:
            for piece in row:
                print(piece, end=" ")
            print()

    def getBoard(self):
        return self.board

    def getSize(self):
        return self.size
    
    def getPiece(self, index):
        return self.board[index[0]][index[1]]

    def handleClick(self, piece, flag):
        if piece.getClicked() or (piece.getFlagged() and not flag):
            return
        if flag:
            piece.toggleFlag()
            if(piece.getFlagged()):
                pointSound = pygame.mixer.Sound("audio/point.wav")
                pointSound.play()
            return
        piece.handleClick()
        if piece.getNumAround() == 0:
            for neighbor in piece.getNeighbors():
                self.handleClick(neighbor, False)
        if piece.getHasBomb():
            self.lost = True
        else:
            self.won = self.checkWon()
    
    def getBombLeft(self, size):
        bomb_left = 0
        for row in range(size[0]):
            for col in range(size[1]):
                bomb_left += self.getPiece((row, col)).getFlagged()
        return bomb_left

    def checkWon(self):
        for row in self.board:
            for piece in row:
                if not piece.getHasBomb() and not piece.getClicked():
                    return False
        return True

    def getWon(self):
        return self.won

    def getLost(self):
        return self.lost

    def setNeighbors(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                piece = self.board[row][col]
                neighbors = []
                self.addToNeighborsList(neighbors, row, col)
                piece.setNeighbors(neighbors)
    
    def addToNeighborsList(self, neighbors, row, col):
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if r == row and c == col:
                    continue
                if r < 0 or r >= self.size[0] or c < 0 or c >= self.size[1]:
                    continue
                neighbors.append(self.board[r][c])
    
    def setNumAround(self):
        for row in self.board:
            for piece in row:
                piece.setNumAround() 
        