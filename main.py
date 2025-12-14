import pygame
import sys
import heapq
import random
import math
import json
import os

# --- 1. CONFIGURACIÓN GLOBAL ---
ANCHO_VENTANA = 900
ALTO_VENTANA = 700
CELDA = 30

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
PISO_CAFE = (100, 70, 0)
PISO_GRIS = (50, 50, 50)
VERDE = (0, 255, 0)       # Jugador Visible
VERDE_OSCURO = (0, 100, 0)# Jugador Escondido
ROJO = (255, 0, 0)        # V1: A*
NARANJA = (255, 140, 0)   # V2: Wavefront
AMARILLO = (255, 255, 0)  # V3: Greedy
MORADO = (128, 0, 128)    # V4: PRM
AZUL = (0, 0, 255)        # Escondites
CIAN = (0, 255, 255)      # ITEMS
ORO = (255, 215, 0)       # UI Tiempo
#LINEA_PRM = (60, 0, 60)   # Grafo PRM

ARCHIVO_SAVE = "savegame.json"

# --- 2. CONFIGURACIÓN DE NIVELES ---
NIVELES = {
    1: {"duracion": 180, "v_activos": [0, 1],       "factor_velocidad": 1.2, "items": 1},
    2: {"duracion": 180, "v_activos": [0, 1, 2],    "factor_velocidad": 1.0, "items": 1},
    3: {"duracion": 240, "v_activos": [0, 1, 2, 3], "factor_velocidad": 0.9, "items": 2},
    4: {"duracion": 240, "v_activos": [0, 1, 2, 3], "factor_velocidad": 0.7, "items": 2},
    5: {"duracion": 300, "v_activos": [0, 1, 2, 3], "factor_velocidad": 0.5, "items": 2}
}

# --- 3. MAPA ---
MAPA = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 3, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 3, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 0, 3, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 3, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 3, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# --- 4. PERSISTENCIA ---
def guardar_juego(nivel):
    try:
        with open(ARCHIVO_SAVE, 'w') as f:
            json.dump({"nivel": nivel}, f)
    except: pass

def cargar_juego():
    if not os.path.exists(ARCHIVO_SAVE): return 1
    try:
        with open(ARCHIVO_SAVE, 'r') as f:
            return min(5, json.load(f).get("nivel", 1))
    except: return 1

# --- 5. ALGORITMOS IA ---
def heuristica(a, b): return abs(b[0] - a[0]) + abs(b[1] - a[1])

def a_star(inicio, meta, grid):
    filas, cols = len(grid), len(grid[0])
    frontera = [(0, inicio)]; came_from = {inicio: None}; cost_so_far = {inicio: 0}
    while frontera:
        current = heapq.heappop(frontera)[1]
        if current == meta: break
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_node = (current[0] + dx, current[1] + dy)
            if 0 <= next_node[1] < filas and 0 <= next_node[0] < cols:
                if grid[next_node[1]][next_node[0]] != 1:
                    new_cost = cost_so_far[current] + 1
                    if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                        cost_so_far[next_node] = new_cost
                        priority = new_cost + heuristica(meta, next_node)
                        heapq.heappush(frontera, (priority, next_node))
                        came_from[next_node] = current
    path = []
    curr = meta
    if meta not in came_from: return []
    while curr != inicio: path.append(curr); curr = came_from[curr]
    path.reverse()
    return path

def wavefront(meta, grid):
    filas, cols = len(grid), len(grid[0])
    valor_mapa = [[-1 for _ in range(cols)] for _ in range(filas)]
    cola = [meta]; valor_mapa[meta[1]][meta[0]] = 0
    while cola:
        curr = cola.pop(0)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = curr[0] + dx, curr[1] + dy
            if 0 <= ny < filas and 0 <= nx < cols:
                if grid[ny][nx] != 1 and valor_mapa[ny][nx] == -1:
                    valor_mapa[ny][nx] = valor_mapa[curr[1]][curr[0]] + 1
                    cola.append((nx, ny))
    return valor_mapa

def greedy_bfs(inicio, meta, grid):
    filas, cols = len(grid), len(grid[0])
    frontera = [(0, inicio)]; came_from = {inicio: None}
    while frontera:
        current = heapq.heappop(frontera)[1]
        if current == meta: break
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_node = (current[0] + dx, current[1] + dy)
            if 0 <= next_node[1] < filas and 0 <= next_node[0] < cols:
                if grid[next_node[1]][next_node[0]] != 1:
                    if next_node not in came_from:
                        priority = heuristica(meta, next_node)
                        heapq.heappush(frontera, (priority, next_node))
                        came_from[next_node] = current
    path = []
    curr = meta
    if meta not in came_from: return []
    while curr != inicio: path.append(curr); curr = came_from[curr]
    path.reverse()
    return path

class PRM_Graph:
    def __init__(self, grid, num_nodos=60):
        self.grid = grid
        self.nodos = []; self.aristas = {}
        self.generar_nodos(num_nodos)
        self.conectar_nodos()

    def es_libre(self, x, y):
        if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0]): return self.grid[int(y)][int(x)] != 1
        return False

    def linea_libre(self, p1, p2):
        x1, y1 = p1; x2, y2 = p2
        issteep = abs(y2-y1) > abs(x2-x1)
        if issteep: x1, y1 = y1, x1; x2, y2 = y2, x2
        if x1 > x2: x1, x2 = x2, x1; y1, y2 = y2, y1
        deltax = x2 - x1; deltay = abs(y2 - y1); error = int(deltax / 2); y = y1
        ystep = 1 if y1 < y2 else -1
        for x in range(int(x1), int(x2) + 1):
            coord = (y, x) if issteep else (x, y)
            if not self.es_libre(coord[0], coord[1]): return False
            error -= deltay
            if error < 0: y += ystep; error += deltax
        return True

    def generar_nodos(self, num):
        intentos = 0
        while len(self.nodos) < num and intentos < 1000:
            rx = random.randint(0, len(self.grid[0])-1); ry = random.randint(0, len(self.grid)-1)
            if self.es_libre(rx, ry): self.nodos.append((rx, ry))
            intentos += 1
        self.nodos.extend([(14,17), (14,2), (1,1), (2,11), (3,11), (9,11), (19,11), (26,2)])

    def conectar_nodos(self):
        for nodo in self.nodos: self.aristas[nodo] = []
        for n1 in self.nodos:
            distancias = []
            for n2 in self.nodos:
                if n1 != n2:
                    d = math.sqrt((n1[0]-n2[0])**2 + (n1[1]-n2[1])**2)
                    distancias.append((d, n2))
            distancias.sort()
            conectados = 0
            for d, n2 in distancias:
                if conectados >= 3: break
                if self.linea_libre(n1, n2):
                    self.aristas[n1].append(n2); self.aristas[n2].append(n1); conectados += 1

    def encontrar_camino_grafo(self, inicio_aprox, meta_aprox):
        nodo_inicio = min(self.nodos, key=lambda n: math.sqrt((n[0]-inicio_aprox[0])**2 + (n[1]-inicio_aprox[1])**2))
        nodo_meta = min(self.nodos, key=lambda n: math.sqrt((n[0]-meta_aprox[0])**2 + (n[1]-meta_aprox[1])**2))
        frontera = [(0, nodo_inicio)]; came_from = {nodo_inicio: None}; cost_so_far = {nodo_inicio: 0}
        while frontera:
            current = heapq.heappop(frontera)[1]
            if current == nodo_meta: break
            for next_node in self.aristas.get(current, []):
                new_cost = cost_so_far[current] + math.sqrt((current[0]-next_node[0])**2 + (current[1]-next_node[1])**2)
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + heuristica(nodo_meta, next_node)
                    heapq.heappush(frontera, (priority, next_node))
                    came_from[next_node] = current
        path = []
        curr = nodo_meta
        if nodo_meta not in came_from: return []
        while curr != nodo_inicio: path.append(curr); curr = came_from[curr]
        path.reverse()
        return path

# --- 6. MOTOR DEL JUEGO ---
class Game:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("FNAF Informatics: Escape IA")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.SysFont("Arial", 24)
        self.fuente_grande = pygame.font.SysFont("Arial", 48)
        
        self.estado = "MENU"
        self.nivel_actual = cargar_juego()
        self.prm = PRM_Graph(MAPA)
        self.resetear_nivel()

    def resetear_nivel(self):
        if self.nivel_actual > 5: self.nivel_actual = 1
        
        config = NIVELES.get(self.nivel_actual, NIVELES[5])
        self.duracion_total = config["duracion"] * 1000 
        self.tiempo_restante = self.duracion_total # NUEVO: Usamos contador regresivo
        
        self.villanos_activos = config["v_activos"] 
        self.factor_vel = config["factor_velocidad"]
        
        self.jx, self.jy = 14, 17
        self.escondido = False
        self.timer_escondido_actual = 0 # Cronometro para el oxigeno
        self.MAX_TIEMPO_ESCONDIDO = 5000 # 5 segundos
        
        self.mensaje_game_over = ""

        # Items
        self.items = []
        num_items = config["items"]
        intentos = 0
        while len(self.items) < num_items and intentos < 100:
            rx = random.randint(0, len(MAPA[0])-1)
            ry = random.randint(0, len(MAPA)-1)
            if MAPA[ry][rx] in [0, 2] and (rx, ry) != (self.jx, self.jy):
                if (rx, ry) not in self.items:
                    self.items.append((rx, ry))
            intentos += 1

        base_cd = [300, 400, 250, 400]
        # Inicializamos villanos con un "patrol_target" para cuando te escondes
        self.villanos = [
            {'pos': [12, 2], 'timer': 0, 'cd': base_cd[0] * self.factor_vel, 'tipo': 'A*', 'color': ROJO, 'patrol_target': None},
            {'pos': [1, 1],  'timer': 0, 'cd': base_cd[1] * self.factor_vel, 'tipo': 'WAVE', 'color': NARANJA, 'patrol_target': None},
            {'pos': [26, 1], 'timer': 0, 'cd': base_cd[2] * self.factor_vel, 'tipo': 'GREEDY', 'color': AMARILLO, 'patrol_target': None},
            {'pos': [2, 11], 'timer': 0, 'cd': base_cd[3] * self.factor_vel, 'tipo': 'PRM', 'color': MORADO, 'patrol_target': None}
        ]

    def input_jugador(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]: dx = -1
        elif keys[pygame.K_RIGHT]: dx = 1
        elif keys[pygame.K_UP]: dy = -1
        elif keys[pygame.K_DOWN]: dy = 1
        
        if dx != 0 or dy != 0:
            pygame.time.delay(80)
            nx, ny = self.jx + dx, self.jy + dy
            if 0 <= ny < len(MAPA) and 0 <= nx < len(MAPA[0]):
                if MAPA[ny][nx] != 1:
                    self.jx, self.jy = nx, ny
                    self.escondido = False 
                    self.timer_escondido_actual = 0 # Reset oxigeno al moverse
                    
                    if (self.jx, self.jy) in self.items:
                        self.items.remove((self.jx, self.jy))

    def mecanica_escondite(self, dt):
        keys = pygame.key.get_pressed()
        # Entrar al escondite
        if MAPA[self.jy][self.jx] == 3 and keys[pygame.K_e] and not self.escondido:
            self.escondido = True
            self.timer_escondido_actual = self.MAX_TIEMPO_ESCONDIDO
        
        # Lógica mientras está escondido (CONTADOR)
        if self.escondido:
            self.timer_escondido_actual -= dt
            if self.timer_escondido_actual <= 0:
                self.escondido = False # Te sacan a patadas
                self.timer_escondido_actual = 0

    def obtener_punto_random(self):
        # Busca un punto válido en el mapa para patrullar
        for _ in range(10):
            rx = random.randint(0, len(MAPA[0])-1)
            ry = random.randint(0, len(MAPA)-1)
            if MAPA[ry][rx] != 1: return (rx, ry)
        return (14, 17) # Default oficina

    def actualizar_villanos(self, dt):
        # Actualizamos timers de villanos con dt
        for i in self.villanos_activos:
            if i >= len(self.villanos): continue
            v = self.villanos[i]
            v['timer'] += dt # Sumar delta time

            if v['timer'] > v['cd']:
                v['timer'] = 0 # Reset cooldown
                
                # DEFINIR OBJETIVO (Jugador o Patrulla)
                objetivo = (self.jx, self.jy)
                
                if self.escondido:
                    # Si el jugador está escondido, usar punto de patrulla
                    if v['patrol_target'] is None or tuple(v['pos']) == v['patrol_target']:
                        v['patrol_target'] = self.obtener_punto_random()
                    objetivo = v['patrol_target']
                else:
                    # Si el jugador es visible, resetear patrulla y perseguir
                    v['patrol_target'] = None
                
                # MOVER SEGÚN ALGORITMO
                inicio = tuple(v['pos'])
                nuevo_pos = None

                if v['tipo'] == 'A*':
                    camino = a_star(inicio, objetivo, MAPA)
                    if camino: nuevo_pos = camino[0]
                elif v['tipo'] == 'WAVE':
                    hm = wavefront(objetivo, MAPA)
                    mejor = inicio; menor = float('inf')
                    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nx, ny = inicio[0] + dx, inicio[1] + dy
                        if 0 <= ny < len(MAPA) and 0 <= nx < len(MAPA[0]):
                            val = hm[ny][nx]
                            if val != -1 and val < menor:
                                menor = val; mejor = (nx, ny)
                    nuevo_pos = mejor
                elif v['tipo'] == 'GREEDY':
                    camino = greedy_bfs(inicio, objetivo, MAPA)
                    if camino: nuevo_pos = camino[0]
                elif v['tipo'] == 'PRM':
                    ruta = self.prm.encontrar_camino_grafo(inicio, objetivo)
                    if ruta:
                        pasos = a_star(inicio, ruta[0], MAPA)
                        if pasos: nuevo_pos = pasos[0]

                if nuevo_pos: v['pos'] = list(nuevo_pos)
                
                # COLISIÓN (Solo mata si NO estás escondido)
                if tuple(v['pos']) == (self.jx, self.jy) and not self.escondido:
                    self.mensaje_game_over = "¡TE ATRAPARON!"
                    self.estado = "GAME_OVER"

    def dibujar(self):
        self.pantalla.fill(NEGRO)
        
        if self.estado == "MENU":
            txt = self.fuente_grande.render(f"FNAF IA - NOCHE {self.nivel_actual}", True, BLANCO)
            txt2 = self.fuente.render("ENTER: Iniciar | L: Cargar Partida", True, BLANCO)
            self.pantalla.blit(txt, (ANCHO_VENTANA//2 - txt.get_width()//2, 200))
            self.pantalla.blit(txt2, (ANCHO_VENTANA//2 - txt2.get_width()//2, 300))
        
        elif self.estado == "WIN_GAME":
            txt = self.fuente_grande.render("¡JUEGO COMPLETADO!", True, ORO)
            txt2 = self.fuente.render("Sobreviviste las 5 Noches", True, BLANCO)
            txt3 = self.fuente.render("Presiona ENTER para volver al Menú", True, BLANCO)
            self.pantalla.blit(txt, (ANCHO_VENTANA//2 - txt.get_width()//2, 200))
            self.pantalla.blit(txt2, (ANCHO_VENTANA//2 - txt2.get_width()//2, 300))
            self.pantalla.blit(txt3, (ANCHO_VENTANA//2 - txt3.get_width()//2, 400))

        elif self.estado == "JUGANDO" or self.estado == "PAUSA":
            # Mapa
            for r in range(len(MAPA)):
                for c in range(len(MAPA[0])):
                    x, y = c*CELDA, r*CELDA
                    if MAPA[r][c] == 0: pygame.draw.rect(self.pantalla, PISO_CAFE, (x,y,CELDA,CELDA))
                    elif MAPA[r][c] == 2: pygame.draw.rect(self.pantalla, PISO_GRIS, (x,y,CELDA,CELDA))
                    elif MAPA[r][c] == 3: pygame.draw.rect(self.pantalla, AZUL, (x,y,CELDA,CELDA))
            
            # ITEMS
            for item in self.items:
                pygame.draw.rect(self.pantalla, CIAN, (item[0]*CELDA+8, item[1]*CELDA+8, CELDA-16, CELDA-16))

            # Villanos (PRM Lines)
            if 3 in self.villanos_activos:
                for nodo, vecinos in self.prm.aristas.items():
                    for v in vecinos:
                        s = (nodo[0]*CELDA+CELDA//2, nodo[1]*CELDA+CELDA//2)
                        e = (v[0]*CELDA+CELDA//2, v[1]*CELDA+CELDA//2)
                        #pygame.draw.line(self.pantalla, LINEA_PRM, s, e, 1)

            # Jugador
            color_j = VERDE_OSCURO if self.escondido else VERDE
            pygame.draw.rect(self.pantalla, color_j, (self.jx*CELDA+5, self.jy*CELDA+5, CELDA-10, CELDA-10))
            
            # Villanos
            for i in self.villanos_activos:
                if i < len(self.villanos):
                    v = self.villanos[i]
                    pygame.draw.rect(self.pantalla, v['color'], (v['pos'][0]*CELDA+5, v['pos'][1]*CELDA+5, CELDA-10, CELDA-10))

            # UI TIEMPO (Calculado con tiempo restante directo)
            progreso = 1 - (self.tiempo_restante / self.duracion_total)
            total_minutos_juego = int(progreso * 6 * 60)
            hora = 12 + (total_minutos_juego // 60)
            if hora > 12: hora -= 12
            minutos = total_minutos_juego % 60
            
            txt_time = self.fuente.render(f"{hora}:{minutos:02d} AM", True, ORO)
            txt_items = self.fuente.render(f"Items: {len(self.items)}", True, CIAN)
            txt_night = self.fuente.render(f"Noche {self.nivel_actual}", True, BLANCO)
            
            self.pantalla.blit(txt_time, (ANCHO_VENTANA - 130, 10))
            self.pantalla.blit(txt_night, (ANCHO_VENTANA - 130, 40))
            self.pantalla.blit(txt_items, (10, 10))

            # UI AGUANTE ESCONDITE
            if self.escondido:
                ancho_barra = 200
                porcentaje = self.timer_escondido_actual / self.MAX_TIEMPO_ESCONDIDO
                pygame.draw.rect(self.pantalla, ROJO, (10, 50, ancho_barra, 20))
                pygame.draw.rect(self.pantalla, VERDE, (10, 50, ancho_barra * porcentaje, 20))
                txt_hide = self.fuente.render("!SAL ALGO TE VA A SACAR!", True, BLANCO)
                self.pantalla.blit(txt_hide, (10, 20))
            else:
                txt_hide = self.fuente.render("Presiona 'E' en Azul", True, BLANCO)
                self.pantalla.blit(txt_hide, (10, 20))

            if self.estado == "PAUSA":
                overlay = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
                overlay.set_alpha(150)
                overlay.fill(NEGRO)
                self.pantalla.blit(overlay, (0,0))
                txt_p = self.fuente_grande.render("PAUSA", True, BLANCO)
                txt_q = self.fuente.render("Q: Salir al Menú", True, BLANCO)
                txt_r = self.fuente.render("P: Reanudar", True, BLANCO)
                self.pantalla.blit(txt_p, (ANCHO_VENTANA//2 - txt_p.get_width()//2, 250))
                self.pantalla.blit(txt_r, (ANCHO_VENTANA//2 - txt_r.get_width()//2, 350))
                self.pantalla.blit(txt_q, (ANCHO_VENTANA//2 - txt_q.get_width()//2, 400))

        elif self.estado == "GAME_OVER":
            txt = self.fuente_grande.render("GAME OVER", True, ROJO)
            txt_m = self.fuente.render(self.mensaje_game_over, True, BLANCO)
            txt2 = self.fuente.render("R: Reiniciar Noche", True, BLANCO)
            self.pantalla.blit(txt, (ANCHO_VENTANA//2 - txt.get_width()//2, 250))
            self.pantalla.blit(txt_m, (ANCHO_VENTANA//2 - txt_m.get_width()//2, 320))
            self.pantalla.blit(txt2, (ANCHO_VENTANA//2 - txt2.get_width()//2, 400))
        
        elif self.estado == "VICTORIA_NOCHE":
            txt = self.fuente_grande.render("6:00 AM - ¡SOBREVIVISTE!", True, VERDE)
            txt2 = self.fuente.render("ENTER: Siguiente Noche", True, BLANCO)
            self.pantalla.blit(txt, (ANCHO_VENTANA//2 - txt.get_width()//2, 300))
            self.pantalla.blit(txt2, (ANCHO_VENTANA//2 - txt2.get_width()//2, 400))

        pygame.display.flip()

    def loop_principal(self):
        while True:
            # DELTA TIME (Milisegundos entre frames)
            dt = self.reloj.tick(30) 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if self.estado == "MENU":
                        if event.key == pygame.K_RETURN:
                            self.estado = "JUGANDO"
                        elif event.key == pygame.K_l:
                            self.nivel_actual = cargar_juego()
                            self.resetear_nivel()
                            self.estado = "JUGANDO"

                    elif self.estado == "JUGANDO":
                        if event.key == pygame.K_p:
                            self.estado = "PAUSA"
                        # mecanica_escondite ya no va aquí, se revisa cada frame

                    elif self.estado == "PAUSA":
                        if event.key == pygame.K_p:
                            self.estado = "JUGANDO"
                        elif event.key == pygame.K_q:
                            self.estado = "MENU"
                    
                    elif self.estado == "GAME_OVER":
                        if event.key == pygame.K_r:
                            self.resetear_nivel()
                            self.estado = "JUGANDO"

                    elif self.estado == "VICTORIA_NOCHE":
                        if event.key == pygame.K_RETURN:
                            self.nivel_actual += 1
                            guardar_juego(self.nivel_actual)
                            self.resetear_nivel()
                            self.estado = "JUGANDO"
                        else:
                                self.estado = "WIN_GAME"
                                self.nivel_actual = 1
                                guardar_juego(1)
                    
                    elif self.estado == "WIN_GAME":
                        if event.key == pygame.K_RETURN:
                            self.estado = "MENU"

            # LÓGICA CONTINUA
            if self.estado == "JUGANDO":
                self.input_jugador()
                self.mecanica_escondite(dt) # Ahora pasamos dt para la cuenta regresiva
                self.actualizar_villanos(dt) # Ahora pasamos dt para moverlos
                
                # Restar tiempo solo si jugamos
                self.tiempo_restante -= dt
                
                if self.tiempo_restante <= 0:
                    if len(self.items) == 0:
                        self.estado = "VICTORIA_NOCHE"
                    else:
                        self.mensaje_game_over = "¡SE ACABÓ EL TIEMPO! (Faltaron Items)"
                        self.estado = "GAME_OVER"

            self.dibujar()

if __name__ == "__main__":
    juego = Game()
    juego.loop_principal()