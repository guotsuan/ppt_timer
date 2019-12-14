#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 gq <gq@Quans-iMac-Pro>
#
# Distributed under terms of the MIT license.

"""

"""
import sys
from PyQt5.QtCore import QTimer, QCoreApplication, Qt
from PyQt5 import uic,QtGui
from PyQt5.QtWidgets import QApplication, QLCDNumber,QMainWindow, QVBoxLayout,\
    QWidget,QPushButton, QCheckBox, QLineEdit, QLabel, QHBoxLayout, QStatusBar,\
    QDialog,QMessageBox, QSizePolicy,QGridLayout

class DigitalClock(QMainWindow):

    # duration time in mins
    targetTime = 10
    answerTime = 5
    counter = 0
    willblack = True
    p = 'report'


    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent, Qt.WindowStaysOnTopHint)
        self.central = QWidget(self)
        # self.setWindowTitle("SHAO PPT记时")

        self.setWindowFlags(Qt.CustomizeWindowHint|Qt.WindowCloseButtonHint|Qt.WindowStaysOnTopHint)
        # initial timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.inicio = self.targetTime*60

        # LCDwidget
        self.lcd = QLCDNumber()
        self.lcd.setSegmentStyle(QLCDNumber.Filled)
        self.lcd.setMinimumHeight(40)

        # Black screen checkbox
        # self.cb = QCheckBox('Black Screen')
        # self.cb.toggle()
        # self.cb.stateChanged.connect(self.blackornot)

        # Duration setup
        self.line = QLineEdit()
        self.line.setMaximumWidth(30)
        self.line.setContentsMargins(0,0,0,0)
        self.setbutton = QPushButton('K', self)
        self.setbutton.setMaximumWidth(20)
        self.setbutton.clicked.connect(self.setTimer)

        # Label widget
        # self.nameLabel = QLabel()
        # self.nameLabel.setText('Duration: ' + str(self.targetTime) + ' mins')
        # self.nameLabel.resize(60, 20)


        # start and reset button
        self.start_button = QPushButton("S")
        self.start_button.resize(30,20)
        self.start_button.setMaximumWidth(20)
        self.stop_button = QPushButton("R")
        self.stop_button.setMaximumWidth(20)
        self.start_button.clicked.connect(self.restartTimer)
        self.stop_button.clicked.connect(self.stopTimer)

        # layout setup
        self.vbox = QVBoxLayout(self.central)
        # self.vbox = QVBoxLayout(self.center)
        self.vbox.setContentsMargins(0,0,0,0)
        self.vbox.addStretch(0)
        self.hbox1 = QGridLayout()
        self.hbox1.setContentsMargins(0,0,0,0)
        self.vbox.addWidget(self.lcd)
        self.vbox.addLayout(self.hbox1)
        self.hbox1.addWidget(self.start_button, 0, 0)
        self.hbox1.addWidget(self.stop_button, 0,1)
        self.hbox1.addWidget(self.line, 0,2)
        self.hbox1.addWidget(self.setbutton, 0,3)
        # self.vbox.addWidget(self.nameLabel)
        self.setCentralWidget(self.central)

        self.setMaximumWidth(120)
        self.setContentsMargins(0,0,0,0)
        # self.setGeometry(0,0,100,80)
        self.setMinimumWidth(120)
        # initial clock display
        self.updateLCD()

    def updateLCD(self):
        diffStr = "%d:%02d" % (self.inicio//60, self.inicio % 60)
        self.lcd.setDigitCount(len(diffStr))
        self.lcd.display(diffStr)


    def setTimer(self):
        if self.line.text():
            try:
                self.targetTime = float(self.line.text().split(",")[0])
                self.answerTime = float(self.line.text().split(",")[1])
                # self.nameLabel.setText('Duration: ' + str(self.targetTime) + ' mins')
            except ValueError:
                self.line.clear()
                # self.nameLabel.setText('Duration: (mins)  1 ~ 100 mins!')
        else:
            self.targetTime = 10.0

        self.inicio = self.targetTime*60
        self.p = 'report'
        self.updateLCD()
        self.start_button.setText('S')
        self.counter = 0
        self.timer.stop()

    def blackornot(self, state):
        if state == Qt.Checked:
            self.willblack=True
        else:
            self.willblack=False

    def restartTimer(self):
        # Reset the timer and the lcd
        self.p = 'report'
        if self.counter == 0:
            self.timer.start(1000)
            self.start_button.setText('P')
            self.counter += 1
        else:
            self.timer.stop()
            self.start_button.setText('C')
            self.counter -= 1

    def stopTimer(self):
        self.timer.stop()
        self.inicio = self.targetTime*60
        self.updateLCD()
        self.start_button.setText('S')
        self.counter = 0

    def showTime(self):
        self.inicio -= 1
        self.updateLCD()

        if self.inicio == 0:
            self.stopTimer()
            self.timer.stop()
            self.start_button.setText('S')
            self.counter = 0
            if self.willblack:
                self.blackscreen()

    def blackscreen(self):

        self.dialog = QDialog()
        self.dialog.resize(1024,768)

        self.dcentral = QWidget(self)
        self.dlayout = QVBoxLayout()
        self.dlabel = QLabel()
        self.dlabel.setAlignment(Qt.AlignCenter)
        if self.p == 'report':
            self.db = QPushButton("按此进入答辩环节 (5秒后自动进入)",self.dialog)
            self.db.setStyleSheet('QPushButton {color: black;}')
            self.dlabel.setText("汇报时间到")
            self.puttontime = 5
            self.btimer = QTimer(self)
            self.btimer.timeout.connect(self.countdown)
            self.btimer.start(1000)
        else:
            self.dlabel.setText("答辩时间到")
            self.db = QPushButton("5秒后自动结束",self.dialog)
            self.db.setStyleSheet('QPushButton {color: black;}')
            self.puttontime = 5
            self.btimer = QTimer(self)
            self.btimer.timeout.connect(self.countdown)
            self.btimer.start(1000)
        newfont = QtGui.QFont("SimSun", 120)
        bfont = QtGui.QFont("Hei", 45)
        self.db.setFont(bfont)
        self.dlabel.setFont(newfont)
        self.dlayout.addWidget(self.dlabel)
        self.dlayout.addWidget(self.db)
        self.dialog.setLayout(self.dlayout)
        self.db.setMaximumHeight(120)
        # self.setCentralWidget(self.dcentral)
        self.dlabel.resize(400, 300)

        self.db.clicked.connect(self.closeit)
        self.dialog.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.dialog.exec_()

    def countdown(self):
        self.puttontime -=1
        if self.p == 'report':
            self.db.setText("按此确认进入答辩环节 (" + str(self.puttontime) +
                            "秒后自动进入)")
        else:
            self.db.setText(str(self.puttontime) + "秒后自动结束")

        self.updateLCD()

        if self.puttontime == 0:
            self.btimer.stop()
            self.closeit()


    def closeit(self):
        self.dialog.close()
        if self.p == 'report':
            self.inicio = self.answerTime*60
            self.timer.start(1000)
            self.p = 'answer'
        else:
            self.inicio = self.targetTime*60
            self.timer.stop()
            self.p = 'report'
        self.updateLCD()
        self.start_button.setText('S')
        self.counter = 0


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    clock = DigitalClock()
    clock.show()
    sys.exit(app.exec_())
