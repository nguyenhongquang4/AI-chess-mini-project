#pragma once
#pragma once
#ifndef BUTTON_H
#define BUTTON_H

#include <SDL.h>


class LButton
{
public:
	//Initializes internal variables
	LButton();

	//Sets top left position
	void setPosition(int x, int y);

	//set button in game
	void handleEventAgain(SDL_Event* e);
	void handleEventBack(SDL_Event* e);

	//Handles mouse event
	void handleEvent(SDL_Event* e);

	//Shows button sprite
	void render(int i, int j);

	//Shows button sprite when we lose
	void loseRender(int i, int j);

private:
	//Top left position
	SDL_Point mPosition;
};
#endif
