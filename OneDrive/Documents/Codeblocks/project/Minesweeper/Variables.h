#pragma once
#pragma once
#ifndef VARIABLES_H
#define VARIABLES_H

#include "Texture.h"
#include "Button.h"
#include <sstream>
#include <cstring>

const std::string WINDOW_TITLE = "Minesweeper!";

const int SCREEN_WIDTH = 720;
const int SCREEN_HEIGHT = 720;
const int TILE_SIZE = 32;
// initialization
extern SDL_Window* window;
extern SDL_Renderer* renderer;

// loop variable
extern bool isRunning;
extern bool showmenu;
extern bool isChoosing;
extern bool mainLoop;

//win or lose
extern bool isWinning;
extern bool lose;



// image use in game
extern LTexture menuTheme;
extern LTexture levelTheme;
extern LTexture easyTable;
extern LTexture mediumTable;
extern LTexture hardTable;
extern LTexture customStart;
extern LTexture back;


// Tiles in board
extern LTexture Tiles_image;
extern SDL_Rect Tilesprites[12];

// text
extern LTexture menu;
extern LTexture menu1;
extern LTexture menuColor;
extern LTexture menu1Color;
extern LTexture easyChoice;
extern LTexture mediumChoice;
extern LTexture hardChoice;
extern LTexture easyChoiceColor;
extern LTexture mediumChoiceColor;
extern LTexture hardChoiceColor;
extern LTexture easyBackGround;
extern LTexture mediumBackGround;
extern LTexture hardBackGround;

extern LTexture scoreTheme;
extern LTexture easyOver;
extern LTexture mediumOver;
extern LTexture hardOver;
extern LTexture easyWinning;
extern LTexture mediumWinning;
extern LTexture hardWinning;
extern LTexture easyFont;
extern LTexture mediumFont;
extern LTexture hardFont;
extern LTexture winning;
extern LTexture game_over;
extern LTexture play_again;
extern LTexture play_againColor;

extern LTexture wInput;
extern LTexture hInput;
extern LTexture mInput;
extern TTF_Font* gFont;

extern LTexture mineLeft;

// Create board data
extern std::vector <std::vector<int> > sBoard;
extern std::vector <std::vector<int> > board;

// mines
extern int mineCountLeft;
extern int CountTileLeft;
extern int score;

// audio
extern bool mute;
extern Mix_Chunk* click;
extern Mix_Music* loseMusic;
extern Mix_Music* winMusic;

// distance
extern int distance_x;
extern int distance_y;
extern int digit_x;
extern int digit_y;

// digits image
extern LTexture Digits;
extern SDL_Rect Digitsprites[10];

// board size
extern int BOARD_SIZE_X;
extern int BOARD_SIZE_Y;
extern int NumberOfMines;


// boolean
extern bool playAgain;
extern bool saveScore;
extern bool start;
extern bool easy;
extern bool medium;
extern bool hard;
extern bool customMode;
extern bool isAgain;

#endif
