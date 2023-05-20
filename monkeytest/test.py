import sys
from PyQt6.QtWidgets import  QApplication, QWidget, QLineEdit, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QKeySequence, QPalette, QLinearGradient, QColor, QPixmap, QImage, QBrush
from PyQt6.QtCore import Qt, QTimer, QRectF, QPropertyAnimation, QPoint, QSize
from PyQt6.QtGui import *
from PyQt6 import QtQuick
from colorLet import *
from game import *

path = "Wbank.enc"

styleS = """border-style: solid;
            border-width: 2px;
            border-color: #fceaa1;
            border-radius: 3px"""

ListWord = [30,60,100]
ListTime = [30,60,90]

class MainWindow(QWidget):
    def __init__(self,mode,ind):
        super().__init__()
        
        #Initialize window and game
        self.setWindowTitle("FTTS")        
        #self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.wi = 1200
        self.he = 600
        self.setFixedSize(self.wi,self.he)

        oImage = QImage("ressources/FTTS_backv3.png")
        if oImage.isNull():
            raise Exception("""You are missing an image ! 
           Go download 'ressources/FTTS_backv3.png' 
           from https://github.com/panpanDKC/FTTS""")

        sImage = oImage.scaled(QSize(self.wi,self.he))
        pal = QPalette()
        pal.setBrush(QPalette.ColorRole.Window, QBrush(sImage))
        self.setPalette(pal)
        
        #Initalize game mode bool and mode label
        self.chooseGame = QLabel(self)
        self.chooseGame.setFont(QFont('Andale Mono',15))
        self.chooseGame.setGeometry(460,10,280,30)
        self.chooseGame.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gameMode = mode
        self.chooseGame.setStyleSheet("""border-style: solid; 
                                      border-width: 2px; 
                                      border-color: #fceaa1;
                                      border-radius: 3px""")#fff0b8
        self.ListInd = ind
        self.List = QLabel(self)        
        self.List.setFont(QFont('Andale Mono',18))
        self.List.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.List.setGeometry(505,560,350,30)

        rect_select = QLabel(self)
        rect_select.setGeometry(501+self.ListInd*43,556,30,30)
        rect_select.setStyleSheet("""
                                  border-style: solid;
                                  border-width: 2px;
                                  border-color: #fceaa1;
                                  border-radius: 3px
                                  """)

        #Indicate user how to choose game length
        self.indicA = QLabel(self)
        self.indicA.setFont(QFont('Andale Mono',10))
        self.indicA.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.indicA.setGeometry(460,530,280,30)
        self.indicA.setText("Use ◀ or ▶ to select")

        #Indicate user how to switch game mode
        self.indicB = QLabel(self)
        self.indicB.setFont(QFont('Andale Mono',10))
        self.indicB.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.indicB.setGeometry(460,35,280,30)
        self.indicB.setText("Press Shift + Backspace to change")
       
        #Choose game mode based on 'mode' bool
        if mode:
            self.ty_game = typeGameNum(path, ListWord[self.ListInd])
            self.chooseGame.setText("You are playing Normal Mode")
            self.List.setText("30  60  100 words")
            if self.ListInd == 2:
                rect_select.setGeometry(501+self.ListInd*43,556,42,30)
        else:
            self.ty_game = typeGameTime(path, ListTime[self.ListInd])
            self.chooseGame.setText("You are playing Time Mode")
            self.List.setText("30  60  90 seconds")
        
        #Shortcut for game's stats
        self.stats = self.ty_game.stats

        #---- Stats text area ----
        wcol = defineColor(60,40,self.stats.averageWPM)
        acol = defineColor(95,85,self.stats.avg_accu)

        statText = ("Average WPM : "+
                wcol + str(self.stats.averageWPM)+"</span>"+"<br>"
                    +"Average Accu : " + 
                acol + str(self.stats.avg_accu)+"</span>"+"<br>"
            +"Training Done : "+str(self.stats.total_train)+"<br>"
            +"Time spent : "+str(self.stats.time_spent))

        self.statsT = QLabel(self)
        self.statsT.setFont(QFont('Andale Mono',15))
        self.statsT.setText(statText)
        self.statsT.setAlignment(Qt.AlignmentFlag.AlignLeft | 
                                 Qt.AlignmentFlag.AlignVCenter)
        self.statsT.setGeometry(20,
                                int(self.he - 95),
                                200,
                                80)
        self.statsT.setStyleSheet(styleS)
                
        #---- Main text area ----
        self.rect = QRectF(400,200,500,100)#width: 500
        self.centerRect()
        self.test = ColoredLabel(self.ty_game.rd_textL, self.rect)
        self.test.setText(self.ty_game.currSen)
        self.test.setWordWrap(True)
        self.test.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        #Statistic label
        #Word per minutes
        self.wpm = QLabel(self)
        self.wpm.setFont(QFont('Andale Mono',20))
        self.wpm.setText(str(self.ty_game.wpm)+"wpm")
        self.wpm.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.wpm.setGeometry(410,280,120,70)

        #Accuracy
        self.accu = QLabel(self)
        self.accu.setFont(QFont('Andale Mono',20))
        self.accu.setText('⌖'+str(self.ty_game.accu)+'%')
        self.accu.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.accu.setGeometry(540,280,120,70)

        #Set the text cursor
        self.cursor = QLabel(self)
        self.cursor.setFont(QFont('Andale Mono',15))
        self.cursor.setText("|")
        self.cursor.setGeometry(int(self.rect.left())+16,
                                int(self.rect.top())+20,
                                15,
                                15)
        self.cursor.setVisible(True)
        self.cursor_timer = QTimer()
        self.cursor_timer.timeout.connect(self.cursorBlink)
        self.cursor_timer.start(500)
        self.lastP = 0 #Last postion of cursor before spacing
        
        #Initialize timer and timer's label
        self.time = QLabel(self)
        self.time.setFont(QFont('Andale Mono',20))
        self.time.setText(str(self.ty_game.time)+"s")
        self.time.setGeometry(700,280,120,70)
        self.refT = QTimer()
        self.refT.timeout.connect(self.updTime)
        self.refT.start(100)
        #-------------
        
        #Boolean that show if 'SHIFT' is pressed
        self.shiftT = False
        self.ctrlT = False

        #Initialise Layout
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.test)
        self.setLayout(vlayout)

    #Catch key event (char, validation, shortcut, ...)
    def keyPressEvent(self,event):
        k = event.key()
        if k == Qt.Key.Key_Shift:
            self.shiftT = True

        if k == Qt.Key.Key_Control:
            self.ctrlT = True

        #Check if user want to restart game
        if self.shiftT and k == Qt.Key.Key_Return:
            self.w = MainWindow(self.gameMode, self.ListInd)
            self.w.show()
            self.close()

        #Check if user want to change game mode
        if self.shiftT and k == Qt.Key.Key_Backspace:
            self.w = MainWindow(not self.gameMode, 0)
            self.w.show()
            self.close()

        if self.shiftT and self.ctrlT and k == 82: #'r' char code
            self.ty_game.stats.resetStats()
            self.w = MainWindow(self.gameMode, self.ListInd)
            self.w.show()
            self.close()

        if k == Qt.Key.Key_Left:
            if self.ListInd > 0:
                self.w = MainWindow(self.gameMode, self.ListInd - 1)
                self.w.show()
                self.close()
            else:
                return

        if k == Qt.Key.Key_Right:
            if self.ListInd < 2:
                self.w = MainWindow(self.gameMode, self.ListInd + 1)
                self.w.show()
                self.close()
            else:
                return

        #Check if game is done
        if self.ty_game.end:
            self.ty_game.end = True
            return

        #Check if game is launched
        if not self.ty_game.is_launched:
            self.ty_game.LaunchTimer()

        x,y = self.cursor.x(),self.cursor.y()

        #Check what key is pressed
        if k == Qt.Key.Key_Space:
            #Extra spaceing for cursor if word not fully written
            if self.ty_game.rd_textL[self.ty_game.r1] != self.ty_game.currWord:
                x += ((len(self.ty_game.rd_textL[self.ty_game.r1])
                       - len(self.ty_game.currWord)) * 8)
            #Check if cursor needs to go down
            if x >= self.rect.right():
                self.lastP = x
                x = int(self.rect.left())+7
                y += 15
            
            self.ty_game.updatePtrText(' ')
            self.cursor.move(x+9,y)
        
        #Check if user want to erase last char
        elif k == Qt.Key.Key_Backspace:
            if x < self.rect.left()+18:
                x = self.lastP+8
                y -= 14
            x -= self.ty_game.delLastPtrText()
            self.cursor.move(x,y)

        #Check if user input is a char
        elif (k >= 65 and k <= 90):#Looking for char
            ch = chr(k + 32 * (not self.shiftT))
            if self.ty_game.updatePtrText(ch):
                self.cursor.move(x+8,y)
        
        #Check if user input is punctuation
        elif k in [44,46,33,63]:#Looking for [',','.','!','?']
            if self.ty_game.updatePtrText(chr(k)):
                self.cursor.move(x+8,y)
        self.test.setText(self.ty_game.currSen)
    
    #Catch when Shift key is released
    def keyReleaseEvent(self, event):
        k = event.key()
        if k == Qt.Key.Key_Shift:
            self.shiftT = False
        
        if k == Qt.Key.Key_Control:
            self.ctrlT = False

    #Update stats labels
    def updTime(self):
        self.time.setText(str(self.ty_game.time)+"s")
        self.ty_game.computeStats()
        wpm = self.ty_game.wpm
        acc = self.ty_game.accu
        wpm_format = defineColor(60,40,wpm)
        acc_format = defineColor(95,85,acc)
        wpm_out = wpm_format + str(wpm) + "wpm" + "</span>"
        acc_out = acc_format + '⌖' + str(acc) + '%' + "</span>"
        self.wpm.setText(wpm_out)
        self.accu.setText(acc_out)
    
    #Update main text label
    def updDispText():
        self.test.setText()
    
    #Center main text rect
    def centerRect(self):
        # Get the size of the widget
        wi = self.width()
        hg = self.height()
        
        x,y = (wi/2,hg/2)
        
        self.rect.moveTo(x-(self.rect.width()/2)-22,
                         y-(self.rect.height()/2)+70)
    
    #Make cursor blinking
    def cursorBlink(self):
        self.cursor.setVisible(not self.cursor.isVisible())

#Define stats color based on arguments
def defineColor(topB, midB, var):
    if var >= topB:
        return "<span style='color:rgb(115,255,100)'>"
    elif var >= midB:
        return "<span style='color:rgb(255,180,140)'>"
    return "<span style='color:rgb(255,88,100)'>"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow(True, 0)
    win.show()
    sys.exit(app.exec())
