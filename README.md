*This project has been created as part of the 42 curriculum by zdaouari, momahdam*

<table>
<tr><td bgcolor="#355872">

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
<<<<<<< HEAD
<tr><td bgcolor="#7AAACE">
=======
<tr><td bgcolor="#4e87b4">
>>>>>>> Ziad

____**Instructions**

Compilation/Interpretation:<br>
Run make at the root of the repository.

Installation:<br>
run this in terminal : ```pip install pygame```

Execution:<br>
```make run```
or simply ```make```.

</td></tr><tr>
<<<<<<< HEAD
<tr><td bgcolor="#79c7ff">
=======
<tr><td bgcolor="#2690db">
>>>>>>> Ziad

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


<<<<<<< HEAD
</table>
=======
</table>
>>>>>>> Ziad
