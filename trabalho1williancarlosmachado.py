# -*- coding: utf-8 -*-
"""Trabalho1WillianCarlosMachado.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aTXoK7SwKssTVB_-mmgJbASdo9ZohRLT
"""

import heapq
import numpy as np

# Define o estado objetivo
estado_objetivo = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

# Função para calcular a heurística de Manhattan
def heuristica_manhattan(estado):
    distancia = 0
    for i in range(3):
        for j in range(3):
            if estado[i, j] != 0 and estado[i, j] != estado_objetivo[i, j]:
                posicao_correta = ((estado[i, j] - 1) // 3, (estado[i, j] - 1) % 3)
                distancia += abs(i - posicao_correta[0]) + abs(j - posicao_correta[1])
    return distancia

# Função para gerar os estados sucessores
def gerar_sucessores(estado):
    sucessores = []
    posicao_vazia = np.where(estado == 0)
    i, j = posicao_vazia[0][0], posicao_vazia[1][0]
    movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for movimento in movimentos:
        novo_i, novo_j = i + movimento[0], j + movimento[1]
        if 0 <= novo_i < 3 and 0 <= novo_j < 3:
            sucessor = np.copy(estado)
            sucessor[i, j], sucessor[novo_i, novo_j] = sucessor[novo_i, novo_j], sucessor[i, j]
            sucessores.append(sucessor)
    return sucessores

# Algoritmo de busca A*
def busca_a_estrela(estado_inicial):
    fila = []
    # Convert the initial state to a tuple for hashing in the visited set
    estado_inicial_tuple = tuple(map(tuple, estado_inicial))
    heapq.heappush(fila, (heuristica_manhattan(estado_inicial), estado_inicial_tuple, []))
    visitados = set()
    while fila:
        _, estado_atual_tuple, caminho = heapq.heappop(fila)
        # Convert the state back to a NumPy array for calculations
        estado_atual = np.array(estado_atual_tuple)
        if np.array_equal(estado_atual, estado_objetivo):
            return caminho + [estado_atual]
        visitados.add(estado_atual_tuple)
        for sucessor in gerar_sucessores(estado_atual):
            # Convert the successor to a tuple for hashing
            sucessor_tuple = tuple(map(tuple, sucessor))
            if sucessor_tuple not in visitados:
                heapq.heappush(fila, (len(caminho) + 1 + heuristica_manhattan(sucessor), sucessor_tuple, caminho + [estado_atual]))
    return None

# Exemplo de uso
estado_inicial = np.array([[4, 1, 3], [7, 2, 5], [8, 0, 6]])
solucao = busca_a_estrela(estado_inicial)
if solucao:
    for i, estado in enumerate(solucao):
        print(f"Passo {i}:")
        print(estado)
        print()
else:
    print("Não foi possível encontrar uma solução.")