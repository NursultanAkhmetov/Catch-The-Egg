import pygame
from pygame._sdl2 import Window

from screen_main_menu import MainMenu
from screen_show_info import ShowInfo
from screen_level import ChooseLevel
from screen_highscores import Highscores

from screen_game_start import GameStart
from screen_game_win import GameWin
from screen_game_over import GameOver
from screen_game_save_highscore import GameSaveHighscores

pygame.init()

monitor_width = pygame.display.Info().current_w
monitor_height = pygame.display.Info().current_h
screen = pygame.display.set_mode((800, 600)) 
font = pygame.font.SysFont("comicsans", 30)
font_for_game = pygame.font.SysFont("comicsans", 20)
clock = pygame.time.Clock()
fps = 60

main_menu = MainMenu()
show_info = ShowInfo()
choose_level = ChooseLevel()
highscores = Highscores()

game_start = GameStart()
game_over = GameOver()
game_win = GameWin()
game_save_highscore = GameSaveHighscores()

def set(size):
    screen = pygame.display.set_mode(size)
    screen_x = (monitor_width - size[0]) // 2
    screen_y = (monitor_height - size[1]) // 2
    window = Window.from_display_module()
    window.position = (screen_x, screen_y)
    pygame.display.flip()