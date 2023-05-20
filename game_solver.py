import pyautogui

class Solver:
    def __init__(self, board):
        self.board = board

    def move(self):
        completed = False
        for row in self.board.getBoard():
            for piece in row:
                if not piece.getClicked():
                    continue
                around = piece.getNumAround()
                unknown = 0
                flagged = 0
                neighbors = piece.getNeighbors()
                for p in neighbors:
                    if not p.getClicked():
                        unknown += 1
                    if p.getFlagged():
                        flagged += 1
                if around == flagged:
                    if (self.openUnflagged(neighbors)):
                        completed = True
                if around == unknown:
                    if (self.flagAll(neighbors)):
                        completed = True
        return completed

    def openUnflagged(self, neighbors):
        found = False
        for piece in neighbors:
            if not piece.getFlagged():
                found = True
                self.board.handleClick(piece, False)
        return found

    def flagAll(self, neighbors):
        found = False
        for piece in neighbors:
            if not piece.getFlagged():
                found = True
                self.board.handleClick(piece, True)
        return found