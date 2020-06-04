from sklearn.model_selection import train_test_split
#Separo los datos de "train" en entrenamiento y prueba para probar los algoritmos
import numpy as np
def maqvec(x,y):
  X = np.array(x).T
  y = np.array(y)

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
  #Defino el algoritmo a utilizar
  from sklearn.svm import SVC
  algoritmo = SVC(kernel = 'linear')
  #Entreno el modelo
  algoritmo.fit(X_train, y_train)
  #Realizo una predicción
  y_pred = algoritmo.predict(X_test)
  #Verifico la matriz de Confusión
  from sklearn.metrics import confusion_matrix
  matriz = confusion_matrix(y_test, y_pred)
  print('Matriz de Confusión:')
  print(matriz)
  #Calculo la precisión del modelo
  from sklearn.metrics import precision_score
  precision = precision_score(y_test, y_pred, pos_label="1")
  print('Precisión del modelo:')
  print(precision)