from sklearn.model_selection import train_test_split
#Separo los datos de "train" en entrenamiento y prueba para probar los algoritmos
import numpy as np

def maqvec(x,y):
  X = np.array(x).T
  y = np.array(y)
  rep=[]
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
  #Defino el algoritmo a utilizar
  from sklearn.svm import SVC
  algoritmo = SVC(kernel = 'linear')
  #Entreno el modelo
  algoritmo.fit(X_train, y_train) 
  print(algoritmo.score(X_train, y_train))
  #Realizo una predicción
  y_pred = algoritmo.predict(X_test)
  #Verifico la matriz de Confusión
  from sklearn.metrics import confusion_matrix
  matriz = confusion_matrix(y_test, y_pred)
  print('Matriz de Confusión:')
  print(matriz)
  rep.append(str(matriz[0][0]))
  rep.append(str(matriz[0][1]))
  rep.append(str(matriz[1][0]))
  rep.append(str(matriz[1][1]))
  #Calculo la precisión del modelo
  from sklearn.metrics import precision_score
  precision = precision_score(y_test, y_pred, pos_label="1")
  print("Porcentaje de Positivos",round(matriz[0][0]/300,2))
  print("Porcentaje de Negativos",round(matriz[1][1]/300,2))
  print("Porcentaje de Error",round((matriz[0][1]+matriz[1][0])/300,2))
  print('Precisión del modelo:',round(precision,2))
  rep.append(str(precision))
  
  return rep