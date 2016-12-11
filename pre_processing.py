#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import fileinput
import math

'''variables globales'''
NUM_PARTITIONS = None
partition = {}
nodes = {}


def assign_partions_to_nodes(total_nodes):
    global nodes
    '''

    Asigno el número de partición a cada vertice
    :param total_nodes: cantidad de nodos
    :return:
    '''
    ct = 1
    num_partition = 1

    total_graph_partition = math.ceil(total_nodes / (NUM_PARTITIONS * 1.0))

    nodes = list(nodes.keys())
    nodes.sort()

    for i in nodes:
        if ct % total_graph_partition == 0:
            partition[i] = num_partition
            num_partition += 1
        else:
            partition[i] = num_partition
        ct += 1

if __name__ == '__main__':

    filename = ''
    print sys.argv
    if len(sys.argv) == 3:
        filename = sys.argv[1]
        NUM_PARTITIONS = int(sys.argv[2])
    else:
        print 'Incorrecto número de parametros'
        sys.exit()

    file = open(filename, 'r')

    for line in file:
        if not line[0].isdigit():
            continue
        line = line.split()
        '''Carga los edges al grafo'''
        nodes[int(line[0])] = int(line[0])
        nodes[int(line[1])] = int(line[1])

    '''Asigno el número de partición a cada vertice'''
    assign_partions_to_nodes(len(nodes.keys()))

    for line in fileinput.FileInput(filename, inplace=1):

        '''Salto las filas que no son digitos'''
        if not line[0].isdigit():
            continue

        '''
        Se agrega el número de partición a cada uno de los dos vertices:
        por ejemplo:
        edges -> 1 2
        número de particiones -> 1 1
        entonces la linea queda:
        1   2   1   1
        '''
        data = line.split()
        line += ('\t%s\t%s' % (partition[int(data[0])], partition[int(data[1])]))
        line = line.replace("\r", "").replace("\n", "")
        print line
