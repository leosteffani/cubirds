Creating your game

1. Create and activate a virtual environment (in the folder that contains the folders dog and config);
python -m venv venv
. .\venv\Scripts\activate

2. Execute 'pip install -r ..\requirements.txt' (to install the libraries used by the framework);

3. Go to folder 'config' and follow the instructions therein;

4. DEVELOP YOUR GAME;

5. Execute 'pip freeze > requirements.txt' (to update requirements.txt with the libraries used by your game);

6. To distribute your game: python interface.py

	a. Remove the folder of the virtual environment;
	b. Compact and send your game with the following instrucions:
		I. Create and activate a virtual environment;
		II. Execute pip 'install -r requirements.txt';
		III. To run the game:  <name_of_your_game>.py.


