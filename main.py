import numpy as np

from controlador import modulo_jaccard as ja
from controlador import modulo_coseno as cs
from controlador import modulo_tweets as tw
from controlador import modulo_lec_escri as lc
from controlador import modulo_maquinavec as mv
from textblob import TextBlob 
from controlador import nlp as nl

##########################################
def categorizar(positivo,negativo):
  negativo = np.array(negativo)
  positivo = np.array(positivo)
  print('Vector Resultante')
  total = np.vstack((positivo, negativo)).T
  #print(total)
  temp1 = []
  contpos = 0
  contneg = 0
  contneutro = 0
  for temp in total:
    if temp[0] > temp[1]:
      temp1.append('Positivo')
      contpos += 1
    elif temp[0] == temp[1]:
      temp1.append('Neutro')
      contneutro +=1
    elif temp[0] < temp[1]:
      temp1.append('Negativo')
      contneg +=1

  for i in zip(total,temp1):
    print(i)
  print("Porcentaje de Positivos: ",round(contpos/len(total),2))
  print("Porcentaje de Negativos: ",round(contneg/len(total),2))
  print("Porcentaje de Neutros: ",round(contneutro/len(total),2))
  print("Total de Tweets: ",len(total))

###########EJECUCION###################3
from controlador import servidor as sv

sv.correr()

print("Literal 1")
tweet = tw.obtenerTweets(5) 
temp = tweet[:]
print(tweet)
tweet = nl.minusculas(tweet)
tweet = nl.eliminarce(tweet)
tweet = nl.tokenizar(tweet)
tweet = nl.qstopwords(tweet,1)
tweet = nl.stemmer(tweet)

dicposi = lc.leerTxt('modelo/dic_posi.txt')
dicneg = lc.leerTxt('modelo/dic_neg.txt')

print("***************Jaccard*********************")
#print('negativo')
negativo = ja.vectores(tweet,dicneg)
#print(negativo)
#print('positivo')
positivo = ja.vectores(tweet,dicposi)
#print(positivo)
categorizar(positivo,negativo)

print("\n*************Coseno*******************")
#print('negativo')
tweetneg = []
tweetneg.append(dicneg)
tweetneg = tweetneg+tweet
#print('inverted')
invertit = nl.inverted(tweetneg,dicneg)
#print("df")
df=cs.df(invertit)
#print("idf")
idf=cs.idf(df,len(invertit[0]))
#print("wtf")
wtf=cs.wtf(invertit)
#print("tf-idf")
tfidf = cs.tfidf(wtf,idf)
#print("modulo")
modulo= cs.modulo(wtf)
#print("longnomr")
longnorneg= cs.longnorm(wtf,modulo)
vectorneg = cs.vectordistance(longnorneg)
#print(vectorneg[1:,0])

#print('positivo')
tweetpos =[]
tweetpos.append(dicposi)
tweetpos = tweetpos+tweet
#print('inverted')
invertit = nl.inverted(tweetpos,dicposi)
#print("df")
df=cs.df(invertit)
#print("idf")
idf=cs.idf(df,len(invertit[0]))
#print("wtf")
wtf=cs.wtf(invertit)
#print("tf-idf")
tfidf = cs.tfidf(wtf,idf)
#print("modulo")
modulo= cs.modulo(wtf)
#print("longnomr")
longnorpos= cs.longnorm(wtf,modulo)
vectorpos = cs.vectordistance(longnorpos)
#print(vectorpos[1:,0])
categorizar(vectorpos[1:,0],vectorneg[1:,0])

print("literal 2")
tt,etiquetado = lc.leercsv('modelo/datasetGlobal.csv')
tt = nl.minusculas(tt[:1000])
tt = nl.eliminarce(tt)
tt = nl.tokenizar(tt)
tt = nl.qstopwords(tt,1)
tt = nl.stemmer(tt)
print('Generando Diccionario')
dic = nl.generardic(tt)
print('Generando Bolsa de Palabras')
bolsa = nl.inverted(tt,dic)
print('Maquina de Soporte Vectorial')
mv.maqvec(bolsa,etiquetado[:1000])

print("literal 3")
temp = nl.minusculas(temp)
temp = nl.eliminarce(temp)
print(temp[1])
c1 = TextBlob(temp[0]).translate(to="en")
print(c1.sentiment)

