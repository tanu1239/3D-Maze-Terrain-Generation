# 3D Maze Terrain Generation

A generative escape game offering one and two-player game modes equipped with 3D maze terrain generation.
The user will be spawned into a 3D maze generated with raycasting. 

Along with the player, several monsters are also spawned in the maze. 
Higher levels have more complex mazes with more monsters. In various
chests distributed throughout the maze, the user can gain access to swords, health boosters,
and shields. There are different types of swords (wooden, stone, iron, golden, and diamond)
which do varying levels of damage when attacking the monsters with better swords being rarer. 
The swords can be used to fight the monsters and also the other player in 2-player mode. Health boosters 
replenish health and shields protect against damage from monsters and also the other player in 2-player mode.
Adversarial search is implemented, allowing the monsters to chase the user.

The user must escape the maze in order to win (the first user to escape the maze in 2-player
mode is the winner). Lastly, in build-your-own-maze mode, the user can create a personalized
maze by specifying size, wall locations, monster spawn, chest spawn and player spawn
locations. The user can then use the maze they built and play it in 1-player or 2-player mode.
