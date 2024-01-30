import pygame
import random

pygame.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 800, 800
TILE_SIZE = 30
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE

BORDER_THICKNESS = 1

BLACK = (0,0,0)
GRAY = (70,80,90)
GREEN = (34,139,34)
YELLOW = (196, 180, 84)
RED = (139, 34, 34)
PURPLE = (128,0,128)

screen = pygame.display.set_mode((WIDTH, HEIGHT))


FPS = 30

def main():
    running = True
    maze = Maze(screen, 0,0,int(WIDTH / TILE_SIZE) - 1,int(HEIGHT / TILE_SIZE) - 1)
    while running:
        clock.tick(FPS)
        screen.fill('#FFFFFF')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    if maze.maze_created:
                        maze = Maze(screen, 0, 0, int(WIDTH / TILE_SIZE) - 1, int(HEIGHT / TILE_SIZE) - 1)
                    maze.dfs(screen)
                    maze.defineNeighbors()
                if event.key == pygame.K_s and maze.maze_created:
                    maze.bfs(screen)
        maze.render(screen)
        

        pygame.display.update()
    pygame.quit()

class Node:

    def __init__(self, pos_x, pos_y):
        self.color = GRAY

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.matrix_x = 0
        self.matrix_y = 0

        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.top_border = NodeBorder(self.pos_x, self.pos_y, TILE_SIZE, BORDER_THICKNESS)
        self.bottom_border = NodeBorder(self.pos_x, self.pos_y + TILE_SIZE, TILE_SIZE, BORDER_THICKNESS)
        self.right_border = NodeBorder(self.pos_x + TILE_SIZE - BORDER_THICKNESS, self.pos_y, BORDER_THICKNESS, TILE_SIZE)
        self.left_border = NodeBorder(self.pos_x, self.pos_y, BORDER_THICKNESS, TILE_SIZE)

        self.visited = False
        self.explored = False

        self.neighbors = []
        self.neighbors_connected = []

        self.parent = None

    def render(self, background):
        pygame.draw.rect(background, self.color, (self.pos_x, self.pos_y, self.width, self.height))

        self.top_border.render(background)
        self.bottom_border.render(background)
        self.right_border.render(background)
        self.left_border.render(background)

class NodeBorder:
    def __init__(self, pos_x, pos_y, width, height):
        self.color = BLACK
        self.thickness = BORDER_THICKNESS
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height

    def render(self, background):
        pygame.draw.rect(background, self.color, (self.pos_x, self.pos_y, self.width, self.height))



class Maze:

    def __init__(self, background, initial_x, initial_y, final_x, final_y):
        self.maze = []
        self.total_nodes = 0
        self.maze_created = False
        self.initial_y = initial_x
        self.initial_x = initial_y
        self.final_y = final_x
        self.final_x = final_y

        x = 0
        y = 0

        for i in range(0, WIDTH, TILE_SIZE):
            self.maze.append([])
            for j in range(0, HEIGHT, TILE_SIZE):
                self.maze[x].append(Node(i, j))
                self.total_nodes+=1
                y+=1
                
            x+=1

        self.total_nodes-=2
        self.defineNeighbors()

    def addEdge(self, node, neighbor):
        node.neighbors_connected.append(neighbor)
        neighbor.neighbors_connected.append(node)
        

    def removeNeighborsVisited(self, node):
        node.neighbors = [x for x in node.neighbors if not x.visited]

    def defineNeighbors(self):
        for i in range(0,int(HEIGHT / TILE_SIZE)):
            for j in range(0, int(WIDTH / TILE_SIZE)):

                self.maze[i][j].matrix_x = i
                self.maze[i][j].matrix_y = j

                if 0 <= i < int(HEIGHT / TILE_SIZE) - 1 and 0 <= j < int(WIDTH / TILE_SIZE) - 1:
                    self.maze[i][j].neighbors.append(self.maze[i + 1][j]) # bottom
                    self.maze[i][j].neighbors.append(self.maze[i-1][j]) # top
                    self.maze[i][j].neighbors.append(self.maze[i][j+1]) # right
                    self.maze[i][j].neighbors.append(self.maze[i][j-1]) # left
                elif i == 0 and j == 0:
                    self.maze[i][j].neighbors.append(self.maze[i + 1][j]) # bottom
                    self.maze[i][j].neighbors.append(self.maze[i][j+1]) # right
                elif i == 0 and j == int(WIDTH / TILE_SIZE) - 1:
                    self.maze[i][j].neighbors.append(self.maze[i + 1][j]) # bottom
                    self.maze[i][j].neighbors.append(self.maze[i][j-1]) # left
                elif i == int(HEIGHT / TILE_SIZE) - 1 and j == int(WIDTH / TILE_SIZE):
                    self.maze[i][j].neighbors.append(self.maze[i-1][j]) # top
                    self.maze[i][j].neighbors.append(self.maze[i][j-1]) # left  
                elif i == int(HEIGHT / TILE_SIZE) - 1 and j == 0:
                    self.maze[i][j].neighbors.append(self.maze[i-1][j]) # top
                    self.maze[i][j].neighbors.append(self.maze[i][j+1]) # right
                elif i == 0:
                    self.maze[i][j].neighbors.append(self.maze[i + 1][j]) # bottom
                    self.maze[i][j].neighbors.append(self.maze[i][j+1]) # right
                    self.maze[i][j].neighbors.append(self.maze[i][j-1]) # left
                elif i == int(HEIGHT/TILE_SIZE) - 1:
                    self.maze[i][j].neighbors.append(self.maze[i-1][j]) # top
                    self.maze[i][j].neighbors.append(self.maze[i][j+1]) # right
                    self.maze[i][j].neighbors.append(self.maze[i][j-1]) # left
                elif j == 0:
                    self.maze[i][j].neighbors.append(self.maze[i + 1][j]) # bottom
                    self.maze[i][j].neighbors.append(self.maze[i-1][j]) # top
                    self.maze[i][j].neighbors.append(self.maze[i][j+1]) # right
                elif j == int(WIDTH / TILE_SIZE) - 1:
                    self.maze[i][j].neighbors.append(self.maze[i + 1][j]) # bottom
                    self.maze[i][j].neighbors.append(self.maze[i-1][j]) # top
                    self.maze[i][j].neighbors.append(self.maze[i][j-1]) # left

    def breakBorder(self, node: Node, neighbor: Node, color):
        # right:
        if(neighbor.matrix_x == node.matrix_x + 1) and (neighbor.matrix_y == node.matrix_y):
            node.right_border.color = color
            neighbor.left_border.color = color
        # left
        elif(neighbor.matrix_x == node.matrix_x - 1) and (neighbor.matrix_y == node.matrix_y):
            node.left_border.color = color
            neighbor.right_border.color = color
        #top
        elif(neighbor.matrix_x == node.matrix_x) and (neighbor.matrix_y == node.matrix_y - 1):
            node.top_border.color = color
            neighbor.bottom_border.color = color
        #bottom
        elif (neighbor.matrix_x == node.matrix_x) and (neighbor.matrix_y == node.matrix_y + 1):
            node.bottom_border.color = color
            neighbor.top_border.color = color

    def dfs(self, background):
            current_cell = random.choice(random.choice(self.maze))
            current_cell.visited = True
            current_cell.color = GREEN
            stack = [current_cell]
            nodes_visited = 1

            while nodes_visited != self.total_nodes or len(stack) != 0:
                
                self.removeNeighborsVisited(current_cell)
                if(len(current_cell.neighbors) > 0):
                    next_cell = random.choice(current_cell.neighbors)

                    self.breakBorder(current_cell, next_cell, GREEN)
                    self.addEdge(current_cell, next_cell)
                    current_cell = next_cell
                    current_cell.color = GREEN
                    current_cell.visited = True
                    stack.append(current_cell)
                    nodes_visited+=1
                else:
                    current_cell.color = YELLOW

                    if current_cell.top_border.color == GREEN:
                        current_cell.top_border.color = YELLOW
                    if current_cell.bottom_border.color == GREEN:
                        current_cell.bottom_border.color = YELLOW
                    if current_cell.right_border.color == GREEN:
                        current_cell.right_border.color = YELLOW
                    if current_cell.left_border.color == GREEN:
                        current_cell.left_border.color = YELLOW

                    if(len(stack) == 1):
                        current_cell = stack.pop()
                    else:
                        stack.pop()
                        current_cell = stack[-1]
                self.render(background)
                pygame.display.update()
            self.maze_created = True

            

    def bfs(self, background):
        initial_node = self.maze[self.initial_x][self.initial_y]
        final_node = self.maze[self.final_x][self.final_y]
        final_node.color = GREEN
        found = False
        queue = [initial_node]
        child_node = None

        while(len(queue) != 0 and not found):
            node = queue[0]
            node.color = RED
            queue.remove(queue[0])

            if node.top_border.color == YELLOW:
                node.top_border.color = RED
            if node.bottom_border.color == YELLOW:
                node.bottom_border.color = RED
            if node.right_border.color == YELLOW:
                node.right_border.color = RED
            if node.left_border.color == YELLOW:
                node.left_border.color = RED

            for neighbor in node.neighbors_connected:
                if neighbor.explored == False:
                    neighbor.parent = node
                    neighbor.explored = True
                    queue.append(neighbor)
                if(neighbor.pos_x == final_node.pos_x and neighbor.pos_y == final_node.pos_y):
                    child_node = neighbor
                    found = True
            self.render(background)
            pygame.display.update()

        found = False
        while not found:
            child_node.color = PURPLE

            if child_node.top_border.color == YELLOW or child_node.top_border.color == RED:
                child_node.top_border.color = PURPLE
            if child_node.bottom_border.color == YELLOW or child_node.bottom_border.color == RED:
                child_node.bottom_border.color = PURPLE
            if child_node.right_border.color == YELLOW or child_node.right_border.color == RED:
                child_node.right_border.color = PURPLE
            if child_node.left_border.color == YELLOW or child_node.left_border.color == RED:
                child_node.left_border.color = PURPLE

            child_node = child_node.parent
            if(child_node.pos_x == initial_node.pos_x and child_node.pos_y == initial_node.pos_y):
                found = True
                child_node.color = GREEN
            self.render(background)
            pygame.display.update()
        
                


    def render(self, background):
        for i in range(0, int(HEIGHT / TILE_SIZE)):
            for j in range (0, int(WIDTH / TILE_SIZE)):
                self.maze[i][j].render(background)

if __name__ == '__main__':
    main()
        