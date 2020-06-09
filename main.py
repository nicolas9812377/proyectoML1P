from controlador import procesos as p  
p.topicmodeling()

from flask import Flask, render_template,request
import json 
app = Flask(__name__)


@app.route('/')
def hello_world(): 
  return render_template('index.html')

@app.route('/grafica')
def grafica(): 
  return render_template('LDA_Visualization.html') 

@app.route('/lit1',methods=['GET','POST'])
def recibircant():
  if request.method == 'POST':
    rs = p.literal1(int(request.values.get('cant')))
  return json.dumps(rs),{'Content-Type': 'application/json'}

@app.route('/lit2',methods=['GET','POST'])
def pedirMV():
  if request.method == 'POST':
    rs2 = p.literal2()
  return json.dumps(rs2),{'Content-Type': 'application/json'}

@app.route('/lit3',methods=['GET','POST'])
def recibirtweet():
  if request.method == 'POST':
    rs = p.literal3(str(request.values.get('tweet')))
  return json.dumps(rs),{'Content-Type': 'application/json'}

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=3000,debug=True)     
 