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
from PyQt5.QtCore import QTime, QTimer, QCoreApplication, Qt
from PyQt5 import uic,QtGui
from PyQt5.QtWidgets import QApplication, QLCDNumber,QMainWindow, QVBoxLayout,\
    QWidget,QPushButton, QCheckBox, QLineEdit, QLabel, QHBoxLayout, QStatusBar,\
    QDialog,QMessageBox, QSizePolicy,QGridLayout

class DigitalClock(QMainWindow):

    # duration time in mins
    targetTime = 10
    counter = 0
    willblack = True


    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent, Qt.WindowStaysOnTopHint)
        self.central = QWidget(self)
        # self.setWindowTitle("SHAO PPT记时")

        self.setWindowFlags(Qt.CustomizeWindowHint|Qt.WindowCloseButtonHint)
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
                self.targetTime = float(self.line.text())
                # self.nameLabel.setText('Duration: ' + str(self.targetTime) + ' mins')
            except ValueError:
                self.line.clear()
                # self.nameLabel.setText('Duration: (mins)  1 ~ 100 mins!')
        else:
            self.targetTime = 10.0

        self.inicio = self.targetTime*60
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
            self.timer.stop()
            if self.willblack:
                self.blackscreen()

    def blackscreen(self):
        import sys

        if sys.platform.startswith('linux'):
            import os
            os.system("xset dpms force off")

        elif sys.platform.startswith('win'):

            self.dialog = QDialog()
            self.dialog.resize(1024,768)
            self.db = QPushButton("ok",self.dialog)
            # self.dialog.showFullScreen()

            self.dcentral = QWidget(self)
            self.dlayout = QVBoxLayout()
            self.dlabel = QLabel()
            self.dlabel.setAlignment(Qt.AlignCenter)
            self.dlabel.setText("汇报时间到")
            newfont = QtGui.QFont("SimSun", 120)
            self.dlabel.setFont(newfont)
            self.dlayout.addWidget(self.dlabel)
            self.dlayout.addWidget(self.db)
            self.dialog.setLayout(self.dlayout)
            # self.setCentralWidget(self.dcentral)
            self.dlabel.resize(400, 300)

            self.db.clicked.connect(self.closeit)
            self.dialog.setWindowFlags(Qt.WindowStaysOnTopHint)

            self.dialog.exec_()
            # import os
            # winpath = os.environ["windir"]
            # os.system(winpath + r'\system32\rundll32 user32.dll, LockWorkStation')

        elif sys.platform.startswith('darwin'):
            # import subprocess
            # subprocess.call('echo \'tell application "Finder" to sleep\' | osascript', shell=True)

            self.dialog = QDialog()
            self.dialog.resize(1024,768)
            self.db = QPushButton("ok",self.dialog)
            # self.dialog.showFullScreen()

            self.dcentral = QWidget(self)
            self.dlayout = QVBoxLayout()
            self.dlabel = QLabel()
            self.dlabel.setAlignment(Qt.AlignCenter)
            self.dlabel.setText("汇报时间到")
            newfont = QtGui.QFont("SimSun", 120)
            self.dlabel.setFont(newfont)
            self.dlayout.addWidget(self.dlabel)
            self.dlayout.addWidget(self.db)
            self.dialog.setLayout(self.dlayout)
            # self.setCentralWidget(self.dcentral)
            self.dlabel.resize(400, 300)

            self.db.clicked.connect(self.closeit)
            self.dialog.setWindowFlags(Qt.WindowStaysOnTopHint)

            self.dialog.exec_()

            # dialog.showFullScreen()
   # msg.setIcon(QMessageBox.Information)

            # msg = QMessageBox(Qt.WindowStaysOnTopHint)
            # msg.setText("汇报结束")
            # msg.setStandardButtons(QMessageBox.Ok)
            # msg.exec_()
            # msg.buttonClicked.connect(msgbtn)

    def closeit(self):
        self.dialog.close()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    clock = DigitalClock()
    clock.show()
    sys.exit(app.exec_())
