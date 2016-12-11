#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys


def map(u, v, p_u, p_v):
    '''

    :param u: node u
    :param v: nodo v
    :param p_u: número de partición de u
    :param p_v: número de partición de v
    :return:
    '''
    for a in range(1, NUM_PARTITIONS):
        for b in range(a + 1, NUM_PARTITIONS + 1):
            if {p_u, p_v}.issubset({a, b}):
                print '%s,%s.%s,%s.%s,%s.%s' % (a, b, u, v, p_u, p_v, NUM_PARTITIONS)

    if p_u != p_v:
        for a in range(1, NUM_PARTITIONS - 1):
            for b in range(a + 1, NUM_PARTITIONS):
                for c in range(b + 1, NUM_PARTITIONS + 1):
                    if {p_u, p_v}.issubset({a, b, c}):
                        print '%s,%s,%s.%s,%s.%s,%s.%s' % (a, b, c, u, v, p_u, p_v, NUM_PARTITIONS)



if __name__ == '__main__':
    if len(sys.argv) == 2:
        NUM_PARTITIONS = int(sys.argv[1])

    for line in sys.stdin:
        '''Si no es digito el primer carácter, entonces salta a la siguiente linea.'''
        if not line[0].isdigit():
            continue

        data = line.split()
        '''
        {u, v} = vertice

        p_u = número de partición del vertice u
        p_v = número de partición del vertice v
        '''
        u, v, p_u, p_v = int(data[0]), int(data[1]), int(data[2]), int(data[3])
        map(u, v, p_u, p_v)
