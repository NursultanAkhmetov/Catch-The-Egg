# Catch-The-Egg

Welcome to "Catch The Egg", a game created as a part of the application process for the nFactorial Incubator 2023 program. The game is developed using Python with Pygame and Google Sheets API libraries.

## How To Play
To move the basket left and right, use the left and right arrow keys. Your goal is to catch as many eggs as possible without touching the bombs. The game has three levels of difficulty: easy, medium, and hard, each with five lives.

### Easy level:
The falling speed of the objects is the lowest, and all objects are eggs.

### Medium level:
The speed is faster than in the previous level, and there are also bomb objects that should be avoided.

### Hard level:
The fastest speed in the game, and there is also a type of egg that is similar to the background color, making it more challenging to play.

## Saving the players result
If you manage to get a high score and make it to the top 5, you will be asked to enter your nickname to save your results. Otherwise, your results will be saved with the nickname "Unknown".

## Installation
To play the game, you need to have Python installed on your computer along with the Pygame and Google Sheets API libraries. You can download and install Python from the official website: https://www.python.org/downloads/.

### Installing Pygame
To install Pygame, use the following command in your terminal:
pip3 install pygame

### Installing Google Sheets API
To install Google Sheets API, use the following command in your terminal:
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

### Starting the game
To start the game, navigate to the root folder of the game in your terminal and run the following command:
python3 main.py

## Author
Nursultan Akhmetov

## License
This project is licensed under the MIT License.

## Acknowledgments
Special thanks to the nFactorial Incubator 2023 program for giving me the opportunity to create this game.