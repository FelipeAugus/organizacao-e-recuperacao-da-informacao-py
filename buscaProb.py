from bs4 import BeautifulSoup
import os
from numpy import mat
import yaml
import math 

from processamento import Stemming, Tokenize, getArquivos, preProcessaHtml

def calculaPesoDoDoc(query):
    query = trataQuery(query)
    arquivos = getArquivos()
    documentosRelevantes = getDocumentosRelevantes()
    if (not documentosRelevantes): documentosRelevantes = []

    pesosDosDoc = []

    N = len(arquivos) # Quant Documentos na coleção
    N += 1
    R = len(documentosRelevantes) # Quant Documentos relevantes
    
    pesos = {}
    for ti in query:
        n = getDocumentosContemTI(arquivos, ti) # documentos que contem ti
        r = getDocumentosContemTI(documentosRelevantes, ti) # documentos relevantes que contem ti

        # para evitar divisão por 0
        if(r>0): r -= 0.1

        if(not R): # se tiver vazio
            print("IDF")
            pesos[ti] = math.log(N/n)
        else:
            print("Documentos Relevantes")
            try: pesos[ti] = math.log( ( (r)*(N-R-n+r) / ((n-r)*(R-r)) ) )
            except: pesos[ti] = 0 # caso r = 0

    for arq in arquivos:
        similaridade = 0
        for ti in query:
            file = open(arq, 'r', encoding='latin-1')
            html = file.read()
            if(ti in html.lower()): 
                similaridade += pesos[ti]
        pesosDosDoc.append([similaridade, arq])

    # SaveMemory(pesosDosDoc, "pesosDosDoc")
    pesosDosDoc.sort(reverse=True)
    return pesosDosDoc

def setOrUnsetDocRelevante(arq, insert):
    documentosRelevantes = getDocumentosRelevantes()
    insert = int(insert)

    if (arq not in documentosRelevantes) and insert: # arq nao ta na lista e insert = true, adiciona ele 
        documentosRelevantes.append(arq)
        SaveMemory(documentosRelevantes, "documentosRelevantes")
    elif (arq in documentosRelevantes) and not insert: # arq na lista e insert = falso, remove ele da lista
        documentosRelevantes.remove(arq)
        SaveMemory(documentosRelevantes, "documentosRelevantes")

def getDocumentosRelevantes():
    documentosRelevantes = LoadMemory("documentosRelevantes")
    if(not documentosRelevantes): documentosRelevantes = []
    documentosRelevantes = [doc.replace('\\\\', '\\') for doc in documentosRelevantes]
    return documentosRelevantes

def getDocumentosContemTI(arquivos, ti):
    n = 0
    for arq in arquivos:
        file = open(arq, 'r', encoding='latin-1')
        html = file.read()

        if(ti in html.lower()): n+=1
    return n

def trataQuery(query):
    query = Tokenize(query)
    query = Stemming(query)
    return query

# Carrega os termos
def LoadMemory(arq):
    fileW = open(arq+".nlp", 'r', encoding="latin-1")
    termos = fileW.read()
    termos = yaml.safe_load(termos)
    return termos

# Salva os termos com as atualizações
def SaveMemory(w, arq):
    fileW = open(arq+".nlp", 'w', encoding="latin-1")
    fileW.write(str(w))
    fileW.close()
