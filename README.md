*This project has been created as part of the 42 curriculum by zdaouari, momahdam*

<table>
<tr>

____**Description**

***<li>Project description***:
<br>A-Maze-ing is a technical exploration into graph theory and procedural generation. The primary objective of this project is to develop a software suite capable of generating "perfect" mazes—labyrinths where every cell is reachable and exactly one unique path exists between any two points—while adhering to strict algorithmic constraints.

<u>Core Objectives</u>:

The project focuses on three main pillars:

Algorithmic Generation: Implementing a specific generation algorithm (such as Randomized Prim's, Kruskal's, or Recursive Backtracking) to create complex, non-biased grid structures.

Validation & Solvability: Ensuring the generated data structure is logically sound, contains no isolated "islands," and provides a guaranteed path from a defined entry point to an exit.

Data Representation: Parsing and interpreting external configuration files to define maze dimensions, seeds for randomness, and structural parameters.

<u>Technical Overview</u>

At its heart, the project treats the maze as a spanning tree of a 2D grid graph. By manipulating the edges (walls) between vertices (cells), the program transforms a solid block of cells into a navigable network. The challenge lies in managing memory efficiently during the generation process and ensuring the software remains performant even as the grid dimensions ($N \times M$) scale upward.

***<li>Description of the game***

Default Mode: <br>The maze is generated using a DFS algorithm, solved using BFS, and rendered using the curses library for terminal-based output.

Player Mode:
In Player Mode, you select your character (Monkey 🐒 or Rabbit 🐇) before the game begins. This mode allows you to navigate the generated maze manually using the keyboard. Your goal is to reach the exit while managing resources and navigating through dynamic visual effects. You are given three hearts ❤️ shown in the health bar; if you lose them all, it is Game Over.


🕹️ Controls & Navigation

Movement: Use W, A, S, D keys to move the player through the maze paths.
Once the player hits the wall, a heart is removed from his Health bar.
</td></tr><tr>
<tr>

____**Instructions**

Compilation/Interpretation:<br>
Run make at the root of the repository.

Installation:<br>
run this in terminal : ```make install```

Execution:<br>
```make run```
or simply ```make```.

</td></tr><tr>
<tr>


____**Resources**


Official Python curses HOWTO: <a>Curses Programming with Python</a> — The primary reference for terminal-independent screen painting and keyboard handling.
watch this out : <a>https://www.youtube.com/watch?v=BK7YvpTT4Sw</a>

GeeksforGeeks: <a>Curses Module in Python</a> — Comprehensive guide on windows, colors, and user input handling in TUIs.

Real Python: <a>Mazes in Python: Build, Visualize, Store, and Solve</a> — A deep dive into representing mazes as graphs and applying pathfinding algorithms.

Stuff With Stuff: <a>Rooms and Mazes</a> — An excellent article on procedural dungeon/maze generation logic.

Algorithm Visualizations
VisuAlgo: <a>Graph Traversal (DFS/BFS)</a> — Interactive animations showing how stack-based (DFS) and queue-based (BFS) traversals differ.

<u>AI Usage</u>

AI was utilized as a collaborative tool throughout this project for the following tasks:

Documentation: <br>Assistance in structuring this README to meet the specific requirements of the 42 curriculum.




In accordance with the project management requirements the subject, our team utilized a collaborative approach where responsibilities were divided based on technical specializations to ensure a cohesive workflow. Momahdam spearheaded the core generation engine by implementing the Randomized DFS algorithm and creating the fluid maze animations and rendering systems; additionally, they managed the input parsing logic, final branch merging, and the structural integrity of the project's documentation, and cells pattern.<br>Simultaneously, Zdaouari focused on the game logic and the Player Mode enhancements, integrating the ASCII visuals, bonus mechanics, and the BFS solver for automated pathfinding. He also handled the technical translation of the maze into hexadecimal output files, while maintaining the build system through a robust Makefile.

Initially, our planning followed a linear trajectory, but we evolved into an agile cycle to better handle the complexities of the hexadecimal transformations and rendering synchronization. What worked particularly well was our modular code structure, which allowed the generation and solving algorithms to be tested independently of the UI. While our communication was consistent, we identified that earlier integration of the curses and pygame components could have streamlined the final debugging phase. To maintain our workflow, we relied on Git for version control<br>

**Algorithm Choice**
:We implemented Recursive Backtracking (DFS) to ensure a "perfect" maze with no loops. We chose this because it creates long, winding corridors with fewer dead-ends, providing a more challenging and aesthetic experience for the Player Mode.

**Code Reusability**
:The BFS Solver and the core Grid Data Structure are designed as independent modules. They can be reused in any grid-based pathfinding project by simply importing the logic without the curses rendering dependency.

**Project Management**
:Team Roles
Momahdam managed the DFS algorithm, rendering animations, parsing logic, and documentation. zdaouari handled the game logic, BFS pathfinding, ASCII/Hex transformations, and the build system via the Makefile.

**Planning Evolution**
:Our initial plan was a linear "Logic-first" approach, but it evolved into an agile cycle to handle hexadecimal conversion hurdles. This shift allowed us to refine the player mechanics while simultaneously perfecting the generation engine.

**Retrospective**
:Our modular architecture worked exceptionally well, allowing for independent testing of algorithms. However, we could improve our early-stage integration testing to avoid the minor UI synchronization issues we faced near the deadline, hearthsystem and peace 18 stuffs.
</td></tr>

</table>