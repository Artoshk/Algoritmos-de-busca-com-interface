from operator import itemgetter
import random
import pygame
from queue import PriorityQueue
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import os
from csv import DictWriter
from uuid import uuid4
import subprocess as s

BTTN_W = 140
BTTN_H = 40
GRID_COUNT = 50
WIDTH = 700
HEIGHT = WIDTH+BTTN_H
ALGORITHMS = ["A*", "Busca em Largura - BFS", "Busca em Profundidade - DFS","Busca em Profundidade Aleatória - DFSA", "Busca Gulosa Pela Melhor Escolha - BGME", "Busca Pela Melhor Escolha - BME", "Busca de Custo Uniforme - BCU", "Busca de Aprofundamento Iterativo - IDFS", "Busca Bidirecional"]
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Buscas")

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
ORANGE = (255,165,0)
GREY = (128,128,128)
DARK_GREY = (64,64,64)
LIGHT_GREY = (200,200,200)
TURQUOISE = (64,224,208)
EMERALD = (4,99,7)
LIGHT_GREEN = (127,255,0)

hash = ""
total_caminho = 0
expandidos = 0

pygame.init()
class Node:

    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.visited = False
        self.dualVisited = [False, False]
        self.weight = 0

    def __repr__(self) -> str:
        return f"x: {self.x} y: {self.y} color: {self.color} visited: {self.visited}"
    
    def get_pos(self):
        return self.row, self.col

    def is_barrier(self):
        return self.color == BLACK
    
    def reset(self):
        self.color = WHITE

    def make_weight(self):
        self.color = LIGHT_GREY
        self.weight = 500

    def make_closed(self):
        global expandidos
        expandidos += 1
        self.color = GREEN
    
    def make_open(self):
        self.color = EMERALD
    
    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE
    
    def make_path(self):
        global total_caminho
        total_caminho += 1
        self.color = RED

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    #Adiciona os vizinhos adjacentes ao node que não são barreiras
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #Vizinho de cima
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #Vizinho de baixo
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): #Vizinho da direita
            self.neighbors.append(grid[self.row][self.col + 1])
            
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): #Vizinho da esquerda
            self.neighbors.append(grid[self.row][self.col - 1])

    #Compara os pontos
    def __lt__(self, other):
        return False

def writeToCsv(info):
    arquivo = 'report.csv'
    if not os.path.exists(arquivo):
        with open(arquivo, "+w") as f:
            writer = DictWriter(f, fieldnames = info.keys())
            writer.writeheader()

    with open(arquivo, "a+") as f:
        writer = DictWriter(f, fieldnames = info.keys())
        writer.writerow(info)


def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    #Caminho rápido
    #return abs(x1 - x2) + abs(y1 - y2)
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    D = max(dx, dy)
    #return D * math.sqrt(dx * dx + dy * dy)
    #return D * (dx * dx + dy * dy)
    return D * (dx + dy)
    #return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def reconstruct_path(came_from, current, draw, grid):
    aux = []
    while current in came_from:
        current = came_from[current]
        
        current.make_path()

        aux.append(current)
        if len(set(aux)) != len(aux):
            return
           
    draw()

def iddfs(draw, grid, start, end, maximum_depth: int=200):
    
    for depth in range(0, maximum_depth):
        for i in range(len(grid)):
            for j in range(len(grid)):
                grid[i][j].visited = False
    
        if _dfs(draw, start, end, depth):
            start.make_start()
            end.make_end()
            print(counter() - 1)
            write_information("iddfs", grid, counter() - 1)
            counter(True)
            return
    
        start.make_start()
        end.make_end()
        draw()
    print(counter() - 1)
    write_information("iddfs", grid, counter() - 1)
    counter(True)

def counter(reset=False, i=[0]):  
    if not reset:    
        i[0]+=1
        return i[0]
    else:
        i[0] = 0
        return i[0]

def _dfs(draw, src, end, depth: int):
    if src == end:
        return True 

    if depth <= 0:
        return False

    src.visited = True
    for edge in src.neighbors:
        edge.make_closed()
        if not edge.visited:
            counter() 
            if _dfs(draw, edge, end, depth - 1):
                return True

    return False

def dfs(draw, grid, start, end):
    stack = []
    stack.append(start)
    came_from = {}
    start.visited = True
    while len(stack):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN: #Cancela o a função durante a execução
                if event.key == pygame.K_ESCAPE:
                    return False

        node = stack.pop(-1)
        node.make_closed()
        for neighbor in node.neighbors:
            if node.color != BLACK and not neighbor.visited:
                stack.append(neighbor)
                neighbor.visited = True
                neighbor.make_open()
                came_from[neighbor] = node
                
        end.make_end()
        start.make_start()
        if node == end:
            reconstruct_path(came_from, end, draw, grid)
            end.make_end()
            start.make_start()
            write_information("dfs", grid, 0)
            break 
            
        draw()

def dfs_random(draw, grid, start, end):
    stack = []
    stack.append(start)
    came_from = {}
    start.visited = True
    while len(stack):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN: #Cancela o a função durante a execução
                if event.key == pygame.K_ESCAPE:
                    return False

        node = stack.pop(-1)
        node.make_closed()
        neighbors = list(node.neighbors)  # Convert neighbors to a list
        random.shuffle(neighbors)  # Shuffle the list of neighbors randomly
        for neighbor in neighbors:
            if node.color != BLACK and not neighbor.visited:
                stack.append(neighbor)
                neighbor.visited = True
                neighbor.make_open()
                came_from[neighbor] = node
                
        end.make_end()
        start.make_start()
        if node == end:
            reconstruct_path(came_from, end, draw, grid)
            end.make_end()
            start.make_start()
            write_information("dfs_random", grid, 0)
            break 
            
        draw()


def bcu(draw, grid, start, end):
    count = 0
    queue = PriorityQueue()
    #Adiciona o node inicial com o seu f_score inical que é igal a 0 e um count para diferir elementos com o mesmo f_score adjacentes na fila 
    queue.put((0, count, start))
    came_from = {}
    #Bruxaria
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    open_set_hash = {start}

    while not queue.empty():
        #interrompe o while caso vc queira
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN: #Cancela o a função durante a execução
                if event.key == pygame.K_ESCAPE:
                    return False

        current = queue.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw, grid)
            # print('asdsad', g_score[end])
            print(g_score[current]) 
            write_information("bcu", grid, g_score[current])
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1 + neighbor.weight

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                if neighbor not in open_set_hash:
                    count += 1
                    queue.put((g_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        #Animação da busca        
        draw()

        if current != start:
            current.make_closed()

    return False


def bidirectional(draw, grid, start, end):
    src_queue = []
    dest_queue = []
    src_queue.append(start)
    dest_queue.append(end)
    start.visited = True
    end.visited = True
    src_came_from = {}
    dest_came_from = {}
    found = False
    while len(src_queue) and len(dest_queue):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN: #Cancela o a função durante a execução
                if event.key == pygame.K_ESCAPE:
                    return False
        
        if found:
            reconstruct_path(src_came_from, check, draw, grid)
            reconstruct_path(dest_came_from, check, draw, grid)
            end.make_end()
            start.make_start()
            write_information("bi_d", grid, 0)
            return     

        src_node = src_queue.pop(0)
        src_node.make_closed()

        if src_node.dualVisited == [True, True]:
            check = src_node
            found = True

        for neighbor in src_node.neighbors:
            if not neighbor.dualVisited[0]:
                src_queue.append(neighbor)
                neighbor.dualVisited[0] = True
                neighbor.make_open()
                start.make_start()
                src_came_from[neighbor] = src_node

           
        dest_node = dest_queue.pop(0)
        dest_node.make_closed()

        if dest_node.dualVisited == [True, True]:
            check = dest_node
            found = True

        for neighbor in dest_node.neighbors:
            if not neighbor.dualVisited[1]:
                dest_queue.append(neighbor)
                neighbor.dualVisited[1] = True
                neighbor.make_open()
                end.make_end()
                dest_came_from[neighbor] = dest_node
                
        draw()


def bfs(draw, grid, start, end):
    queue = []
    queue.append(start)
    came_from = {}
    start.visited = True
    while len(queue):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN: #Cancela o a função durante a execução
                if event.key == pygame.K_ESCAPE:
                    return False

        node = queue.pop(0)
        node.make_closed()
        for neighbor in node.neighbors:
            if node.color != BLACK and not neighbor.visited:
                queue.append(neighbor)
                neighbor.visited = True
                neighbor.make_open()
                start.make_start()
                came_from[neighbor] = node
                
        if node == end:
            global total_caminho
            reconstruct_path(came_from, end, draw, grid)
            end.make_end()
            start.make_start()
            write_information("bfs", grid, 0)
            break 
            
        draw()


def write_information(algorithm, grid, weight):
    verde = 0
    verde_escuro = 0
    verde_claro = 0
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j].color == EMERALD:
                verde_escuro += 1
            if grid[i][j].color == GREEN:
                verde += 1
            if grid[i][j].color == RED:
                verde_claro += 1

    caminho = 0
    expandidos = 0
    if verde_claro > 0:
        caminho = verde_claro + 1
    else:
        caminho = verde
    
    if algorithm == "bi_d":
        caminho = caminho + 1

    expandidos = verde_claro+verde_escuro+verde
    global hash
    info = {
        "algoritmo": algorithm,
        "hash": hash,
        "expandidos": expandidos,
        "caminho": caminho,
        "visitados" : verde if verde > 0 else verde_claro,
        "peso": weight
    }

    if algorithm == "iddfs": 
        info["caminho"] = 0
        info["expandidos"] = 0
        info["visitados"] = weight
        info["peso"] = 0

    writeToCsv(info)

def bme(draw, grid, start, end):
    queue = []
    queue.append(start)
    start.visited = True
    current = start
    while(len(queue)):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN: #Cancela o a função durante a execução
                if event.key == pygame.K_ESCAPE:
                    return False

        if current == end:
            write_information("bme", grid, 0)
            break
        
        compare = []
        for neighbor in current.neighbors:
            compare.append( (neighbor, heuristic(neighbor.get_pos(), end.get_pos())) )
        current = compare[compare.index(min(compare, key=itemgetter(1)))][0]
        current.visited = True
        current.make_closed()

        queue.pop()

        for neighbor in current.neighbors:
            if not neighbor.visited:
                queue.append(neighbor)
                neighbor.visited = True
                neighbor.make_open()
        

        end.make_end()
        start.make_start()
            
        draw()

def bgme(draw, grid, start, end):
    current = start
    while(current is not end):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN: #Cancela o a função durante a execução
                if event.key == pygame.K_ESCAPE:
                    return False
        
        current.color = WHITE
        
        compare = []
        for neighbor in current.neighbors:
            compare.append( (neighbor, heuristic(neighbor.get_pos(), end.get_pos())) )
        current = compare[compare.index(min(compare, key=itemgetter(1)))][0]
        current.make_open()
        
        end.make_end()
        start.make_start()
            
        draw()
    write_information("bgme", grid, 0)


def a_star(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    #Adiciona o node inicial com o seu f_score inical que é igal a 0 e um count para diferir elementos com o mesmo f_score adjacentes na fila 
    open_set.put((0, count, start))
    came_from = {}
    #Bruxaria
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        #interrompe o while caso vc queira
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN: #Cancela o a função durante a execução
                if event.key == pygame.K_ESCAPE:
                    return False

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            global expandidos
            global total_caminho
            reconstruct_path(came_from, end, draw, grid)
            end.make_end()
            start.make_start()
            print(g_score[current]) 
            write_information("a_star", grid, g_score[current])
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1 + neighbor.weight

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())# + neighbor.weight
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        #Animação da busca        
        draw()

        if current != start:
            current.make_closed()

    return False


def make_grid(rows, width, clear):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            #Pré adiciona elementos
            if not clear:
                if random.randint(1, 100) > 65:
                    node.color = BLACK
            grid[i].append(node)
    
    return grid

def draw_grid(window, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, GREY,(0, i * gap),(width, i * gap))
        for j in range(rows):
            pygame.draw.line(window, GREY,(j * gap, 0),(j * gap, width))

def draw(window, grid, rows, width, index):
    window.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(window)

    draw_grid(window, rows, width)
    
    draw_UI(window, index, rows)

    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x, y = pos

    row = y // gap
    col = x // gap

    if col >= rows:
        col = rows-1
    if row >= rows:
        row = rows-1
        
    return row, col

def draw_UI(window, index, rows):
    mouse = pygame.mouse.get_pos()
    if 0 <= mouse[0] <= BTTN_W and WIDTH <= mouse[1] <= WIDTH+BTTN_H:
        pygame.draw.rect(window,DARK_GREY,[0,WIDTH,BTTN_W,BTTN_H])
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Tk().wm_withdraw() #to hide the main window
                    messagebox.showinfo('INFORMAÇÕES!'
                    ,'Use ESC (2x)para reiniciar o grid ou (1x) para cancelar uma operação em andamento.\n\n'+
                    'Use o botão esquerdo do mouse para adicionar elementos à grid.\n'+
                    '(O primeiro elemento adicionado será o ponto inicial e o segundo o ponto final)\n\n'+
                    'Use o botão direito do mouse para remover elementos da grid.\n\n'+
                    'Use o botão do meio do mouse para remover elementos da grid.\n\n'+
                    'Use C para limpar a grid após uma execução.\n\n'+
                    'Use ESPAÇO para iniciar a operação de busca!\n\n'+
                    'Use as sétas [ ← → ] para alternar entre os algorítmos de busca.\n\n'+
                    'Use R para limpar completamente a grid.\n\n'+
                    'Use P para abrir o libreoffice com os dados dos algoritmos.'
                    )
    else:
        pygame.draw.rect(window,GREY,[0,WIDTH,BTTN_W,BTTN_H])

    if 0 <= mouse[0] >= WIDTH-BTTN_W and WIDTH <= mouse[1] <= WIDTH+BTTN_H:
        pygame.draw.rect(window,DARK_GREY,[WIDTH-BTTN_W,WIDTH,BTTN_W,BTTN_H])
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Tk().wm_withdraw() 
                    USER_INP = simpledialog.askinteger(title="Tamanho", prompt="Digite um novo tamanho:", initialvalue=50, minvalue=10, maxvalue=200)
                    if isinstance(USER_INP, int):
                        main(WIN, WIDTH, USER_INP)
    else:
        pygame.draw.rect(window,GREY,[WIDTH-BTTN_W,WIDTH,BTTN_W,BTTN_H])

    text_font = pygame.font.SysFont('Arial',16)
    bttn1_text = text_font.render('AJUDA' , True , BLACK)
    bttn1_rect = bttn1_text.get_rect(center=(BTTN_W/2, WIDTH+BTTN_H/2))

    algInfo_text = text_font.render("Algorítmo: " + ALGORITHMS[index] , True , BLACK)
    algInfo_rect = algInfo_text.get_rect(midleft=(BTTN_W+10, WIDTH+BTTN_H/2))

    bttn2_text = text_font.render('TAMANHO' , True , BLACK)
    bttn2_rect = bttn2_text.get_rect(center=(WIDTH-BTTN_W/2, WIDTH+BTTN_H/2))

    window.blit(bttn1_text , bttn1_rect)
    window.blit(algInfo_text , algInfo_rect)
    window.blit(bttn2_text , bttn2_rect)

def change_hash():
    global hash
    hash = uuid4().hex
    print(hash)

def open_file():
    try:
        path = "C:\Program Files\LibreOffice\program\soffice"
        s.call([path, "--calc", "-o", "report.csv"])
    except:
        print("LibreOffice não encontrado!")
    
def main(window, width, grid_count):
    change_hash()
    ROWS = grid_count
    grid = make_grid(ROWS, width, False)
    alg_index = 0
    start = None
    end = None

    run = True
    started = False
    
    draw(window, grid, ROWS, width, alg_index)
    while run:
        #draw(window, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue
            
            if pygame.mouse.get_pressed()[0]: #Botão esquerdo do mouse
                pos = pygame.mouse.get_pos()
                if(pos[0] < WIDTH and pos[1] < WIDTH):
                    col, row = get_clicked_pos(pos, ROWS, width)
                    
                    node = grid[row][col]
                    change_hash()
                    if not start and node != end:
                        start = node
                        start.make_start()
                    
                    elif not end and node != start:
                        end = node
                        end.make_end()
                    
                    elif node != end and node != start:
                        node.make_barrier()

            elif pygame.mouse.get_pressed()[2]: #Botão direito do mouse
                pos = pygame.mouse.get_pos()
                if(pos[0] < WIDTH and pos[1] < WIDTH):
                    col, row = get_clicked_pos(pos, ROWS, width)
                    node = grid[row][col]
                    change_hash()
                    node.weight = 0
                    node.reset()
                    if node == start:
                        start = None
                    elif node == end:
                        end = None
            
            elif pygame.mouse.get_pressed()[1]: #Botão do meio do mouse
                pos = pygame.mouse.get_pos()
                if(pos[0] < WIDTH and pos[1] < WIDTH):
                    col, row = get_clicked_pos(pos, ROWS, width)
                    node = grid[row][col]
                    change_hash()
                    if node != start and node != end and node.color != BLACK:
                        node.make_weight()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    for i in range(ROWS):
                        for j in range(ROWS):
                            current = grid[i][j].color
                            grid[i][j].visited = False
                            grid[i][j].dualVisited = [False, False]
                            if current == GREEN or current == EMERALD or current == RED:
                                grid[i][j].reset()
                            if grid[i][j].weight > 0:
                                grid[i][j].make_weight()

                    #Lambda é uma variável que chama uma função
                    if start != None and end != None:
                        if alg_index == 0:
                            a_star(lambda: draw(window, grid, ROWS, width, alg_index), grid, start, end)
                        if alg_index == 1:
                            bfs(lambda: draw(window, grid, ROWS, width, alg_index), grid, start, end)
                        if alg_index == 2:
                            dfs(lambda: draw(window, grid, ROWS, width, alg_index), grid, start, end)
                        if alg_index == 3:
                            dfs_random(lambda: draw(window, grid, ROWS, width, alg_index), grid, start, end)
                        if alg_index == 4:
                            bgme(lambda: draw(window, grid, ROWS, width, alg_index), grid, start, end)
                        if alg_index == 5:
                            bme(lambda: draw(window, grid, ROWS, width, alg_index), grid, start, end)
                        if alg_index == 6:
                            bcu(lambda: draw(window, grid, ROWS, width, alg_index), grid, start, end)
                        if alg_index == 7:
                            iddfs(lambda: draw(window, grid, ROWS, width, alg_index), grid, start, end)
                        if alg_index == 8:
                            bidirectional(lambda: draw(window, grid, ROWS, width, alg_index), grid, start, end)
                if event.key == pygame.K_ESCAPE:
                    change_hash()
                    global expandidos 
                    global total_caminho
                    total_caminho = 0
                    expandidos = 0
                    start = None
                    end = None
                    grid = make_grid(ROWS, width, False)

                if event.key == pygame.K_r:
                    change_hash()
                    start = None
                    end = None
                    grid = make_grid(ROWS, width, True)

                if event.key == pygame.K_c:
                    for i in range(ROWS):
                        for j in range(ROWS):
                            current = grid[i][j].color
                            grid[i][j].visited = False
                            grid[i][j].dualVisited = [False, False]
                            if current == GREEN or current == EMERALD or current == RED:
                                grid[i][j].reset()
                            if grid[i][j].weight > 0:
                                grid[i][j].make_weight()

                if event.key == pygame.K_LEFT:
                    alg_index = (alg_index - 1) % len(ALGORITHMS)
                
                if event.key == pygame.K_RIGHT:
                    alg_index = (alg_index + 1) % len(ALGORITHMS)

                if event.key == pygame.K_p:
                    open_file()

        draw(window, grid, ROWS, width, alg_index)
    pygame.quit()


main(WIN, WIDTH, GRID_COUNT)