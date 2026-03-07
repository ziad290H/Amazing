<table bgcolor="#0000">
<tr><td>

<h2><i>This project has been created as part of the 42 curriculum by zdaouari, momahdam</i></h2>

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
<tr><td>

____**Instructions**

Compilation/Interpretation:<br>
Run make at the root of the repository.

Installation:<br>
run this in terminal : ```make install```<br>
all needed modules and packages will be installed using makefile, make sure to execute it at the root of this repository.

Execution:
```make run```
<br>or simply ```make```

Debuging:
<br>run this in terminal : ```make debug``` if you want to debug

Cleaning aka remove cache:
<br>use this cmd at the root of the repo : ```make clean```

Packaging:
<br><ul>
<li>Build the Archive :
<br>

```python3 -m build```</li>

<li>Install compressed mazegen :</<br>

```pip install dist/mazegen_zdaouari-1.0.0.tar.gz```</li>

<li>Check of the package building and <u>Run :</u>
<br>

```python3 a_maze_ing.py config.txt```</li>






</ul>
</td></tr><tr>
<tr><td>





____**Resources**


Official Python curses HOWTO: <a>Curses Programming with Python</a> — The primary reference for terminal-independent screen painting and keyboard handling.
watch this out : <a>https://www.youtube.com/watch?v=BK7YvpTT4Sw</a>

GeeksforGeeks: <a>Curses Module in Python</a> — Comprehensive guide on windows, colors, and user input handling in TUIs.

Real Python: <a>Mazes in Python: Build, Visualize, Store, and Solve</a> — A deep dive into representing mazes as graphs and applying pathfinding algorithms.

Stuff With Stuff: <a>Rooms and Mazes</a> — An excellent article on procedural dungeon/maze generation logic.

Algorithm Visualizations
VisuAlgo: <a>Graph Traversal (DFS/BFS)</a> — Interactive animations showing how stack-based (DFS) and queue-based (BFS) traversals differ.


DFS Visualization:
<br>
<a>https://www.youtube.com/shorts/L1vGm2_cPU0</a><br>
<a>https://www.youtube.com/shorts/jKnrGwqjlWo</a><br>
<a>https://www.youtube.com/shorts/n6U5kbez_WM</a>

BFS VS DFS Animation:<br>
<a>https://www.youtube.com/shorts/1-elk8F8_UM</a>

<u>AI Usage</u>

AI was utilized as a collaborative tool throughout this project for the following tasks:

Documentation: <br>Assistance in structuring this README to meet the specific requirements of the 42 curriculum.

<tr><td>

____**Additional section**


In accordance with the project management requirements the subject, our team utilized a collaborative approach where responsibilities were divided based on technical specializations to ensure a cohesive workflow. Momahdam spearheaded the core generation engine by implementing the Randomized DFS algorithm and creating the fluid maze animations and rendering systems; additionally, they managed the input parsing logic, final branch merging, and the structural integrity of the project's documentation, and cells pattern.<br>Simultaneously, Ziad focused on the game logic and the Player Mode enhancements, integrating the ASCII visuals, bonus mechanics, and the BFS solver for automated pathfinding. He also handled the technical translation of the maze into hexadecimal output files, while maintaining the build system through a robust Makefile.

Initially, our planning followed a linear trajectory, but we evolved into an agile cycle to better handle the complexities of the hexadecimal transformations and rendering synchronization. What worked particularly well was our modular code structure, which allowed the generation and solving algorithms to be tested independently of the UI. While our communication was consistent, we identified that earlier integration of the curses and pygame components could have streamlined the final debugging phase. To maintain our workflow, we relied on Git for version control<br>

**Algorithm Choice**
:We implemented Recursive Backtracking (DFS) to ensure a "perfect" maze with no loops. We chose this because it creates long, winding corridors with fewer dead-ends, providing a more challenging and aesthetic experience for the Player Mode.

**Code Reusability**
:The BFS Solver and the core Grid Data Structure are designed as independent modules. They can be reused in any grid-based pathfinding project by simply importing the logic without the curses rendering dependency.

**Project Management**
:Team Roles
Momahdam managed the DFS algorithm, rendering animations, parsing logic, and documentation. <br>
Ziad handled the game logic, BFS pathfinding, ASCII/Hex transformations, and the build system via the Makefile.

**Planning Evolution**
:Our initial plan was a linear "Logic-first" approach, but it evolved into an agile cycle to handle hexadecimal conversion hurdles. This shift allowed us to refine the player mechanics while simultaneously perfecting the generation engine.

**Retrospective**
:Our modular architecture worked exceptionally well, allowing for independent testing of algorithms. However, we could improve our early-stage integration testing to avoid the minor UI synchronization issues we faced near the deadline, hearthsystem and peace 18 stuffs.

**Tools**
<br>For this project, I used several tools and libraries to implement and visualize the maze generator. The core logic was written in **Python**, using built-in modules such as **random** for randomized maze generation and **typing** to improve code readability and maintainability through type hints. To create the interactive terminal visualization, I used the **curses** library, which allows efficient screen updates and keyboard input handling in a text-based interface. Additionally, **Git** was used for version control to track changes during development, and **GitHub** for hosting and sharing the project. These tools helped structure the code, simplify debugging, and provide a smooth visualization of the maze generation and solving process.
</tr>
</td></tr>

<tr bgcolor="#1877bbb2"><td>

In accordance with the project management requirements the subject, our team utilized a collaborative approach where responsibilities were divided based on technical specializations to ensure a cohesive workflow. Momahdam spearheaded the core generation engine by implementing the Randomized DFS algorithm and creating the fluid maze animations and rendering systems; additionally, they managed the input parsing logic, final branch merging, and the structural integrity of the project's documentation, and cells pattern.<br>Simultaneously, Ziad focused on the game logic and the Player Mode enhancements, integrating the ASCII visuals, bonus mechanics, and the BFS solver for automated pathfinding. He also handled the technical translation of the maze into hexadecimal output files, while maintaining the build system through a robust Makefile.

Initially, our planning followed a linear trajectory, but we evolved into an agile cycle to better handle the complexities of the hexadecimal transformations and rendering synchronization. What worked particularly well was our modular code structure, which allowed the generation and solving algorithms to be tested independently of the UI. While our communication was consistent, we identified that earlier integration of the curses and pygame components could have streamlined the final debugging phase. To maintain our workflow, we relied on Git for version control<br>

**Algorithm Choice**
:We implemented Recursive Backtracking (DFS) to ensure a "perfect" maze with no loops. We chose this because it creates long, winding corridors with fewer dead-ends, providing a more challenging and aesthetic experience for the Player Mode.

**Code Reusability**
:The BFS Solver and the core Grid Data Structure are designed as independent modules. They can be reused in any grid-based pathfinding project by simply importing the logic without the curses rendering dependency.

**Project Management**
:Team Roles
Momahdam managed the DFS algorithm, rendering animations, parsing logic, and documentation. Ziad handled the game logic, BFS pathfinding, ASCII/Hex transformations, and the build system via the Makefile.

**Planning Evolution**
:Our initial plan was a linear "Logic-first" approach, but it evolved into an agile cycle to handle hexadecimal conversion hurdles. This shift allowed us to refine the player mechanics while simultaneously perfecting the generation engine.

**Retrospective**
:Our modular architecture worked exceptionally well, allowing for independent testing of algorithms. However, we could improve our early-stage integration testing to avoid the minor UI synchronization issues we faced near the deadline, hearthsystem and peace 18 stuffs.
</td></tr>

</table>
