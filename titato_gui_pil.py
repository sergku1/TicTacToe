#!/usr/bin/python3
# -*- coding: utf-8 -*-
# TicTacToe with simplif structure and GUI on PyQt
import os
import sys
from typing import Any
import cv2
import numpy as np
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLineEdit
from keyboard import add_hotkey
import gui_tictactoe
from PIL import Image
points = {}
lineX = {}
line0 = {}


def points_scan(xdat, ival, jval):
    points[str(ival) + '-' + str(jval)] = xdat
    i = 1
    while i <= 8:
        ik, jm = numb(i)
        if (ival + ik > 0) and (ival + ik < sq) and (jval + jm > 0) and (jval + jm < sq):  # Не выйдет ли за границы игрового поля при поиске вектора
            try:
                if xdat[0] in points[str(ival + ik) + "-" + str(jval + jm)][0]:  # Если в соседней ячейке по вектору i есть такой же знак X или 0
                    vector = i  # Направления вектора : 1 - лево, 2 - лево-вверх, 3 - вверх, 4 - право - вверх.. до 8
                    if i > 4:
                        rr = -4
                    else:
                        rr = 4
                    mirvector = i + rr  # считаем вектор в противоположном напаравлении
                    xdat.append(i)  # Заносим в  xdate
                    points[str(ival) + '-' + str(jval)] = xdat  # added vector to xdate in point T(i,j)
                    if mirvector in points[str(ival + ik) + "-" + str(jval + jm)]:  # Проверяем наличие обратного вектора в точке T1
                        continue
                    else:  # Нет обратного вектора т к точка стояла отдельно
                        xdate1 = points[str(ival + ik) + "-" + str(jval + jm)]
                        xdate1.append(mirvector)  # Добавляем второй, обратный вектор
                        points[str(ival + ik) + "-" + str(jval + jm)] = xdate1  # И заносим в T1
                    ikl, jml = numb(vector)
                    i1 = vector
                    if i1 > 4:
                        rr1 = -4
                    else:
                        rr1 = 4
                    mirvector1 = i1 + rr1  # считаем вектор в противоположном напаравлении
                    xval = xdat[0]
                    if xval == 'X':  #
                        kiter = -1
                        while vector in points[str(ival - kiter * ikl) + "-" + str(
                                jval - kiter * jml)]:  # Проверяем, есть ли vector в точке T+1 по линии, соседней + проверка выхода за границу
                            lineX[str(ival - kiter * ikl) + '-' + str(jval - kiter * jml) + '-' + str(
                                vector)] = xval  # Заносим точку T+1 с mirvector в lineX
                            lineX[str(ival) + '-' + str(jval) + '-' + str(vector)] = xval  #
                            if len(lineX) >= int(lintowin):
                                print(f'Win X! line = {len(lineX)} XXXXXXXXXXXXXXXXXXXXXXXXXXXx')
                            kiter += 1
                        lineX[str(ival + ikl) + '-' + str(jval + jml) + '-' + str(mirvector1)] = xval  # Заносим точку T с mirvector
                    elif xval == '0':
                        kiter1 = -1
                        while vector in points[str(ival - kiter1 * ikl) + "-" + str(jval - kiter1 * jml)]: #and (ival - kiter1 * ikl > 0) and (ival - kiter1 * ikl < sq) and (jval - kiter1 * jml > 0) and (jval - kiter1 * jml < sq):  # Проверяем, есть ли vector в точке T+1 по линии, соседней с проверкой выхода за границу
                            line0[str(ival - kiter1 * ikl) + '-' + str(jval - kiter1 * jml) + '-' + str(
                                vector)] = xval  # Заносим точку T+1 с mirvector в lineX
                            line0[str(ival) + '-' + str(jval) + '-' + str(vector)] = xval  #
                            if len(line0) >= int(lintowin):
                                print(f'Win 0! line = {len(line0)} 0000000000000000000')
                            kiter1 += 1
                        line0[str(ival + ikl) + '-' + str(jval + jml) + '-' + str(mirvector1)] = xval  # Заносим точку T с mirvector
                else:
                    points[str(ival) + '-' + str(jval)] = xdat  # Если в ячейке T1 нету соответствующего T0
            except KeyError:
                pass
        i += 1
        print(f'points = {points}')
        print(f'lineX = {lineX}')
        print(f'line0 = {line0}')
    return points, lineX, line0


def numb(chi):
    k, m = 0, 0
    match chi:
        case 1:
            k, m = -1, 0
        case 2:
            k, m = -1, 1
        case 3:
            k, m = 0, 1
        case 4:
            k, m = 1, 1
        case 5:
            k, m = 1, 0
        case 6:
            k, m = 1, -1
        case 7:
            k, m = 0, -1
        case 8:
            k, m = -1, -1
    return k, m


class MyWindow(QtWidgets.QMainWindow, gui_tictactoe.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.centralSpinPoint = None
        self.setupUi(self)  #
        self.wEv = 0  # mouse wheel spin counter
        #  add_hotkey('alt + x', QtWidgets.qApp.quit)  # hot buttons, must be root for use this functional
        self.pushButton.clicked.connect(QtWidgets.qApp.quit)  # Logout button event
        self.pushButton_2.clicked.connect(self.clear_all)  # L
        self.spinBox.setValue(3)
        self.spinBox_2.setValue(3)
        new_im = Image.open('blanc.png')
        new_im.save('blanc_new.png')
        self.pixmap = QPixmap('blanc_new.png')  # image setup and output
        self.label.setPixmap(self.pixmap)
        self.pixmap = QPixmap('tictaktoeX.png')  # image setup and output
        self.label_4.setPixmap(self.pixmap)
        self.label_6.setText('You play X')
        sq = self.spinBox.value()
        self.lineEdit.setFocus()
        self.lineEdit.returnPressed.connect(self.click_method)  #
        #



    def clear_all(self):
        self.spinBox.setValue(3)
        self.spinBox_2.setValue(3)
        self.lineEdit.setText('')
        self.lineEdit.setFocus()
        points = {}
        new_im = Image.open('blanc.png')
        new_im.save('blanc_new.png')
        self.pixmap = QPixmap('blanc_new.png')  # image setup and output
        self.label.setPixmap(self.pixmap)
        self.label_7.setText(str(points))
        self.label_6.setText('')
        return

    def pagalve(self, points):
        po_list = list(points.items())
        i = 0
        while i < len(po_list):
            mazas = int(30)
            if (po_list)[i][1][0] == 'X':
                smal = Image.open('tictaktoeX.png')
            else :
                smal = Image.open('tictaktoe0.png')
            new_im = Image.open('blanc_new.png')
            iv = int(list(po_list)[i][0].split('-')[0])
            jv = int(list(po_list)[i][0].split('-')[1])
            put_in_place = ((iv-1)*mazas, (jv-1)*mazas, iv*mazas, jv*mazas)
            new_im.paste(smal, put_in_place)
            new_im.save('blanc_new.png')
            self.pixmap = QPixmap('blanc_new.png')  # image setup and output
            self.label.setPixmap(self.pixmap)
            i+=1
        return

    def click_method(self):
        xvalue = self.label_6.text().split()[2]
        xdate = ['']
        if xvalue == 'X':
            self.label_6.setText('You play X')
        else:
            self.label_6.setText('You play 0')
        xdate[0] = xvalue
        play = self.lineEdit.text()
        play1 = play.split('-')
        ivalue = int(play1[0])  # Counter i, axis X
        jvalue = int(play1[1])  # Counter j, axis Y
        global sq
        sq = self.spinBox.value()
        global lintowin
        lintowin = self.spinBox_2.value()
        self.lineEdit.setText('')
        points_scan(xdate, ivalue, jvalue)
        if len(lineX) == aq:
            self.label_4.setText('X Win!!!!')
        elif len(line0) == aq:
            self.label_4.setText('X Win!!!!')
        self.pagalve(points)
        self.label_7.setText(str(points))
        if xvalue == 'X':
            self.pixmap = QPixmap('tictaktoe0.png')  # image setup and output
            self.label_4.setPixmap(self.pixmap)
            self.label_6.setText('You play 0')
        else:
            self.pixmap = QPixmap('tictaktoeX.png')  # image setup and output
            self.label_4.setPixmap(self.pixmap)
            self.label_6.setText('You play X')
        return points


if __name__ == "__main__":
    #   import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

