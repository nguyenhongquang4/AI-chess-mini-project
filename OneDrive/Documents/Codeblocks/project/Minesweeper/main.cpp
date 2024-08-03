#include "Texture.h"
#include "Button.h"
#include "Variables.h"
#include "mainFunction.h"
using namespace std;

int main(int argc, char* argv[]) {

    if (!init())
	{
		printf("Failed to initialize!\n");
	}
	else
	{
		if (loadmedia())
		{
			if (loadMenuMedia())
			{
				showMenu();
				while (mainLoop) {
					if (isChoosing)
					{
						showModeChoice();
					}
					//if(customMode) CustomMode();
					while (isRunning)
					{
						handleEvent();
						setButtonPosition();
						renderGame();
					}
				}
			}

		}
	}
	//Free resources and close SDL
	close();
	return 0;
}
