from markov import *
from PyQt6.QtCore import QTimer
from stats import *

#Main game class
class typeGame:
    def __init__(self,path,n):
        self.rd_textL = fullFunc(path, n-1) #Get words to write
        self.r1 = 0
        self.r2 = 0
        self.currWord = "" #Current word (avoid list searching)
        self.currSen = [""] #List of word written by user

        self.validW = 0 #Number of validated word
        self.wpm = round(0,2)
        self.wLetter = 0
        self.accu = 0
        self.time = 0
        self.timer = QTimer()

        self.stats = stats()

        self.is_launched = False
        self.end = False

#Update string when adding a char
    def updatePtrText(self,c):
        if (c == ' '):
            self.r2 = 0
            if self.checkCurr():
                self.validW += 1
            self.currSen.append("")
            self.currWord = ""
            self.r1 += 1
            if self.r1 >= len(self.rd_textL):
                self.end = True
        elif len(self.currWord) < len(self.rd_textL[self.r1]):
            self.currWord += c
            self.currSen[self.r1] += c
            if self.currSen[-1][-1]!=self.rd_textL[self.r1][self.r2]:
                self.wLetter += 1
            self.r2 += 1
            return True
        #print("sen :",self.currSen)
        return False

    #Update string when deleting last char
    def delLastPtrText(self):
        if self.r2 <= 0 and self.r1 > 0:
            self.r1 -= 1
            if self.currSen[self.r1] == self.rd_textL[self.r1]:
                self.validW -= 1
            self.r2 = len(self.currSen[self.r1])
            self.currWord = self.currSen[self.r1]
            self.currSen.pop()
            if self.rd_textL[self.r1] == self.currWord:
                return 9
            return (len(self.rd_textL[self.r1])-len(self.currWord))*8+9
        elif self.r2 > 0:
            self.r2 -= 1
            if self.currSen[-1][-1]!=self.rd_textL[self.r1][self.r2]:
                self.wLetter -= 1
            self.currWord = self.currWord[:-1]
            self.currSen[self.r1] = self.currSen[self.r1][:-1]

        #print("sen :",self.currSen)
        return 8

    #Check if word submited is valid or not
    def checkCurr(self):
        i = 0
        while i < len(self.rd_textL[self.r1]) and i < len(self.currWord) and self.rd_textL[self.r1][i] == self.currWord[i]:
            i += 1
        return i == len(self.rd_textL[self.r1]) and i == len(self.currWord)

    def LaunchTimer(self):
        self.is_launched = True
        self.timer.start(100)

#Game class limited by number of word that inherit from typeGame
class typeGameNum(typeGame):
    def __init__(self,path,n):
        super().__init__(path,n)
        self.time = 0
        self.timer.timeout.connect(self.updateTimer)

    def updateTimer(self):
        self.time = round(self.time + 0.1,1)
        if self.end:
            self.timer.stop()
            self.computeStats()
            self.stats.updateStats(self.wpm, self.accu, self.time)
            self.stats.saveStats()

    def computeStats(self):
        if self.time == 0:
            self.wpm = round(self.validW,1)
        else:
            self.wpm = round(self.validW*100/self.time,1)
        
        total_len = 0
        for w in self.currSen: 
            total_len+=len(w)
        if total_len <= 0:
            self.accu = round(0,1)
        else:
            self.accu=round((total_len-self.wLetter)*100/total_len,1)

#Game class limited by time that inherit from typeGame
class typeGameTime(typeGame):
    def __init__(self, path, count):
        super().__init__(path,50)
        self.setted_time = count
        self.time = count
        self.timer.timeout.connect(self.updateTimer)

    def updateTimer(self):
        self.time = round(self.time - 0.1,1)
        if self.time <= 0:
            self.end = True
            self.timer.stop()
            self.computeStats()
            self.stats.updateStats(self.wpm, self.accu,self.setted_time)
            self.stats.saveStats()

    def computeStats(self):
        if self.time == 0:
            self.wpm = round(self.validW*100/self.setted_time,2)
        else:
            val = self.setted_time-self.time
            if val == 0:
                self.wpm = round(0,1)
            else:
                self.wpm = round(self.validW*100/val,1)

        total_len = 1
        for w in self.currSen: 
            total_len+=len(w)
        if total_len <= 0:
            self.accu = round(0,2)
        else:
            self.accu=round((total_len-self.wLetter)*100/total_len,1)

