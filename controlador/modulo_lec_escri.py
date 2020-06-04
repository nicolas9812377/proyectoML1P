import csv
from controlador import nlp as nl
###############LEER DATASET###############
def leercsv(nombre):
  tweet = []
  etiquetado = []
  with open(nombre, 'r', encoding = "utf-8") as csvfile:#abre documento en forma de lectura
      leer = csv.DictReader(csvfile, delimiter=',')
      for row in leer:#recorre lineas del documentp
        tweet.append(row['texto'])
        etiquetado.append(row['cs'])
  return tweet,etiquetado
#####################################################
###########LEER TXT#################################
def leerTxt(nombre):
  f = open (nombre,'r')
  palabrasneg = []
  temp = []
  for linea in f.readlines():
    temp.append(linea.strip('\n'))
  palabrasneg.append(temp)
  palabrasneg = nl.stemmer(palabrasneg)
  palabrasneg = palabrasneg[0]
  f.close()
  return palabrasneg
######################################
#####################GUARDAR CSV#################
def guardarCSV(nombre,tit):
  with open(nombre, 'a',encoding='utf-8') as csvfile:#abre documento y escribe
    writer = csv.writer(csvfile, delimiter=',')#escribe en documento
    writer.writerows(tit)
    return True#retorna verdadero si no hubo problemas
  return False#retorna falso en caso de error
###################################################