from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPainter, QColor, QFontMetrics, QFont, QTextOption
from PyQt6.QtCore import Qt, QRectF
from markov import *

gap = 10

class ColoredLabel(QLabel):
    #Initialize text with markov generated string and text's rectangle
    def __init__(self, to_write, _rect, parent=None):
        super().__init__(parent)
        getProperMarkov(to_write)
        self.twri = to_write
        self.rect = _rect

    def setText(self, text):
        self.text = text
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        font = QFont(QFont('Andale Mono',18))
        font_metrics = QFontMetrics(font)
        option = QTextOption()
        option.setWrapMode(QTextOption.WrapMode.WrapAnywhere)
        x = 0
        nl = 0
        size = self.rect.left()

        #Print each char independently for color validation
        for i in range(len(self.twri)):
            #Every 10th word we jump to a newline
            if size-gap >= self.rect.right()-16:
                nl += 1
                size = self.rect.left()

            for j in range(len(self.twri[i])):
                grey = 255
                color = QColor(grey, grey, grey)
                ch = self.twri[i][j]

                #Check whether the char is good or not
                if i < len(self.text) and j < len(self.text[i]):
                    if ch == self.text[i][j]:
                        color = QColor(115,255,100)#Green
                    else:
                        color = QColor(255,88,100)#Red
                painter.setPen(color)
                painter.setFont(font)

                #Compute char position
                char_rect = QRectF(size + (j * gap), 
                                   self.rect.top()+nl*(gap+8), 
                                   gap, 
                                   self.rect.height())
                painter.drawText(char_rect, ch, option)
            #Store word size + space for next char
            size += (gap*(len(self.twri[i]))+gap+1)






