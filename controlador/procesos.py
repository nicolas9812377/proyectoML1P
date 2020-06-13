import numpy as np
from controlador import modulo_jaccard as ja
from controlador import modulo_coseno as cs
from controlador import modulo_tweets as tw
from controlador import modulo_lec_escri as lc
from controlador import modulo_maquinavec as mv
from textblob import TextBlob 

from controlador import nlp as nl

##############CALCULADOR########################
def categorizar(positivo,negativo):
  negativo = np.array(negativo)
  positivo = np.array(positivo)
  print('Vector Resultante')
  total = np.vstack((positivo, negativo)).T
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

  #for i in zip(total,temp1):
  #  print(i)
  
  print("Porcentaje de Positivos: ",round(contpos/len(total),2))
  print("Porcentaje de Negativos: ",round(contneg/len(total),2))
  print("Porcentaje de Neutros: ",round(contneutro/len(total),2))
  print("Total de Tweets: ",len(total))
  return [round(contpos/len(total),2),round(contneg/len(total),2),round(contneutro/len(total),2),len(total)],temp1
##########################################################

###########LITERAL 1###################
def literal1(n):
  rs = []
  print("Literal 1")
  #Consultando Tweets
  tweet = tw.obtenerTweets(n) 
  temp = tweet[:]
  #Proceso NLP
  tweet = nl.minusculas(tweet)
  tweet = nl.eliminarce(tweet)
  tweet = nl.tokenizar(tweet)
  tweet = nl.qstopwords(tweet,1)
  #Obteniendo Diccionarios
  dicposi = lc.leerTxt('modelo/dic_posi.txt')
  dicneg = lc.leerTxt('modelo/dic_neg.txt')
  
  print("***************Jaccard*********************")
  #Jaccard de Negativos
  negativo = ja.vectores(tweet,dicneg)
  #Jaccard de Positivos
  positivo = ja.vectores(tweet,dicposi)
  #Obteniendo Resultados
  est1, cl1 = categorizar(positivo,negativo)
  rs.append(est1)
  

  print("\n*************Coseno*******************")
  #Coseno de Negativos
  tweetneg = []
  tweetneg.append(dicneg)
  tweetneg = tweetneg+tweet
  invertit = nl.inverted(tweetneg,dicneg)
  df=cs.df(invertit)
  idf=cs.idf(df,len(invertit[0]))
  wtf=cs.wtf(invertit)
  tfidf = cs.tfidf(wtf,idf)
  modulo= cs.modulo(tfidf)
  longnorneg= cs.longnorm(tfidf,modulo)
  vectorneg = cs.vectordistance(longnorneg)
  #Coseno de Positivos
  tweetpos =[]
  tweetpos.append(dicposi)
  tweetpos = tweetpos+tweet
  invertit = nl.inverted(tweetpos,dicposi)
  df=cs.df(invertit)
  idf=cs.idf(df,len(invertit[0]))
  wtf=cs.wtf(invertit)
  tfidf = cs.tfidf(wtf,idf)
  modulo= cs.modulo(tfidf)
  longnorpos= cs.longnorm(tfidf,modulo)
  vectorpos = cs.vectordistance(longnorpos)
  #Obteniendo Resultados, columnas = vectorneg[0,1:]
  # filas = vectorneg[1:,0]
  est, cl = categorizar(vectorpos[1:,0],vectorneg[1:,0])

  rs.append(est)
  rs.append(cl1)
  rs.append(cl)
  rs.append(temp[:8])
  
  return rs
##########################################################
def topicmodeling(n):
  import gensim
  import pyLDAvis
  import pyLDAvis.gensim 
  from nltk.corpus import stopwords
  import gensim.corpora as corpora  
  from wordcloud import WordCloud

  tpm = []
  n4 = stopwords.words('spanish')
  n4 += stopwords.words('english')
  n4.append('gt')
  n4.append('oms')
  n4.append('así')
  n4.append('aquí')

  print("Topic Modeling")
  tweet = tw.obtenerTweets(n) 
  tweet = nl.minusculas(tweet)
  tweet = nl.eliminarce(tweet)
  tt = tweet[:]
  tweet = nl.tokenizar(tweet)
  tweet = nl.qstopwords(tweet,1)
  
  #Diccionario
  id2word = corpora.Dictionary(tweet)
  #Bolsa de palabras
  corpus = [id2word.doc2bow(text) for text in tweet]

  lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,id2word=id2word,num_topics=4,alpha='auto')

  topics = []
  for idx, topic in lda_model.print_topics(-1):
    tp = topic.split('+')
    tp = [w.split('*') for w in tp] 
    topics.append(tp)

  tpm.append(topics)

  temp = []
  for top in topics:
    t = []
    for j in top:
      t.append(j[1].replace('"','').strip())
    temp.append(t)

  print(temp)

  #Obteniendo Diccionarios
  dicposi = lc.leerTxt('modelo/dic_posi.txt')
  dicneg = lc.leerTxt('modelo/dic_neg.txt')

  print("***************Jaccard Topics***************")
  #Jaccard de Negativos
  negativo = ja.vectores(temp,dicneg)
  #Jaccard de Positivos
  positivo = ja.vectores(temp,dicposi)
  #Obteniendo Resultados
  est1, cl1 = categorizar(positivo,negativo)

  tpm.append(est1)
  tpm.append(cl1)
  
  vis = pyLDAvis.gensim.prepare(lda_model,corpus,id2word) 
  pyLDAvis.save_html(vis,'templates/LDA_Visualization.html')

  for i in range(4):
    wordcloud = WordCloud(stopwords=n4,max_font_size=50, max_words=100, background_color="white").generate(tt[i])
    wordcloud.to_file("static/wordc/"+str(i)+".png")

  return tpm
###############LITERAL 2###############################
def literal2():
  print("literal 2")
  #Lee el DatasetGlobal.csv
  tt,etiquetado = lc.leercsv('modelo/datasetGlobal.csv')
  #Proceso NLP
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
  return mv.maqvec(bolsa,etiquetado[:1000])
#######################################################

##############LITERAL ###########################
def literal3(frase):
  temp = []
  print("literal 3")
  temp.append(frase)
  temp = nl.minusculas(temp)
  temp = nl.eliminarce(temp)
  try:
   c1 = TextBlob(frase).translate(from_lang='es',to='en')
   print(c1.sentiment)
   return c1.sentiment
  except:
    print('corregido error')
    return [0,0]
################################################## 