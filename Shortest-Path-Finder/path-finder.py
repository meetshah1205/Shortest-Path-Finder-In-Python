import curses
from curses import wrapper
import heapq
import time

maze = [
    ["#", "", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", "#", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", "O", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", "X", "#", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", " ", "#"]
]

def print_maze(maze, stdscr, path=[]):
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j*2, "X", RED)
            else:
                stdscr.addstr(i, j*2, value, BLUE)

def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j
    return None

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_paths(maze, stdscr, num_paths=3):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)
    end_pos = find_start(maze, end)

    open_set = []
    heapq.heappush(open_set, (0, start_pos))
    came_from = {}
    g_score = {start_pos: 0}
    f_score = {start_pos: heuristic(start_pos, end_pos)}
    
    visited = set()
    paths_found = []

    while open_set and len(paths_found) < num_paths:
        _, current = heapq.heappop(open_set)
        visited.add(current)

        if current == end_pos:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start_pos)
            path.reverse()
            paths_found.append(path)
            
            # Reset open set and visited to find next path
            open_set = []
            heapq.heappush(open_set, (0, start_pos))
            came_from = {}
            g_score = {start_pos: 0}
            f_score = {start_pos: heuristic(start_pos, end_pos)}
            visited = set()

            continue

        stdscr.clear()
        print_maze(maze, stdscr, visited)
        time.sleep(0.1)
        stdscr.refresh()

        for neighbor in find_neighbors(maze, current[0], current[1]):
            if neighbor in visited:
                continue

            tentative_g_score = g_score[current] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end_pos)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return paths_found

def find_neighbors(maze, row, col):
    neighbors = []

    if row > 0 and maze[row - 1][col] != "#":  # UP
        neighbors.append((row - 1, col))
    if row + 1 < len(maze) and maze[row + 1][col] != "#":  # DOWN
        neighbors.append((row + 1, col))
    if col > 0 and maze[row][col - 1] != "#":  # LEFT
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]) and maze[row][col + 1] != "#":  # RIGHT
        neighbors.append((row, col + 1))

    return neighbors

def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    paths = find_paths(maze, stdscr, num_paths=3)
    
    for path in paths:
        stdscr.clear()
        print_maze(maze, stdscr, path)
        stdscr.getch()

wrapper(main)
