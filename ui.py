#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import network
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QPen, QPalette, QColor
from PyQt5.QtCore import Qt

class PaintArea(QWidget):
    def __init__(self):
        super(PaintArea, self).__init__()
        QWidget.__init__(self, None)
        self.resize(280, 280)       
        self.setMouseTracking(False) #setMouseTracking设置为False，否则不按下鼠标时也会跟踪鼠标事件
        self.pos_xy = [] #将按住鼠标后移动的点保存下来
        palette1 = QPalette()
        palette1.setColor(self.backgroundRole(), QColor(192,253,123))   # 设置背景颜色
        self.setPalette(palette1)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        pen = QPen(Qt.black, 10, Qt.SolidLine)
        painter.setPen(pen)
        if len(self.pos_xy) > 1:
            point_start = self.pos_xy[0]
            for pos_tmp in self.pos_xy:
                point_end = pos_tmp
                if point_end == (-1, -1):
                    point_start = (-1, -1)
                    continue
                if point_start == (-1, -1):
                    point_start = point_end
                    continue
                painter.drawLine(point_start[0], point_start[1], point_end[0], point_end[1])
                point_start = point_end
        painter.end()
    
    def mouseMoveEvent(self, event):
        pos_tmp = (event.pos().x(), event.pos().y())
        self.pos_xy.append(pos_tmp)
        self.update()

    def mouseReleaseEvent(self, event):
        pos_test = (-1, -1)
        self.pos_xy.append(pos_test)
        self.update()

class MainWindow(QWidget):
    def __init__(self):
        QMainWindow.__init__(self)
        self.clearButton = QPushButton('clear')
        self.identifyButton = QPushButton('identify')
        self.resultLabel = QLabel('result:') 
        self.resultLineText = QLineEdit()
        self.resultLayout = QHBoxLayout()
        self.resultLayout.addWidget(self.resultLabel)
        self.resultLayout.addWidget(self.resultLineText)
        self.trainButton = QPushButton('train')
        # self.buttonLayout = QVBoxLayout()
        # self.buttonLayout.addWidget(self.clearButton)  
        # self.buttonLayout.addWidget(self.identifyButton)
        # self.buttonLayout.addWidget(self.resultLabel)
        self.paintArea = PaintArea()
        self.resize(280, 380)
        palette1 = QPalette()
        palette1.setColor(self.paintArea.backgroundRole(), QColor(255,255,255))   # 设置背景颜色
        self.setPalette(palette1)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.paintArea)
        self.mainLayout.addWidget(self.clearButton)
        self.mainLayout.addWidget(self.identifyButton)
        self.mainLayout.addLayout(self.resultLayout)
        self.mainLayout.addWidget(self.trainButton)
        #self.mainLayout.addWidget(self.resultLabel)
        self.setLayout(self.mainLayout)
        self.buildUpConnect()

    def buildUpConnect(self):
        self.clearButton.clicked.connect(self.clearArea)
        self.identifyButton.clicked.connect(self.identifyNumber)
        self.trainButton.clicked.connect(self.train)
        
    def clearArea(self):
        self.paintArea.pos_xy = []
        self.paintArea.update()
        self.resultLineText.clear()

    def identifyNumber(self):
        screen = QApplication.primaryScreen()
        savePix = screen.grabWindow(0, self.geometry().x(), self.geometry().y(), self.paintArea.width(), self.paintArea.height())
        #savePix = savePix.scaled(28, 28)
        fileName = 'sample.png'
        savePix.save(fileName, 'PNG')
        self.resultLineText.setText(str(net.predict('sample.png')))
        #print(net.predict('sample.png'))

    def train(self):
        reply = QMessageBox.question(self, 'Message', 'You sure to train?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            num = int(self.resultLineText.text())
            net.train('sample.png', num, 5.0)
            



if __name__ == '__main__':
    net = network.Network([784, 50, 10])
    net.loadModel()
    print ("OK")
    app = QApplication(sys.argv)        
    window = MainWindow()
    window.show()
    app.exec_()
        