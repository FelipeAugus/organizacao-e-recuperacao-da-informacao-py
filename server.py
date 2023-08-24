
import flask
from flask import Flask
from flask import request
from flask import render_template
from werkzeug.utils import redirect
import os

from processamento import getPalavrasHtml, plotaGraf
from buscaBoll import buscaBoll
from buscaProb import calculaPesoDoDoc, setOrUnsetDocRelevante

UPLOAD_FOLDER = './HTML_Importado'

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def index():  
    try:
        return render_template('index.html')
    except:
        return "<H1>404 NOT FOUND </H1>"

@app.route("/palavras", methods = ['POST', 'GET'])
def returnPalavras():
    if request.method == 'POST':
        file = request.files['file']

        if file:
            file = file.stream.read().decode("latin-1")
            palavras = getPalavrasHtml(file)
            plotaGraf(palavras)
            return render_template('palavras.html', palavras = palavras)
        else:
            return redirect("/")

    elif request.method == 'GET':
        palavras = getPalavrasHtml()
        plotaGraf(palavras)
        return render_template('palavras.html', palavras = palavras)

def trataForm(dictForm):
    query = ''
    # first = True
    # boleanos = [ "and", "or", "not" ]
    for key in dictForm:
        query += dictForm[key]+" "
    return query

@app.route("/buscaBool", methods = ['POST', 'GET'])
def returnBuscaBoll():
    if request.method == 'POST':
        print(len(request.form))
        
        query = trataForm(request.form) # request.form['query']
        print("-"*50)
        print("QUERY: ", query)
        print("-"*50)
        resultList = buscaBoll(query, os.getcwd()+ '/HTMLS')

        return render_template('returnBool.html',
        query=query,
        resultList = resultList)

    elif request.method == 'GET':
        return render_template('buscaBool.html')


@app.route("/buscaProb", methods = ['POST', 'GET'])
def returnBuscaProb():
    if request.method == 'POST':
        arquivos = calculaPesoDoDoc(request.form['query'])

        return render_template('buscaProb.html',
            arquivos = arquivos)

    elif request.method == 'GET':
        return render_template('buscaProb.html')


@app.route("/buscaProb/setRelevante", methods = ['POST'])
def returnBuscaProbSetRelevante():
    print(request.form)
    setOrUnsetDocRelevante(request.form["nomeArquivo"], request.form["bool"])
    return render_template('buscaProb.html')

app.run()

# $env:FLASK_APP = "server"
# $env:FLASK_ENV = "development"
# flask run
