#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys


class Graph:
    '''Clase para manejar los grafos'''

    def __init__(self):
        '''
        Inicializa las variables (constructor)
        '''
        self.edges = []
        self.nodes = {}

    def get_edges(self):
        '''
        Retorna los edges del grafo
        :return:
        '''
        return self.edges

    def get_nodes(self):
        '''
        Retorna los nodos(vertices) ordenados del grafo
        :return:
        '''
        _nodes = list(self.nodes.keys())
        _nodes.sort()
        return _nodes

    def get_total_nodes(self):
        '''
        Retorna el total de nodos
        :return:
        '''
        return len(self.nodes)

    def add_edges(self, u, v):
        '''
        Agrega los edges(aristas) al grafo
        :param u:
        :param v:
        :return:
        '''
        self.edges.append((u, v))
        if u not in self.nodes:
            self.nodes[u] = {}
        if v not in self.nodes:
            self.nodes[v] = {}

        '''En vez de utilizar una lista lo guardo en un diccionario'''
        if v not in self.nodes[u]:
            self.nodes[u][v] = v
        if u not in self.nodes[v]:
            self.nodes[v][u] = u

    def neighbors(self, node):
        '''
        Retorna los neighbors de un nodo especifico
        :param node:
        :return:
        '''

        return set(self.nodes[node])

    @staticmethod
    def intersection(neighbors_u, neighbors_v):
        '''
        Por ejemplo: intersection([1,2,3,4], [2,3]) -> retorna: [2,3]

        :param neighbors_u: lista de adyacentes de u
        :param neighbors_v: lista de adyacentes de v
        :return: lista de la intersección entre ambas listas.

        '''
        return neighbors_u.intersection(neighbors_v)

    def counting_triangles_dp(self):
        """
        Cuenta los triángulos en un grafo(versión programación dinamica)
        :return: Número de triángulos encontrados
        """
        neighbors = {}
        triangles = []
        for u in self.get_nodes():
            for v in [_v for _v in self.neighbors(u) if _v > u]:
                if v not in neighbors:
                    neighbors[v] = self.neighbors(v)
                for w in [_w for _w in Graph.intersection(self.neighbors(u), neighbors[v]) if _w > v]:
                    triangles.append((u, v, w))
        return triangles

    def counting_triangles(self):
        """
        Cuenta los triángulos en un grafo
        :return: Número de triángulos encontrados
        """
        triangles = []
        for u in self.get_nodes():
            for v in [_v for _v in self.neighbors(u) if _v > u]:
                for w in [_w for _w in Graph.intersection(self.neighbors(u), self.neighbors(v)) if _w > v]:
                    triangles.append((u, v, w))
        return triangles



'''Variables globales'''
partition_found = []
number_nodes_partition = {}


def reduce(partition_type, edges, NUM_PARTITIONS):
    '''

    :param partition_type: número del tipo de partición
    :param edges: lista de aristas
    :param NUM_PARTITIONS:  número de particiones elegido
    :return:
    '''

    graph = Graph()
    '''guarda los edges'''
    for e in edges:
        graph.add_edges(e[0], e[1])

    triangles = graph.counting_triangles()
    count = {}

    for t in triangles:
        tuple_triangle = (t[0], t[1], t[2])
        partion_nodes = tuple(number_nodes_partition[x] for x in t)
        if tuple_triangle not in count:
            count[tuple_triangle] = 0

        if partion_nodes[0] == partion_nodes[1] == partion_nodes[2]:
            print "%s,%s,%s %s" % (tuple_triangle[0], tuple_triangle[1], tuple_triangle[2], (1.0 / (NUM_PARTITIONS - 1)))

        else:

            print "%s,%s,%s %s" % (tuple_triangle[0], tuple_triangle[1], tuple_triangle[2], 1)


if __name__ == '__main__':

    partition_type_control = None

    for d in sys.stdin:
        info = d.split('.')
        '''Se recibe una estructura:
            n,n    .   n,n .   n,n .   n
            o
            n,n,n   .   n,n .   n,n .   n

            Primero es el número del tipo de partición(sub grafo),
            Segundo los edges(nodo v y u)
            Tercero el número de partición asignada a: v y u.
            Cuarto número de partición del grafo.
        '''
        NUM_PARTITION = int(info[3])

        number_node_partition = info[2].split(',')
        number_node_partition = [int(x) for x in number_node_partition]

        type_partition = info[0].split(',')
        type_partition = [int(y) for y in type_partition]

        edge = info[1].split(',')
        edge = [int(y) for y in edge]

        number_nodes_partition[edge[0]] = number_node_partition[0]
        number_nodes_partition[edge[1]] = number_node_partition[1]

        if partition_type_control is not None and type_partition != partition_type_control:
            reduce(partition_type_control, partition_found, NUM_PARTITION)
            partition_found = []

        partition_type_control = type_partition
        partition_found.append(edge)

    if len(partition_found) > 0:
        reduce(partition_type_control, partition_found, NUM_PARTITION)