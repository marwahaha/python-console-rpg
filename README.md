# python-console-rpg

Setup Requirement:
-Python 3.6 or 3.7
-Termcolor and Random libraries (pip install termcolor, etc.)

Start the game by navigating to the folder is located in and typing `python game.py` (in the console)


Game Layout:

All character and object classes should go in models.py

Anything related to the core game functioning should be in game.py. For the most part this should be pretty simple.

Any code not specfic to a character or game loop should be in utils.py, this might have to be expanded later.

Variations of Monsters and Weapons should be created in the respective files monster.py and weapons.py. Other equipment and objects should follow similar structures.



use the `message('string', 'color')` function to display messages to the chat box. This has the optional flag `returnFormatted`, which returns the formatted string rather then prints it to the console. You can use this to print multiple formatted strings using `messageDirect(args)` (This only accepts strings that have already been foramatted using `message()`). Do not use `print()`. The reason for this is that the game can be later swapped to a different display method and we only have to change one message() method, rather then hunt down 8000 print statements.

Other Thoughts:

All numbers should use whole numbers. Decimals are the devils children.

If you need to add something specific to only Monsters or Players, put that in the monster or player model. Only add to the base character class if everything needs it.

You can have more then 1 player in the game, with the goal in mind of eventually having full parties.

Traversing rooms and interacting with objects isnt implemented yet, except for the equipWeapon() method on players.


Roadmap:

-Add abilties

-Add multiple monster types

-Add more player functions

-Build out character model to include experience, ability power, and full stats list

-Build out armor and equipment models

-Enable armor equiping for character

-Implement player inventory

-Build map and navigation system, room based

-Implement 2 differnt game loops, exploration and combat

-Add multiple party members

-Add quests

-Add shops and bank

-Decide on UI type, either ncurses type display, or port everything to a graphical framework
