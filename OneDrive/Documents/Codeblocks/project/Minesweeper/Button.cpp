#include "Variables.h"
#include "Button.h"
#include "mainFunction.h"

LButton::LButton()
{
	mPosition.x = 0;
	mPosition.y = 0;
}

void LButton::setPosition(int x, int y)
{
	mPosition.x = x;
	mPosition.y = y;
}

void LButton::handleEventBack(SDL_Event* e)
{
	if (e->type == SDL_MOUSEBUTTONDOWN)
	{
		int x, y;
		SDL_GetMouseState(&x, &y);
		bool inside = true;
		//Mouse is left of the button
		if (x < mPosition.x)
		{
			inside = false;
		}
		//Mouse is right of the button
		else if (x > mPosition.x + 50)
		{
			inside = false;
		}
		//Mouse above the button
		else if (y < mPosition.y)
		{
			inside = false;
		}
		//Mouse below the button
		else if (y > mPosition.y + 50)
		{
			inside = false;
		}
		if (inside)
		{
			if (e->button.button == SDL_BUTTON_LEFT)
			{
				SDL_SetWindowSize(window, SCREEN_WIDTH, SCREEN_HEIGHT);
				isRunning = false;
				isChoosing = true;
				isWinning = false;
				lose = false;
				easy = false;
				medium = false;
				hard = false;
				score = 0;
			}
		}
	}
}

void LButton::handleEvent(SDL_Event* e)
{
	//If mouse event happened
	if (e->type == SDL_MOUSEMOTION || e->type == SDL_MOUSEBUTTONDOWN || e->type == SDL_MOUSEBUTTONUP)
	{
		//Get mouse position
		int x, y;
		SDL_GetMouseState(&x, &y);

		int i =  ( x - distance_x)  / TILE_SIZE;
		int j = (y - distance_y) / TILE_SIZE;

		//Check if mouse is in button
		bool inside = true;

		//Mouse is left of the button
		if (x < mPosition.x)
		{
			inside = false;
		}
		//Mouse is right of the button
		else if (x > mPosition.x + TILE_SIZE)
		{
			inside = false;
		}
		//Mouse above the button
		else if (y < mPosition.y)
		{
			inside = false;
		}
		//Mouse below the button
		else if (y > mPosition.y + TILE_SIZE)
		{
			inside = false;
		}

		//Mouse is inside button
		if (inside)
		{
			if (e->type == SDL_MOUSEBUTTONDOWN)
			{

				//Set mouse clicked
				switch (e->button.button)
				{
				case SDL_BUTTON_LEFT:
				{
					reveal(i, j);
					if (CountTileLeft == NumberOfMines)
					{
						Mix_PlayMusic(winMusic, 1);
					}
					if (sBoard[i][j] == 9)
					{
						lose = true;
						Mix_PlayMusic(loseMusic, 1);
					}
					else
					{
						Mix_PlayChannel(-1, click, 0);
					}
					break;
				}
				case SDL_BUTTON_RIGHT:
				{
					Mix_PlayChannel(-1, click, 0);
					if (sBoard[i][j] >= 10)
					{
						if (sBoard[i][j] == 11)
						{
							sBoard[i][j] = 10;
							mineCountLeft++;
						}
						else
						{
							sBoard[i][j] = 11;
							mineCountLeft--;
						}
					}
					else break;
					break;
				}
				}
			}
		}
	}
}

void LButton::render(int i, int j)
{
	//Show current button sprite
	Tiles_image.render(mPosition.x, mPosition.y, &Tilesprites[sBoard[i][j]]);
}
void LButton::loseRender(int i, int j)
{
	//Show all button sprite
	Tiles_image.render(mPosition.x, mPosition.y, &Tilesprites[board[i][j]]);
}
