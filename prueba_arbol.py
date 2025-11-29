#Referencia visual :  https://www.youtube.com/watch?v=W_qQTKupZpY
#Referencia de codigo : https://github.com/lfmarin/IntroIA/blob/main/RobotTree_ML.ipynb
#Daniel Dominguez Azamar -  Introduccion a la Inteligencia Artificial

import plotly.graph_objects as go
from collections import deque, defaultdict
import numpy as np

# 1 2 3
# 4 5 6
# 7 8 0
#Asi lo imagine, (espero asi sea)

ESTADO_META = (1, 2, 3, 4, 5, 6, 7, 8, 0)
TAMANO_LADO = 3
TAMANO_TABLERO = 9

#Este ejercicio me recordo al de los lugares por visitar de la heuristica y demas que se vieron en diapositivas (por eso agarre codigo de ahi xd)
class Nodo:
    def __init__(self, tablero, padre=None, operacion=None, profundidad=0):
        self.tablero = tablero 
        self.padre = padre
        self.operacion = operacion
        self.profundidad = profundidad

    def __eq__(self, otro):
        return self.tablero == otro.tablero

    def __hash__(self):
        return hash(self.tablero)

    def _get_blank_index(self):
        return self.tablero.index(0)

    def _swap(self, i, j):
        tablero_list = list(self.tablero)
        tablero_list[i], tablero_list[j] = tablero_list[j], tablero_list[i]
        return tuple(tablero_list)

#Esto es para lo visual con el plotly
    def generar_hijos(self):
        hijos = []
        i = self._get_blank_index()
        if i >= TAMANO_LADO:
            nuevo_tablero = self._swap(i, i - TAMANO_LADO)
            hijos.append(Nodo(nuevo_tablero, self, 'Arriba', self.profundidad + 1))
        
        if i < TAMANO_TABLERO - TAMANO_LADO:
            nuevo_tablero = self._swap(i, i + TAMANO_LADO)
            hijos.append(Nodo(nuevo_tablero, self, 'Abajo', self.profundidad + 1))

        if i % TAMANO_LADO != 0:
            nuevo_tablero = self._swap(i, i - 1)
            hijos.append(Nodo(nuevo_tablero, self, 'Izquierda', self.profundidad + 1))
            
        if (i + 1) % TAMANO_LADO != 0: 
            nuevo_tablero = self._swap(i, i + 1)
            hijos.append(Nodo(nuevo_tablero, self, 'Derecha', self.profundidad + 1))

        return hijos


def generar_arbol(estado_inicial, max_profundidad=3):
    root_node = Nodo(estado_inicial)
    cola = deque([root_node])
    visitados = {estado_inicial}
    
    nodos_por_profundidad = defaultdict(list)
    nodos_por_profundidad[0].append(root_node)
    
    aristas = [] 
    
    while cola:
        nodo_actual = cola.popleft()
        
        if nodo_actual.profundidad >= max_profundidad:
            continue

        for sucesor in nodo_actual.generar_hijos():
            if sucesor.tablero not in visitados:
                visitados.add(sucesor.tablero)
                cola.append(sucesor)
                
                aristas.append({
                    'parent': nodo_actual.tablero,
                    'child': sucesor.tablero,
                    'operacion': sucesor.operacion
                })
                
                nodos_por_profundidad[sucesor.profundidad].append(sucesor)

    posiciones = {}
    
    Y_MAX = max_profundidad 
    
    for profundidad, lista_nodos in nodos_por_profundidad.items():
        num_nodos = len(lista_nodos)
        ancho_total = 2 * num_nodos 
        
        for idx, nodo in enumerate(lista_nodos):
            x_pos = (idx - (num_nodos - 1) / 2) * 2.0
            y_pos = Y_MAX - profundidad
            
            posiciones[nodo.tablero] = {'x': x_pos, 'y': y_pos, 'profundidad': profundidad, 'operacion': nodo.operacion if nodo.padre else "INICIO"}

    return aristas, posiciones


def visualizar_arbol(aristas, posiciones):

    edge_x = []
    edge_y = []
    edge_text = []

    for arista in aristas:
        parent_pos = posiciones[arista['parent']]
        child_pos = posiciones[arista['child']]

        edge_x.extend([parent_pos['x'], child_pos['x'], None])
        edge_y.extend([parent_pos['y'], child_pos['y'], None])
        
        mid_x = (parent_pos['x'] + child_pos['x']) / 2
        mid_y = (parent_pos['y'] + child_pos['y']) / 2
        
        edge_text.append({
            'x': mid_x, 
            'y': mid_y, 
            'text': arista['operacion']
        })

    trace_edge = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines',
        name='Movimiento'
    )

    node_x = [pos['x'] for pos in posiciones.values()]
    node_y = [pos['y'] for pos in posiciones.values()]
    
    node_hover_text = []
    node_colors = []
    for tablero, pos in posiciones.items():
        board_str = "\n".join([
            f"{tablero[i]} {tablero[i+1]} {tablero[i+2]}"
            for i in range(0, TAMANO_TABLERO, TAMANO_LADO)
        ])
        
        hover_info = f"<b>Profundidad:</b> {pos['profundidad']}<br>" \
                     f"<b>Tablero:</b><pre>{board_str}</pre><br>" \
                     f"<b>Movimiento:</b> {pos['operacion']}"
                     
        node_hover_text.append(hover_info)
        node_colors.append(pos['profundidad'])
        
    trace_node = go.Scatter(
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=15,
            color=node_colors,
            colorbar=dict(
                thickness=15,
                title='Profundidad',
                xanchor='left',
            ),
            line_width=2
        ),
        name='Estado'
    )
    

    trace_labels = go.Scatter(
        x=[t['x'] for t in edge_text], 
        y=[t['y'] for t in edge_text],
        mode='text',
        text=[t['text'] for t in edge_text],
        textfont=dict(size=10, color='blue'),
        hoverinfo='none'
    )
    
    fig = go.Figure(data=[trace_edge, trace_node, trace_labels],
                    layout=go.Layout(
                        title=dict(
                            text='8 Puzzle representado con un arbol',
                            font=dict(size=16)
                        ),
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                    )
                   )
    fig.show()



if __name__ == "__main__":
    estado_inicial_solvable = (1, 2, 3, 0, 4, 6, 7, 5, 8) 
    MAX_DEPTH = 3 
    
    aristas_list, posiciones_dict = generar_arbol(estado_inicial_solvable, MAX_DEPTH)
    
    print(f"Generación de Árbol de Búsqueda del 8-Puzzle:")
    print(f"Estado Inicial: {estado_inicial_solvable}")
    print(f"Nodos generados hasta el nivel {MAX_DEPTH}: {len(posiciones_dict)}")
    print(f"Movimientos hechos: {len(aristas_list)}")
    
    visualizar_arbol(aristas_list, posiciones_dict)