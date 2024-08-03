#include "Texture.h"
#include "Variables.h"
#include "Button.h"
#include "mainFunction.h"
#include <sstream>
#include <fstream>
#include <ctime>
#include <string>
using namespace std;
vector <vector<LButton> > Buttons(3, vector<LButton>(2));
LButton face;
LButton goBack;
LButton sound;
stringstream mine_left;
stringstream scoreFont;
stringstream gameOver;
stringstream youWin;
stringstream yourScore;

//initialization func
bool init()
{
	//Initialization flag
	bool success = true;

	//Initialize SDL
	if (SDL_Init(SDL_INIT_VIDEO) < 0)
	{
		printf("SDL could not initialize! SDL Error: %s\n", SDL_GetError());
		success = false;
	}
	else
	{
		//Set texture filtering to linear
		if (!SDL_SetHint(SDL_HINT_RENDER_SCALE_QUALITY, "1"))
		{
			printf("Warning: Linear texture filtering not enabled!");
		}

		//Create window
		window = SDL_CreateWindow(WINDOW_TITLE.c_str(), SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);
		if (window == NULL)
		{
			printf("Window could not be created! SDL Error: %s\n", SDL_GetError());
			success = false;
		}
		else
		{
			renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
			if (renderer == NULL)
			{
				printf("Renderer could not be created! SDL Error: %s\n", SDL_GetError());
				success = false;
			}
			else
			{
				//Initialize renderer color
				SDL_SetRenderDrawColor(renderer, 0xFF, 0xFF, 0xFF, 0xFF);

				//Initialize PNG loading
				int imgFlags = IMG_INIT_PNG;
				if (!(IMG_Init(imgFlags) & imgFlags))
				{
					printf("SDL_image could not initialize! SDL_image Error: %s\n", IMG_GetError());
					success = false;
				}

				//Initialize SDL_ttf
				if (TTF_Init() == -1)
				{
					printf("SDL_ttf could not initialize! SDL_ttf Error: %s\n", TTF_GetError());
					success = false;
				}
				//Initialize SDL_mixer
				if (Mix_OpenAudio(44100, MIX_DEFAULT_FORMAT, 2, 2048) < 0)
				{
					printf("SDL_mixer could not initialize! SDL_mixer Error: %s\n", Mix_GetError());
					success = false;
				}
			}
		}
	}

	return success;
}
bool loadmedia() {
    bool success = true;
	//Open image of tiles
	if (!Tiles_image.loadFromFile("C:/Users/Admin/OneDrive/Pictures/Tiles.png"))
	{
		printf("Can't load this image from file!");
		success = false;
	}
	else
	{
		//Set sprites
		for (int i = 0;i < 12;++i)
		{
			Tilesprites[i].x = i * TILE_SIZE;
			Tilesprites[i].y = 0;
			Tilesprites[i].w = TILE_SIZE;
			Tilesprites[i].h = TILE_SIZE;
		}
	}
    gFont = TTF_OpenFont("C:/Users/Admin/Downloads/DTM-Sans.ttf", 35);
	if (gFont == NULL)
	{
		printf("Failed to load lazy font! SDL_ttf Error: %s\n", TTF_GetError());
		success = false;
	}
	//load text
	SDL_Color textcolor1 = { 255,255,255 };
	if (!menu.loadFromRenderedText("START", textcolor1))
	{
		printf("Fail");
	}
	if (!menu1.loadFromRenderedText("EXIT", textcolor1))
	{
		printf("fail!");
	}
	SDL_Color color = { 255,0,0 };
	if (!menuColor.loadFromRenderedText("START", color))
	{
		printf("Fail");
		success = false;
	}
	if (!menu1Color.loadFromRenderedText("EXIT", color))
	{
		printf("Fail");
		success = false;
	}

	click = Mix_LoadWAV("C:/Users/Admin/Music/Click sound effect.wav");
    if(click == NULL)
    {
        cout << "Failed to load Click sound effect!" << Mix_GetError() <<endl;
        success = false;
    }
    winMusic = Mix_LoadMUS("C:/Users/Admin/Music/Winner sound effect.wav");
    if(winMusic == NULL)
    {
        cout << "Failed to load Winner sound effect!" << Mix_GetError() <<endl;
        success = false;
    }
    loseMusic = Mix_LoadMUS("C:/Users/Admin/Music/Loser sound effect.wav");
    if(loseMusic == NULL)
    {
        cout << "Failed to load Loser sound effect!" << Mix_GetError() <<endl;
        success = false;
    }
    return success;
}

bool loadMenuMedia()
{
	bool success = true;
	//load background of menu
	if (!menuTheme.loadFromFile("C:/Users/Admin/OneDrive/Pictures/Minesweeper.png"))
	{
		printf("Fail!");
		success = false;
	}
	//load level choice
	if (!levelTheme.loadFromFile("C:/Users/Admin/OneDrive/Pictures/mode1.png"))
	{
		printf("Fail");
		success = false;
	}
	if(!easyBackGround.loadFromFile("C:/Users/Admin/OneDrive/Pictures/Easy picture.png")) {
        printf("Can't load this image from file!");
		success = false;
	}
	if(!mediumBackGround.loadFromFile("C:/Users/Admin/OneDrive/Pictures/Medium picture.png")) {
        printf("Can't load this image from file!");
		success = false;
	}
	if(!hardBackGround.loadFromFile("C:/Users/Admin/OneDrive/Pictures/Hard picture.png")) {
        printf("Can't load this image from file!");
		success = false;
	}

	if(!easyOver.loadFromFile("C:/Users/Admin/OneDrive/Pictures/easy over.png")) {
        printf("Can't load this image from file!");
		success = false;
	}
	if(!mediumOver.loadFromFile("C:/Users/Admin/OneDrive/Pictures/medium over.png")) {
        printf("Can't load this image from file!");
		success = false;
	}
	if(!hardOver.loadFromFile("C:/Users/Admin/OneDrive/Pictures/hard over.png")) {
        printf("Can't load this image from file!");
		success = false;
	}
	if(!easyWinning.loadFromFile("C:/Users/Admin/OneDrive/Pictures/easy winning.png")) {
        printf("Can't load this image from file!");
		success = false;
	}
	if(!mediumWinning.loadFromFile("C:/Users/Admin/OneDrive/Pictures/medium winning.png")) {
        printf("Can't load this image from file!");
		success = false;
	}
	if(!hardWinning.loadFromFile("C:/Users/Admin/OneDrive/Pictures/hard winning.png")) {
        printf("Can't load this image from file!");
		success = false;
	}

	if (!back.loadFromFile("C:/Users/Admin/OneDrive/Pictures/backicon1.png")) {
         printf("Can't load this image from file!");
		success = false;
	}
	//load choice text
	SDL_Color textColor = { 255,255,255 };
	if (!easyChoice.loadFromRenderedText("EASY", textColor))
	{
		printf("Fail");
		success = false;
	}
	if (!mediumChoice.loadFromRenderedText("MEDIUM", textColor))
	{
		printf("Fail");
		success = false;
	}
	if (!hardChoice.loadFromRenderedText("HARD", textColor))
	{
		printf("Fail");
		success = false;
	}
	if (!play_again.loadFromRenderedText("Play Again", textColor)) {
        printf("Fail");
		success = false;
	}

	SDL_Color textcolor = { 255,0,0 };
	if (!easyChoiceColor.loadFromRenderedText("EASY", textcolor))
	{
		printf("Fail");
		success = false;
	}
	if (!mediumChoiceColor.loadFromRenderedText("MEDIUM", textcolor))
	{
		printf("Fail");
		success = false;
	}
	if (!hardChoiceColor.loadFromRenderedText("HARD", textcolor))
	{
		printf("Fail");
		success = false;
	}
	if (!play_againColor.loadFromRenderedText("Play Again", textcolor)) {
        printf("Fail");
		success = false;
	}
	return success;
}

void CreateBoard()
{
	srand(time(0));
	int mine = 0;
	//Initialization
	for (int i = 0;i < BOARD_SIZE_X;i++)
	{
		for (int j = 0;j < BOARD_SIZE_Y;j++)
		{
			sBoard[i][j] = 10;
			board[i][j] = 0;
		}
	}

	//Random mines in board
	while (mine < NumberOfMines)
	{
		int i = rand() % BOARD_SIZE_X;
		int j = rand() % BOARD_SIZE_Y;
		if (board[i][j] == 9) continue;
		board[i][j] = 9;
		mine++;
	}

	//Calculate the number of mines around each cell
	for (int i = 0;i < BOARD_SIZE_X;i++)
	{
		for (int j = 0;j < BOARD_SIZE_Y;j++)
		{
			if (board[i][j] == 9) continue;
			for (int x = -1;x <= 1;x++)
			{
				for (int y = -1;y <= 1;y++)
				{
					int xpos = i + x;
					int ypos = j + y;
					if (xpos < 0 || xpos>BOARD_SIZE_X - 1 || ypos<0 || ypos>BOARD_SIZE_Y - 1) continue;
					if (board[xpos][ypos] == 9) board[i][j]++;
				}
			}
		}
	}
}

void setButtonPosition()
{
	goBack.setPosition(10, 5);
	for (int i = 0;i < BOARD_SIZE_X;++i)
	{
		for (int j = 0;j < BOARD_SIZE_Y;++j)
		{
			Buttons[i][j].setPosition(i * TILE_SIZE + distance_x, j * TILE_SIZE + distance_y);
		}
	}
}


void createMenu()
{
	menuTheme.render(0, 0);
	menu.render(500, 360);
	menu1.render(500, 420);
	SDL_RenderPresent(renderer);
}

void createModeMenu()
{
	levelTheme.render(0, 0);
	easyChoice.render(300, 150);
	mediumChoice.render(300, 225);
	hardChoice.render(300, 300);
}

void createMenuAfterPlay(const int width1, const int height1, const int width2, const int height2) {
    play_again.render(width1, height1);
    menu1.render(width2, height2);
}

void showMenu()
{
	bool startInside = false;
	bool exitInside = false;
	bool isMenuShowing = true;
	SDL_Event event;
	createMenu();
	while (isMenuShowing)
	{
		while (SDL_PollEvent(&event) != 0)
		{
			if (event.type == SDL_QUIT)
			{
				mainLoop = false;
				isMenuShowing = false;
			}
			if (event.type == SDL_MOUSEBUTTONDOWN || event.type == SDL_MOUSEMOTION)
			{
				int x, y;
				SDL_GetMouseState(&x, &y);
				if (x > 500 && x < 500 + menu.getWidth() && y > 360 && y < 360 + menu.getHeight()) startInside = true;
				else startInside = false;
				if (x > 500 && x < 500 + menu1.getWidth() && y > 420 && y < 420 + menu1.getHeight()) exitInside = true;
				else exitInside = false;
				if (event.type == SDL_MOUSEBUTTONDOWN)
				{
					if (event.button.button == SDL_BUTTON_LEFT)
					{
						if (startInside == true)
						{
							start = true;
							isMenuShowing = false;
						}
						if (exitInside == true)
						{
							mainLoop = false;
							isMenuShowing = false;
							start = false;

						}
					}
				}
				if (event.type == SDL_MOUSEMOTION)
				{
					if (startInside == true)
					{
						menuColor.render(500, 360);
					}
					else menu.render(500, 360);
					if (exitInside == true)
					{
						menu1Color.render(500, 420);

					}
					else menu1.render(500, 420);
				}

			}
			SDL_RenderPresent(renderer);
		}
	}
}

void showModeChoice()
{
	bool easyInside = false;
	bool mediumInside = false;
	bool hardInside = false;
	SDL_Event event;
	createModeMenu();
	while (isChoosing)
	{
		while (SDL_PollEvent(&event) != 0)
		{
			if (event.type == SDL_QUIT)
			{
				mainLoop = false;
				isChoosing = false;
			}
			if (event.type == SDL_MOUSEBUTTONDOWN || event.type == SDL_MOUSEMOTION)
			{
				int x, y;
				SDL_GetMouseState(&x, &y);
				if (x > 300 && x < 300 + easyChoice.getWidth() && y > 150 && y < 150 + easyChoice.getHeight()) easyInside = true;
				else easyInside = false;
				if (x > 300 && x < 300 + mediumChoice.getWidth() && y > 225 && y < 225 + mediumChoice.getHeight()) mediumInside = true;
				else mediumInside = false;
				if (x > 300 && x < 300 + hardChoice.getWidth() && y > 300 && y < 300 + hardChoice.getHeight()) hardInside = true;
				else hardInside = false;
				if (event.type == SDL_MOUSEBUTTONDOWN)
				{
					if (event.button.button == SDL_BUTTON_LEFT)
					{
						if (easyInside == true)
						{
							isRunning = true;
							isChoosing = false;
							easyBackGround.render(0, 0);
							easy = true;
							medium = false;
							hard = false;
							SDL_SetWindowSize(window, 340, 460);
							setGameMode(9, 9, 12, 21, 163, 25, 80, 235, BOARD_SIZE_X, BOARD_SIZE_Y, NumberOfMines, mineCountLeft, CountTileLeft, distance_x, distance_y, digit_x, digit_y);
							CreateBoard();
						}
						if (mediumInside == true)
						{
							isRunning = true;
							isChoosing = false;
							easy = false;
							medium = true;
							hard = false;
							SDL_SetWindowSize(window, 560, 720);
							setGameMode(16, 16, 35, 21, 163, 25, 80, 430, BOARD_SIZE_X, BOARD_SIZE_Y, NumberOfMines, mineCountLeft, CountTileLeft, distance_x, distance_y, digit_x, digit_y);
							CreateBoard();
						}
						if (hardInside == true)
						{
							isRunning = true;
							isChoosing = false;
							hardBackGround.render(0, 0);
							easy = false;
							medium = false;
							hard = true;
							SDL_SetWindowSize(window, 1000, 800);
							setGameMode(30, 17, 90, 21, 163, 25, 80, 820, BOARD_SIZE_X, BOARD_SIZE_Y, NumberOfMines, mineCountLeft, CountTileLeft, distance_x, distance_y, digit_x, digit_y);
							CreateBoard();
						}
					}
				}
				if (event.type == SDL_MOUSEMOTION)
				{
					if (easyInside == true) easyChoiceColor.render(300, 150);
					else easyChoice.render(300, 150);
					if (mediumInside == true) mediumChoiceColor.render(300, 225);
					else mediumChoice.render(300, 225);
					if (hardInside == true) hardChoiceColor.render(300, 300);
					else hardChoice.render(300, 300);
				}
			}
			SDL_RenderPresent(renderer);
		}
	}
}


void handleEvent()
{
		SDL_Event e;
		while (SDL_PollEvent(&e) != 0)
		{
			if (e.type == SDL_QUIT)
			{
				isRunning = false;
				mainLoop = false;
			}
			goBack.handleEventBack(&e);
			for (int i = 0; i < BOARD_SIZE_X; i++)
			{
				for (int j = 0; j < BOARD_SIZE_Y; j++)
				{
					Buttons[i][j].handleEvent(&e);
				}
			}

		}
}

void reveal(int i, int j)
{
	if (sBoard[i][j] == 10 || sBoard[i][j] == 11)
	{
		if (sBoard[i][j] == 11)
		{
			return;
		}
		sBoard[i][j] = board[i][j];
		if (sBoard[i][j] != 9 && sBoard[i][j] != 0) {
                CountTileLeft--;
            if (easy) score += 5;
		    else if (medium) score += 10;
		    else if (hard) score += 25;
		    }
		if (sBoard[i][j] == 0)
		{
		    if (easy) score += 10;
		    else if (medium) score += 20;
		    else if (hard) score += 50;
			for (int x = -1;x <= 1;x++)
			{
				for (int y = -1;y <= 1;y++)
				{
					int xpos = i + x;
					int ypos = j + y;
					if (xpos < 0 || xpos > BOARD_SIZE_X - 1 || ypos < 0 || ypos > BOARD_SIZE_Y - 1) continue;
					reveal(xpos, ypos);
				}
			}
		}
		getScore();
	}
}
void isPlayerWinning()
{
	if (CountTileLeft == NumberOfMines) {
        if (easy) {
            isWinning = true;
            SDL_Color textColor = {255, 51, 51};
            SDL_Color textColor1 = {255, 255, 31};
            //Erase the temporary memory
            scoreFont.str( "" );
            scoreFont << "Your Score: " << score + 100;
            if(!scoreTheme.loadFromRenderedText(scoreFont.str().c_str(), textColor))
            {
                cout << "Unable to render score texture!" << endl;
            }
            youWin.str("");
            youWin << "You Win!!!";
            if (!easyFont.loadFromRenderedText(youWin.str().c_str(), textColor1)) {
                cout << "Unable to render score texture!" << endl;
            }
            easyWinning.render(0, 70);
            scoreTheme.render(45, 80);
            easyFont.render(97, 130);
            PlayAgain(0, 300, 250, 300);
        }
        else if (medium) {
            isWinning = true;
            SDL_Color textColor = {255, 51, 51};
            SDL_Color textColor1 = {255, 255, 31};
            //Erase the temporary memory
            scoreFont.str( "" );
            scoreFont << "Your Score: " << score + 200;
            if(!scoreTheme.loadFromRenderedText(scoreFont.str().c_str(), textColor))
            {
                cout << "Unable to render score texture!" << endl;
            }
            youWin.str("");
            youWin << "You Win!!!";
            if (!mediumFont.loadFromRenderedText(youWin.str().c_str(), textColor1)) {
                cout << "Unable to render score texture!" << endl;
            }
            mediumWinning.render(23, 110);
            scoreTheme.render(135, 160);
            mediumFont.render(196, 210);
            PlayAgain(30, 435, 400, 435);
        }
        else {
            isWinning = true;
            SDL_Color textColor = {255, 51, 51};
            SDL_Color textColor1 = {255, 255, 31};
            //Erase the temporary memory
            scoreFont.str( "" );
            scoreFont << "Your Score: " << score + 500;
            if(!scoreTheme.loadFromRenderedText(scoreFont.str().c_str(), textColor))
            {
                cout << "Unable to render score texture!" << endl;
            }
            youWin.str("");
            youWin << "You Win!!!";
            if (!hardFont.loadFromRenderedText(youWin.str().c_str(), textColor1)) {
                cout << "Unable to render score texture!" << endl;
            }
            hardWinning.render(150, 120);
            scoreTheme.render(320, 220);
            hardFont.render(380, 280);
            PlayAgain(250, 600, 600, 600);
        }
	}
}

void GameManager()
{
	//if we lose
	if (lose == true)
	{
		for (int i = 0;i < BOARD_SIZE_X;i++)
		{
			for (int j = 0;j < BOARD_SIZE_Y;j++)
			{
				Buttons[i][j].loseRender(i, j);
			}
		}
		 if (easy) {
            SDL_Color textColor = {255, 255, 31};
            SDL_Color textColor1 = {255, 51, 51};
            //Erase the temporary memory
            scoreFont.str( "" );
            scoreFont << "Your Score: " << score;
            if(!scoreTheme.loadFromRenderedText(scoreFont.str().c_str(), textColor))
            {
                cout << "Unable to render score texture!" << endl;
            }
            gameOver.str("");
            gameOver << "Game Over!";
            if (!easyFont.loadFromRenderedText(gameOver.str().c_str(), textColor1)) {
                cout << "Unable to render score texture!" << endl;
            }
            easyOver.render(0, 70);
            scoreTheme.render(20, 170);
            easyFont.render(70, 120);
            PlayAgain(0, 250, 250, 250);
        }
        else if (medium) {
                SDL_Color textColor = {255, 255, 31};
            SDL_Color textColor1 = {255, 51, 51};
            //Erase the temporary memory
            scoreFont.str( "" );
            scoreFont << "Your Score: " << score;
            if(!scoreTheme.loadFromRenderedText(scoreFont.str().c_str(), textColor))
            {
                cout << "Unable to render score texture!" << endl;
            }
            gameOver.str("");
            gameOver << "Game Over!";
            if (!mediumFont.loadFromRenderedText(gameOver.str().c_str(), textColor1)) {
                cout << "Unable to render score texture!" << endl;
            }
            mediumOver.render(13, 160);
            scoreTheme.render(130, 300);
            mediumFont.render(160, 250);
            PlayAgain(50, 400, 400, 400);
        }
        else {
            SDL_Color textColor = {255, 255, 31};
            SDL_Color textColor1 = {255, 51, 51};
            //Erase the temporary memory
            scoreFont.str( "" );
            scoreFont << "Your Score: " << score;
            if(!scoreTheme.loadFromRenderedText(scoreFont.str().c_str(), textColor))
            {
                cout << "Unable to render score texture!" << endl;
            }
            gameOver.str("");
            gameOver << "Game Over!";
            if (!hardFont.loadFromRenderedText(gameOver.str().c_str(), textColor1)) {
                cout << "Unable to render score texture!" << endl;
            }
            hardOver.render(150, 120);
            scoreTheme.render(350, 300);
            hardFont.render(400, 250);
            PlayAgain(250, 450, 600, 450);
        }
	}
}

void MineManager()
{
	int n = mineCountLeft;
	if (mineCountLeft < 10)
	{
		Digits.render(digit_x, digit_y, &Digitsprites[0]);
		for (int i = 0;i <= 9;i++)
		{
			if (i == mineCountLeft) Digits.render(digit_x + 28, digit_y, &Digitsprites[i]);
		}
	}

	else
	{
		int i = 0;
		while (n > 0)
		{
			int x = n % 10;
			n /= 10;
			Digits.render(digit_x + (1 - i) * 32, digit_y, &Digitsprites[x]);
			i++;
		}
	}
}
void getScore() {
    if(!lose && !isWinning)
    {
        SDL_Color textColor = {255, 255, 255};
        //Erase the temporary memory
        scoreFont.str( "" );
        scoreFont << "Score: " << score;
        if(!scoreTheme.loadFromRenderedText(scoreFont.str().c_str(), textColor))
        {
            cout << "Unable to render score texture!" << endl;
        }
        else {
            if (easy) {
                scoreTheme.render(50, 0);
            }
            else if (medium) {
               scoreTheme.render(150, 50);
            }
            else if (hard) {
                scoreTheme.render(350, 50);
            }
        }
    }
}

void mine()
{
    if(!lose && !isWinning)
    {
        SDL_Color textColor = {255, 255, 255};
        //Erase the temporary memory
        mine_left.str( "" );
        mine_left << "Mine Left: " << mineCountLeft;
        if(!mineLeft.loadFromRenderedText(mine_left.str().c_str(), textColor))
        {
            cout << "Unable to render mine left texture!" << endl;
        }
        else {
            if (easy) {
                mineLeft.render(50, 50);
            }
            else if (medium) {
                mineLeft.render(150, 100);
            }
            else if (hard) {
                mineLeft.render(350, 100);
            }
        }
    }
}
void PlayAgain(const int width1, const int height1, const int width2, const int height2)
{
    SDL_Event event;
    bool playAgainInside = false;
    bool exitInside = false;
    bool isMenuShowing = true;
    createMenuAfterPlay(width1, height1, width2, height2);
    while (isMenuShowing) {
		while (SDL_PollEvent(&event) != 0)
		{
			if (event.type == SDL_QUIT)
			{
				isMenuShowing = false;
				mainLoop = false;
				isChoosing = false;
			}
			if (event.type == SDL_MOUSEBUTTONDOWN || event.type == SDL_MOUSEMOTION)
			{
				int x, y;
				SDL_GetMouseState(&x, &y);
				if (x > width1 && x < width1 + play_again.getWidth() && y > height1 && y < height1 + play_again.getHeight()) playAgainInside = true;
				else playAgainInside = false;
				if (x > width2 && x < width2 + menu1.getWidth() && y > height2 && y < height2 + menu1.getHeight()) exitInside = true;
				else exitInside = false;
				if (event.type == SDL_MOUSEBUTTONDOWN)
				{
					if (event.button.button == SDL_BUTTON_LEFT)
					{
						if (playAgainInside == true)
						{
							playAgain = true;
							isChoosing = true;
							SDL_SetWindowSize(window, SCREEN_WIDTH, SCREEN_HEIGHT);
							showModeChoice();
							CreateBoard();
							setButtonPosition();
							lose = false;
							isWinning = false;
							score = 0;
							return;
						}
						if (exitInside == true)
						{
							playAgain = false;
							isChoosing = false;
							mainLoop = false;
							isMenuShowing = false;
							isRunning = false;
							return;
						}
					}
				}
				if (event.type == SDL_MOUSEMOTION)
				{
					if (playAgainInside == true)
					{
						play_againColor.render(width1, height1);
					}
					else play_again.render(width1, height1);
					if (exitInside == true)
					{
						menu1Color.render(width2, height2);

					}
					else menu1.render(width2, height2);
				}
			}
		}
		SDL_RenderPresent(renderer);
    }
}


void setGameMode(int x, int y, int n, int dx, int dy, int d1x, int d1y, int dtx, int& BOARD_SIZE_X, int& BOARD_SIZE_Y, int& NumberOfMines, int& mineCountLeft, int& CountTileLeft, int& distance_x, int& distance_y, int& digit_x, int& digit_y)
{
	BOARD_SIZE_X = x;
	BOARD_SIZE_Y = y;
	NumberOfMines = n;
	mineCountLeft = n;
	CountTileLeft = x * y;
	distance_x = dx;
	distance_y = dy;
	digit_x = d1x;
	digit_y = d1y;

	Buttons.resize(BOARD_SIZE_X);
	for (int i = 0;i < BOARD_SIZE_X;i++)
	{
		Buttons[i].resize(BOARD_SIZE_Y);
	}
	sBoard.resize(BOARD_SIZE_X);
	for (int i = 0;i < BOARD_SIZE_X;i++)
	{
		sBoard[i].resize(BOARD_SIZE_Y);
	}
	board.resize(BOARD_SIZE_X);
	for (int i = 0;i < BOARD_SIZE_X;i++)
	{
		board[i].resize(BOARD_SIZE_Y);
	}
}

void renderButton()
{
	for (int i = 0;i < BOARD_SIZE_X;i++)
	{
		for (int j = 0;j < BOARD_SIZE_Y;j++)
		{
			Buttons[i][j].render(i, j);
		}
	}
}

void renderGame()
{
		SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0);
		SDL_RenderClear(renderer);
		loseMusic = Mix_LoadMUS("C:/Users/Admin/Music/Loser sound effect.wav");
		winMusic = Mix_LoadMUS("C:/Users/Admin/Music/Winner sound effect.wav");
		click = Mix_LoadWAV("C:/Users/Admin/Music/Click sound effect.wav");
	if (easy == true || medium == true || hard == true)
	{
		if (easy == true)
		{
			easyTable.render(0, 50);
            easyBackGround.render(-30, 0);
		}
		if (medium == true)
		{
			mediumTable.render(0, 50);
			mediumBackGround.render(-30, 0);
		}
		if (hard == true)
		{
			hardTable.render(0, 50);
			hardBackGround.render(0, 0);
		}
	}
	renderButton();
	back.render(10, 5);
	MineManager();
	isPlayerWinning();
	GameManager();
	mine();
	getScore();
	SDL_RenderPresent(renderer);
}

void close()
{
	//Free loaded images
	Tiles_image.free();
	//Free global font
	TTF_CloseFont(gFont);
	gFont = NULL;
	//Destroy window
	SDL_DestroyRenderer(renderer);
	SDL_DestroyWindow(window);
	window = NULL;
	renderer = NULL;

	TTF_Quit();
	IMG_Quit();
	SDL_Quit();
}
