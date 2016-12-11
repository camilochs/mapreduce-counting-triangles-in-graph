#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import shlex
import json
from subprocess import call, check_output
from time import time

try:
    '''
    Se recibe las entradas de parametros:

    Primero: Nombre archivo del grafo
    Segundo: Número de particiones
    Tercero: Nombre de usuario en cluster.
    '''
    file_path = sys.argv[1]
    number_partitions = int(sys.argv[2])
    user_name = sys.argv[3]

    '''Path donde estoy ubicado'''
    current_path = os.path.dirname(os.path.abspath(__file__)) + '/'

    data = {
        "pruebas": []
    }

    """Se crea un json para los resultados si no existe"""
    if not os.path.isfile("tarea.json"):
        '''Crea el json'''
        out_file = open("tarea.json", "w")
        json.dump(data, out_file, indent=4)
        out_file.close()

    ''' Se cargan los resultados anteriores'''
    with open('tarea.json', 'r') as json_file:
        data = json.load(json_file)

        '''si no hay datos se crean'''
        if not data:
            data = {"pruebas": []}

    ### LISTA DE PASOS

    '''Primer comando, procesamos el grafo'''
    print 'Primer comando: '
    command_one = 'python pre_processing.py %s %s' % (file_path, number_partitions)
    print command_one
    print 'Procesando el grafo...'
    tiempo_inicial = time()
    call(shlex.split(command_one))

    '''Compruebo si existe el archivo en hadoop, si asi es, lo borro'''
    print 'Comprobando si ya existe el archivo...'
    remove_file = 'hadoop fs -rm /user/%s/%s' % (user_name, file_path)
    call(shlex.split(remove_file))

    '''Segundo comando, copio el grafo al sistema de archivos de hadoop'''
    print 'Segundo comando:'
    command_two = 'hadoop fs -copyFromLocal %s /user/%s' % (file_path, user_name)
    print command_two
    print 'Copiando archivo .txt(grafo) a hadoop...'
    call(shlex.split(command_two))


    '''Compruebo si existe la carpeta en hadoop, si asi es, lo borro'''
    print 'Comprobando si existe ya la carpeta...'
    remove_output_path = 'hadoop fs -rm -r -f /user/%s/output' % (user_name)
    call(shlex.split(remove_output_path))


    '''Tercer comando, inicio mapreduce, por default esta con 5 reduces.'''
    print 'Tercer comando:'
    command_three = 'time hadoop jar /opt/cloudera/parcels/CDH-5.8.2-1.cdh5.8.2.p0.3/jars/hadoop-streaming-2.6.0-cdh5.8.2.jar' \
                    ' -D stream.map.output.field.separator=. -D stream.num.map.output.key.fields=4' \
                    ' -D mapreduce.map.output.key.field.separator=.  -D mapreduce.partition.keypartitioner.options=-k1,1 ' \
                    '-D mapreduce.job.reduces=5 -D mapred.max.split.size=20  ' \
                    '-file %smapper.py -mapper "%smapper.py %s" ' \
                    '-file %sreducer.py -reducer %sreducer.py  ' \
                    '-input /user/%s/%s -output /user/%s/output ' \
                    '-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner' % (current_path, current_path,
                                                                                            number_partitions,
                                                                                            current_path, current_path,
                                                                                 user_name, file_path, user_name)

    print command_three
    print 'Realizando mapreduce...'
    call(shlex.split(command_three))

    '''Cuarto comando, realizo el getmerge para contar los triángulos'''
    print 'Cuarto comando:'
    command_four = 'hadoop fs -getmerge /user/%s/output %soutput.txt' % (user_name, current_path)
    print command_four
    print 'Realizando getmerge...'
    call(shlex.split(command_four))
    print "Archivo output.txt guardado en %s" % current_path


    print 'Quinto comando:'
    command_five = "awk '{ SUM+= $2 } END { printf(\"%.0f\", SUM); }' " \
                   + ("%soutput.txt" % current_path)
    print command_five
    print 'Contando los triángulos...'


    '''Se guarda el total de triángulos en una variable'''
    total_triangulos = check_output(shlex.split(command_five))

    print 'Número total de triángulos: %s' % total_triangulos

    '''Se calcula el tiempo de ejecución'''
    tiempo_final = time()
    tiempo_ejecucion = tiempo_final - tiempo_inicial

    print '\nFin'

    '''Se agregan los resultados al array de objetos'''
    data["pruebas"].append({
        "nombre_grafo": file_path,
        "tiempo_ejecucion": tiempo_ejecucion,
        "triangulos": total_triangulos,
        "particiones": number_partitions,
        "user_name": user_name
    })

    '''Se guardan los datos del array en un json'''
    with open('tarea.json', 'w') as outfile:
        json.dump(data,
                  outfile,
                  indent=4,
                  sort_keys=True,
                  separators=(',', ':')
                  )

except Exception as e:
    '''Se extrae la linea donde ocurrio el error.'''
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    print 'Ha ocurrido un error.', e.message
