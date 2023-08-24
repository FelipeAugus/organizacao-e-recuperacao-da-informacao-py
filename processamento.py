from bs4 import BeautifulSoup
import re
import os
import nltk 
from nltk.stem import RSLPStemmer
from unidecode import unidecode
expression = '[!-@[-`{-¿ÆÐÑ×ØÝ-ßä-æëðñö-øý-ÿ]'

def Tokenize(a):
    a = nltk.word_tokenize(a)
    return a

#Joga a palavra apenas para raiz dela
def Stemming(a):
    stemmer = RSLPStemmer()
    phrase = []
    for word in a:
        phrase.append(stemmer.stem(word.lower()))
    return phrase

#Remode os "o", "de", "da"
def RemoveStopWords(a):
    stopwords = nltk.corpus.stopwords.words('portuguese')
    phrase = []
    for word in a:
        if word not in stopwords:
            phrase.append(word)
    return phrase

def getArquivos():
    caminhos = [os.path.join("./HTMLS", nome) for nome in os.listdir("./HTMLS")]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    arqsHtml = [arq for arq in arquivos if arq.lower().endswith((".html", ".htm"))]
    return arqsHtml

def getHtmls():
    arqsHtml = getArquivos()
    htmls = ""
    for arq in arqsHtml:
        file = open(arq, 'r', encoding='latin-1')
        htmls += file.read()
    
    return htmls

def preProcessaHtml(html):
    if html == "":
        html = getHtmls()

    soup = BeautifulSoup(str(html), "html.parser")
    
    bodys = soup.find_all("body")
    body = ""
    for b in bodys:
        body += b.get_text()+" "

    sentence = unidecode(body)
    # print(sentence)
    sentence = re.sub(expression, '', str(sentence))
    sentence = Tokenize(sentence)
    sentence = Stemming(sentence)
    sentence = RemoveStopWords(sentence)
    return sentence

def sortDict(dic):
    dicSort = {}
    for i in sorted(dic, key = dic.get, reverse=True):
        dicSort[i] = dic[i]
    return dicSort

def getPalavrasHtml(html = ""):
    palavras = {}
    sentence = preProcessaHtml(html)

    for word in sentence:
            if word not in list(palavras.keys()):
                palavras[word] = 1
            else:
                palavras[word] += 1

    palavras = sortDict(palavras)
    return palavras

import matplotlib.pyplot as plt
def plotaGraf(palavras):
    plt.figure(figsize=(15, 7))
    plt.bar(palavras.keys(), palavras.values())
    plt.xticks(range(len(palavras.values())), palavras.keys(), rotation=90)
    
    plt.savefig("./static/img/grafico.png")

