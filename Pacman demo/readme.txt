Python 2.7

search.py       Where all search algorithms reside. It shows you the implementaion of breath-first search, depth-first search and A*.

searchAgents.py	Where all search-based agents reside.

multiAgents.py  Where ReflexAgent, MinimaxAgent and other multiple agents reside.

pacman.py	The main file that runs Pacman games. This file describes a Pacman GameState type.

Demo 1: To play a game
python pacman.py

Demo 2: Finding a Fixed Food Dot using Depth First Search
python pacman.py -l tinyMaze -p SearchAgent
python pacman.py -l mediumMaze -p SearchAgent
python pacman.py -l bigMaze -z .5 -p SearchAgent

Demo 3: Breadth First Search
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5

Demo 4: A* search
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic

Demo 5: Eating All The Dots
python pacman.py -l trickySearch -p AStarFoodSearchAgent

Demo 6: Reflex Agent with 2 ghosts
python pacman.py --frameTime 0.1 -p ReflexAgent -k 2

Demo 7: Minimax Agent with 2 ghosts
python pacman.py --frameTime 0.1 -p MinimaxAgent -k 2

Demo 8: Microsoft's AI beats Ms. Pac-Man
https://techcrunch.com/2017/06/15/microsofts-ai-beats-ms-pac-man/

Note that pacman.py supports a number of options that can each be expressed in a long way (e.g., --layout) or a short way (e.g., -l). You can see the list of all options and their default values via:

python pacman.py -h

