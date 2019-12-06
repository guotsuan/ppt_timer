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
from PyQt5.QtCore import QTime, QTimer, Qt
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLCDNumber,QMainWindow, QVBoxLayout,\
    QWidget,QPushButton, QCheckBox, QLineEdit, QLabel, QHBoxLayout, QStatusBar

class DigitalClock(QMainWindow):

    # duration time in mins
    targetTime = 10
    counter = 0
    willblack = True


    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent, Qt.WindowStaysOnTopHint)
        self.central = QWidget(self)
        self.setWindowTitle("上海天文台PPT记时")

        # initial timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.inicio = self.targetTime*60

        # LCDwidget
        self.lcd = QLCDNumber()
        self.lcd.setSegmentStyle(QLCDNumber.Filled)
        self.lcd.setMinimumHeight(100)

        # Black screen checkbox
        self.cb = QCheckBox('Black Screen')
        self.cb.toggle()
        self.cb.stateChanged.connect(self.blackornot)

        # Duration setup
        self.line = QLineEdit()
        self.setbutton = QPushButton('Set', self)
        self.setbutton.clicked.connect(self.setTimer)

        # Label widget
        self.nameLabel = QLabel()
        self.nameLabel.setText('Duration: ' + str(self.targetTime) + ' mins')
        self.nameLabel.resize(120, 40)


        # start and reset button
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Reset")
        self.start_button.clicked.connect(self.restartTimer)
        self.stop_button.clicked.connect(self.stopTimer)

        # layout setup
        self.vbox = QVBoxLayout(self.central)
        self.hbox = QHBoxLayout()
        self.vbox.addWidget(self.cb)
        self.vbox.addWidget(self.lcd)
        self.vbox.addWidget(self.start_button)
        self.vbox.addWidget(self.stop_button)
        self.vbox.addLayout(self.hbox)
        self.hbox.addWidget(self.line)
        self.hbox.addWidget(self.setbutton)
        self.vbox.addWidget(self.nameLabel)
        self.setCentralWidget(self.central)

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
                self.nameLabel.setText('Duration: ' + str(self.targetTime) + ' mins')
            except ValueError:
                self.line.clear()
                self.nameLabel.setText('Duration: (mins)  1 ~ 100 mins!')
        else:
            self.targetTime = 10.0

        self.inicio = self.targetTime*60
        self.updateLCD()
        self.start_button.setText('Start')
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
            self.start_button.setText('Pause')
            self.counter += 1
        else:
            self.timer.stop()
            self.start_button.setText('Continue')
            self.counter -= 1

    def stopTimer(self):
        self.timer.stop()
        self.inicio = self.targetTime*60
        self.updateLCD()
        self.start_button.setText('Start')
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
            import os
            winpath = os.environ["windir"]
            os.system(winpath + r'\system32\rundll32 user32.dll, LockWorkStation')

        elif sys.platform.startswith('darwin'):
            import subprocess
            subprocess.call('echo \'tell application "Finder" to sleep\' | osascript', shell=True)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    clock = DigitalClock()
    clock.show()
    sys.exit(app.exec_())
