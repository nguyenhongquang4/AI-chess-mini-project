#include "Variables.h"
#include<iostream>
// loop variable
extern bool isRunning = false;
extern bool showmenu = false;
extern bool isChoosing = true;
extern bool mainLoop = true;

// win or lose
extern bool isWinning = false;
extern bool lose = false;

// mines
extern int mineCountLeft = NumberOfMines;
extern int CountTileLeft = BOARD_SIZE_X * BOARD_SIZE_Y;
extern int score = 0;
// images use in game
extern LTexture menuTheme(NULL, 0, 0);
extern LTexture levelTheme(NULL, 0, 0);
extern LTexture easyTable(NULL, 0, 0);
extern LTexture mediumTable(NULL, 0, 0);
extern LTexture hardTable(NULL, 0, 0);
extern LTexture scoreTheme(NULL, 0, 0);
extern LTexture back(NULL, 0, 0);

// text
extern LTexture menu(NULL, 0, 0);
extern LTexture menu1(NULL, 0, 0);
extern LTexture menuColor(NULL, 0, 0);
extern LTexture menu1Color(NULL, 0, 0);
extern LTexture easyChoice(NULL, 0, 0);
extern LTexture mediumChoice(NULL, 0, 0);
extern LTexture hardChoice(NULL, 0, 0);
extern LTexture easyChoiceColor(NULL, 0, 0);
extern LTexture mediumChoiceColor(NULL, 0, 0);
extern LTexture hardChoiceColor(NULL, 0, 0);
extern LTexture easyBackGround(NULL, 0, 0);
extern LTexture mediumBackGround(NULL, 0, 0);
extern LTexture hardBackGround(NULL, 0, 0);


extern LTexture easyOver(NULL, 0, 0);
extern LTexture mediumOver(NULL, 0, 0);
extern LTexture hardOver(NULL, 0, 0);
extern LTexture easyWinning(NULL, 0, 0);
extern LTexture mediumWinning(NULL, 0, 0);
extern LTexture hardWinning(NULL, 0, 0);
extern LTexture easyFont(NULL, 0, 0);
extern LTexture mediumFont(NULL, 0, 0);
extern LTexture hardFont(NULL, 0, 0);
extern LTexture winning(NULL, 0, 0);
extern LTexture game_over(NULL, 0, 0);
extern LTexture play_again(NULL, 0, 0);
extern LTexture play_againColor(NULL, 0, 0);

extern LTexture mineLeft(NULL, 0, 0);

// create board data
extern std::vector <std::vector<int> > sBoard(3, std::vector<int>(2,0));
extern std::vector <std::vector<int> > board(3, std::vector<int>(2, 0));

// Tiles in board
extern LTexture Tiles_image(NULL, 0, 0);
extern SDL_Rect Tilesprites[12] = {};

// audio
extern Mix_Chunk* click = NULL;
extern Mix_Music* loseMusic = NULL;
extern Mix_Music* winMusic = NULL;

// distance
extern int distance_x = 0;
extern int distance_y = 0;
extern int digit_x = 0;
extern int digit_y = 0;

// digits image
extern LTexture Digits(NULL, 0, 0);
extern SDL_Rect Digitsprites[10] = {};

// Board size
extern int BOARD_SIZE_X = 0;
extern int BOARD_SIZE_Y = 0;
extern int NumberOfMines = 0;

// boolean
extern bool playAgain = false;
extern bool saveScore = false;
extern bool start = false;
extern bool easy = false;
extern bool medium = false;
extern bool hard = false;
extern bool isAgain = false;
