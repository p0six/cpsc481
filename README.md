--------------------------
CPSC 481 PACMAN AI PROJECT
--------------------------
**Project Lead: Mike Romero**

**Partner: Diego Franchi**

**Partner: Miles McCloskey**

Date: 5/6/18

The main idea behind our implementation of the  game is to follow similar logic of the original game's ghosts,
while using more modern AI. At the start of this project, we added our version of the pacman gameboard.
We have added the terminal options of -o and --originalGhosts which we modified 
to utilize the A* algorithm within the logic of each of our ghosts classes. Before 
implementing the A* algorithm with manhattan distance, we used BFS, and we drew the 
path of the various ghosts in order to see our algorithmic path to PACMAN. Towards 
the end of our project we were able to update the multiagents.py file and pacman.py 
file to handle and implement a machine learned version of pacman's artificial intelligence 
by taking into account 5 weighted features that dynamically change at during runtime and 
more specifically after each and every move. 

--------------------------
Files Modified 
--------------------------
####commands.txt
Created commands that initialize our Ghosts in the game. This document contains example
 executions of the program and how we are running the game with options that we have created. 
 The game layout is the classic PAC-MAN board minus the warp pipes. Ghost AI used our classic 
 ghost implementations.

   *Trigger our Ghost Agents... Blinky / Pinky / Inky / Clyde, using the pacmanClassic map we created.*
    
    python pacman.py -l pacmanClassic -o

   *Allow PacMan to play against Blinky and draw Blinky's intended path....*
    
    python pacman.py -l pacmanClassic --blinky  -z .5 -d -p CPSC481Agent

   *PacMan play's against all four ghosts, not drawing intended paths.*
    
    python pacman.py -l pacmanClassic -o -z .5 -p CPSC481Agent

   *Provide some weights to start reinforcementLearning from... play 100 games quitely with CPSC481Agent against Blinky*
   
    python pacman.py --blinky -p CPSC481Agent --reinforcementLearning 1,1,1,1,1,1,1  -l smallClassic -n 100 -q

   *Watch a fairly intelligent PAC-MAN completely fail against all four of our ghosts*
    
    python pacman.py -o -p CPSC481Agent --reinforcementLearning 1,1,1,1,1,1,1 -l pacmanClassic


##ghostAngents.py
Created separate classes for each AI ghost to implement the classic ghost AIs from the famous PAC-MAN game. 
These ghosts currently use a state space search to minimize the distance between PAC-MAN and the ghost 
itself using all legal paths. We currently use an A* algorithm with a manhattan distance heuristic for path finding.
Eeach ghost class is capable of drawing a visible path to their target location for presentation and debugging. 

Blinky (red ghost) always targets PAC-MAN's position

Pinky targets 4 legal positions ahead of PAC-MAN's current vector. 

Inky (blue ghost) draws a target based on the position 2 spots ahead of PAC-MAN and Inky's current position. He then 
draws two times the length of that vector for his target tile.

Clyde (orange ghost) targets PAC-MAN's position until he is within 8 blocks away at which point it will retreat to the
corner until it is no longer 8 blocks from PAC-MAN, at which point it immediately begins chasing PAC-MAN again.


##graphicsDisplay.py
Modified color of ghosts to better match the original PAC-MAN game.

##pacman.py
This file controls the creation of the game model. We have modified it to create our ghost classes with 
appropriate AI modeled after the original PAC-MAN ghost behaviors, triggered using the "-o" command line argument.
We added a flag -d to display the paths ghosts intended targets. Also, we made it so you can play against each on or 
as many of the ghosts that you would like to play against being specified by their names like --blinky or --pinky. Lastly,
we added --reinforcementLearning in with a set of 5 weights. Modified to support getBetterPacmanPosition().

##searchAgents.py
Added a function that returns the set of directions from start location (x1,y1) to end location (x2, y2). 
This is converted by the ghost class into a series of cell coordinates representing a path that is then drawn
 onto the screen displaying the ghosts intended path towards its target.

##util.py
Implemented the Euclidean distance equation to be used by our ghost AI search algorithms.
 We may or may not go forward with euclidean distance in our final version.
 
##multiAgents.py
We added cpsc481 agent to drive the behavior of Pacman to deal with a set of weights which correspond to specific
Qlearning features. These set of weights dynamically change the behavior of Pacmans decisions or turns based 
on the location of the ghosts, food, power pellets, and more.  PAC-MAN now uses getBetterPacmanActions() which
removes the "Stop" direction as an option, making him seem more aggressive.

##game.py
Modified to allow for the setting and the getting of weights which are being used in reinforcement learning. Essentially, 
it was modified to verify that the weights are always kept on the game state. These changes are allow being made when the 
--reinforcementLearning command is being set or called in the terminal. Added a getBetterPacmanActions() function which
removes his ability to stop, and makes him seem more aggressive.

##search.py 
We created the A* search ghost function which is used for path finding 

--------------------------
Files Created
--------------------------
##pacmanClassic.lay
This is a layout file built to match the classic PAC-MAN map. 
We created this as a way to make this version of PAC-MAN to feel more like the original.