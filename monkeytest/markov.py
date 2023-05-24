import random as rand
import json
from crypt import *

#Extract text from file at 'path'
def GetText(path):
    fi = open(path, 'r')
    return fi.read().lower()

#Extract the word from 'text' space-separated (punctuation is
#counted in)
def GetWordList(text):
    tmp = ""
    res = []
    for i in range(len(text)):
        ch = text[i]
        if (ch >= 'a' and ch <= 'z'):
            tmp += ch
        elif len(tmp)>0:
            res.append(tmp)
            tmp = ""
        if ['.','!','?',','].count(ch) > 0:
            if res[-1] not in ['.','!','?',',']: 
                res.append(ch) 
    return res

#Train a markov chain from word list 'wlist'
def trainMarkov(wlist):
    res = dict()
    i = 0
    res["START"] = [[wlist[0], wlist[1]]]
    res["END"] = []

    for w in wlist:
        if not w in res:
            res[w] = []
        if i < len(wlist)-2:
            tmp = []
            tmp.append(wlist[i+1])
            tmp.append(wlist[i+2])
            if w in ['.','?','!']:
                res['START'].append(tmp)
            else:
                res[w].append(tmp)
        i += 1
    return res

#Combine the three function to return a markov bank
def getBank(path):
    text = GetText(path)
    dic = GetWordList(text)
    bank = trainMarkov(dic)
    return bank

#Generate a harsh markov chain in a string list
def genMarkov(n, bank):
    res = []
    i = 0
    curr = 'START'

    while i < n+1:

        cb = bank[curr]
        if len(cb) > 0:
            r = rand.randint(0,len(cb)-1)
            w1 = cb[r][0]
            w2 = cb[r][1]
            if w2 in ['.','?','!']:
                curr = 'START'
            else:
                curr = w2
            res.append(w1)
            res.append(w2)
        i += 2
    return res

#Transform markov generation to a list into a proper list
#for the usage we have
def getProperMarkov(markov):
    i = 0
    a = markov[0][0].upper()
    markov[0] = a + markov[0][1:]

    if markov[0] in ["Im","Ive","Id"]:
        b = markov[0][0] + "'"
        markov[0] = b + markov[0][1:]

    while i < len(markov):
        w = markov[i]
        if w in ['.',',']:
            markov[i-1] += w
            markov.pop(i)
            i -= 1
        elif i > 0 and markov[i-1][-1] in ['.','?','!']:
            b = w[0].upper()
            markov[i] = b + w[1:]
        elif w in ["im","ive","id","i"]:
            b = w[0].upper()
            if len(w) > 1:
                b += "'"
            markov[i] = b + w[1:]
        i += 1

def fullFunc(path, n):
    bank = LoadBank(path) 
    res = genMarkov(n , bank)
    getProperMarkov(res)
    return res

def getStr(propMark):
    res = ""
    for elm in propMark:
        res += elm + ' '
    return res

def SaveBank(bank, name):
    res = json.dumps(bank)
    encrypt(res.encode('utf-8'),name)

def LoadBank(name):
    data = decrypt()
    res = json.loads(data)
    return res
