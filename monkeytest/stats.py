import json
import os
from datetime import timedelta, datetime, time
from crypt import *

direc = os.getcwd()
stat_path = "ressources/stats.enc"

class stats:
    def __init__(self):
        self.averageWPM = 0.0
        self.avg_accu = 0.0
        self.total_train = 0
        self.time_spent = timedelta(0) 

        if os.path.exists(direc + '/' + stat_path):
            self.loadStats()

    def saveStats(self):
        jstats = {
            "avg_wpm": self.averageWPM,
            "avg_accu": self.avg_accu,
            "total_train": self.total_train,
            "time_spent": self.time_spent.strftime('%H:%M:%S')
        }
        res = json.dumps(jstats)
        encrypt(res.encode('utf-8'),stat_path)

    def loadStats(self):
        data = decrypt(stat_path)
        prop = json.loads(data)
        self.averageWPM = prop["avg_wpm"]
        self.avg_accu = prop["avg_accu"]
        self.total_train = prop["total_train"]
        self.time_spent = prop["time_spent"]

    def updateStats(self, wpm, ac, time):
        self.avg_accu = round((self.total_train * self.avg_accu + ac) / (self.total_train + 1),2)
        self.averageWPM = round((self.total_train * self.averageWPM + wpm) / (self.total_train + 1),2)
        self.total_train += 1
        self.time_spent = datetime.strptime(str(self.time_spent), '%H:%M:%S') + timedelta(seconds = time)
        print(type(self.time_spent))

    def resetStats(self):
        self.averageWPM = 0.0
        self.avg_accu = 0.0
        self.total_train = 0
        self.time_spent = time()
        self.saveStats()

