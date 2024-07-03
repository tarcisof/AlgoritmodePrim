import heapq
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def ler_matrizes_de_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        matrizes = []
        matriz_atual = []
        for linha in arquivo:
            linha = linha.strip()
            if linha == "":
                if matriz_atual:
                    matrizes.append(np.array(matriz_atual, dtype=int))
                    matriz_atual = []
            else:
                matriz_atual.append(list(map(int, linha.split())))
        if matriz_atual:
            matrizes.append(np.array(matriz_atual, dtype=int))
    return matrizes


class Grafo:
    def __init__(self, matriz):
        self.matriz = matriz
        self.lista_adjacencia = self.obter_lista_adjacencia()

    def obter_lista_adjacencia(self):
        lista_adjacencia = []
        for indice_vertice, linha in enumerate(self.matriz):
            adjacentes = []
            for indice, valor in enumerate(linha):
                if valor != 0:
                    adjacentes.append((indice + 1, valor))
            lista_adjacencia.append((indice_vertice + 1, adjacentes))
        return lista_adjacencia

    def prim(self, vertice_inicial):
        if not self.lista_adjacencia:
            return []

        mst = []
        visitados = set()
        arestas = []

        def adicionar_arestas(vertice):
            visitados.add(vertice)
            for adjacente, peso in self.lista_adjacencia[vertice - 1][1]:
                if adjacente not in visitados:
                    heapq.heappush(arestas, (peso, vertice, adjacente))

        adicionar_arestas(vertice_inicial)

        while arestas and len(visitados) < len(self.lista_adjacencia):
            peso, vertice, adjacente = heapq.heappop(arestas)
            if adjacente not in visitados:
                mst.append((vertice, adjacente, peso))
                adicionar_arestas(adjacente)

        return mst

    def plotar_mst(self, mst):
        G = nx.Graph()
        for vertice, adjacentes in self.lista_adjacencia:
            G.add_node(vertice)
        for aresta in mst:
            G.add_edge(aresta[0], aresta[1], weight=aresta[2])

        pos = nx.spring_layout(G)
        plt.figure(figsize=(8, 6))

        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, edge_color='gray', linewidths=1,
                font_size=15)
        edge_labels = {(aresta[0], aresta[1]): aresta[2] for aresta in mst}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.title("Árvore Geradora Mínima (MST) - Algoritmo de Prim")
        plt.savefig("mst.png")
        plt.show()


def main():
    nome_arquivo = "grafo.txt"
    matrizes = ler_matrizes_de_arquivo(nome_arquivo)

    print("Selecione a matriz de adjacência (1 a {}):".format(len(matrizes)))
    for i, matriz in enumerate(matrizes, 1):
        print(f"Matriz {i}:\n{matriz}")

    escolha_matriz = int(input("Escolha a matriz: ")) - 1
    matriz_adjacencia = matrizes[escolha_matriz]

    grafo = Grafo(matriz_adjacencia)

    vertices = list(range(1, len(matriz_adjacencia) + 1))
    print(f"Vértices disponíveis: {vertices}")
    vertice_inicial = int(input("Escolha o vértice inicial: "))

    if vertice_inicial not in vertices:
        print("Vértice inválido. Usando o vértice 1 como padrão.")
        vertice_inicial = 1

    mst = grafo.prim(vertice_inicial)
    print("Árvore Geradora Mínima (MST) pelo algoritmo de Prim:")
    for aresta in mst:
        print(f"{aresta[0]} - {aresta[1]} (Peso: {aresta[2]})")

    grafo.plotar_mst(mst)


if __name__ == "__main__":
    main()
