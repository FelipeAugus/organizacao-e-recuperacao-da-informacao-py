from codecs import decode
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer 
from bs4 import BeautifulSoup

boolean_operators = {"and","or","not"}
stop_words = set(stopwords.words('portuguese'))
stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])
lemmatizer = WordNetLemmatizer() 

def lemmatize_fun(lemmatizer,sentence):
    filtered_sentence = []
    for w in sentence:
            if lemmatizer.lemmatize(w)!=w:
                filtered_sentence.append(lemmatizer.lemmatize(w))
            elif lemmatizer.lemmatize(w,'v')!=w:
                filtered_sentence.append(lemmatizer.lemmatize(w,'v'))
            elif lemmatizer.lemmatize(w,'a')!=w:
                filtered_sentence.append(lemmatizer.lemmatize(w,'a'))
            elif lemmatizer.lemmatize(w,'r')!=w:
                filtered_sentence.append(lemmatizer.lemmatize(w,'r'))
            else:
                filtered_sentence.append(w)
    return filtered_sentence

def create_list(posting_list,word):
    list_new = []
    if  word not in posting_list:
        return list_new
    for element in posting_list[word]:
        if isinstance(element, str):
            list_new.append(element)
    return list_new

def union(posting_list,result_list,word):
    list_word = create_list(posting_list,word)
    set1 = set(list_word)
    set2 = set(result_list)
    return set1.union(set2)

def merge_intersect(posting_list,result_list,word):
    list_word = create_list(posting_list,word)
    set1 = set(list_word)
    set2 = set(result_list)
    set2 = set1.intersection(set2)
    return list(set2)

def difference(posting_list,result_list,word):
    list_word = create_list(posting_list,word)
    set1 = set(list_word)
    set2 = set(result_list)
    return list(set2.difference(set1))

def print_content(filename):
    print("FILENAME ---> ", filename)

def getDocumentsBoll(path):
    freq_count = {}
    posting_list = {}
    
    for filename in os.listdir(path):
        filePath = path+'/'+filename

        html =  open(filePath, 'r', encoding='latin-1').read()
        soup = BeautifulSoup(str(html), "html.parser")
        text = soup.find("body").get_text()

        #Removing Stopwords:
        temp = word_tokenize(text)
        filtered_sentence_0 = [] 
        for w in temp:
            if w.lower() not in stop_words:
                filtered_sentence_0.append(w.lower())
        filtered_sentence = lemmatize_fun(lemmatizer,filtered_sentence_0)

        #Printing the filtered important words of document      

        #Word frequency updation:
        for token in filtered_sentence:
            if token in freq_count: 
                freq_count[token] = freq_count[token] + 1
            else:
                freq_count[token] = 1

        #Document frequency updation:
        doc_freq = {}
        for token in filtered_sentence:
            if token in doc_freq: 
                doc_freq[token] = doc_freq[token] + 1
            else:
                doc_freq[token] = 1
 
        #Posting List Creation and Updation:
        for token in filtered_sentence:
            if token not in posting_list:
                posting_list[token] = []
            if filename not in posting_list[token]:     
                posting_list[token].append(filename)
                posting_list[token].append(doc_freq[token])
    return posting_list

def buscaBoll(query, path):
    posting_list = getDocumentsBoll(path)
    
    temp = word_tokenize(query) 
    filtered_sentence_0 = [] 
    for w in temp: 
        if (w.lower() not in stop_words) or (w.lower() in boolean_operators):   
            filtered_sentence_0.append(w.lower())
    filtered_sentence = lemmatize_fun(lemmatizer,filtered_sentence_0)
        
    result_list = {}
    length = len(filtered_sentence)  
    i = 0
    while i < length:
        if i == 0:
            result_list = create_list(posting_list,filtered_sentence[0])
            i=i+1
            continue
        if filtered_sentence[i] in boolean_operators:
            if filtered_sentence[i] == "and":
                result_list = merge_intersect(posting_list,result_list,filtered_sentence[i+1])
                i = i+1
            elif filtered_sentence[i] == "or":
                result_list = union(posting_list,result_list,filtered_sentence[i+1]) 
                i = i+1
            else:
                result_list = difference(posting_list,result_list,filtered_sentence[i+1])
                i = i+1
        else:
            result_list = merge_intersect(posting_list,result_list,filtered_sentence[i])
            i = i+1
        
    return result_list
