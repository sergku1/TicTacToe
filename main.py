#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import hashlib
import shutil
from PyQt5.QtWidgets import QApplication, QWidge
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import smtplib
# Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
import keyboard
from pdf2image import convert_from_path
import gui_tictactoe

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
                        xdate1.append(mirvector)  # Считаем
                        points[str(ival + ik) + "-" + str(jval + jm)] = xdate1  # И заносим в T1
                    lines_scan(xdat, ival, jval, vector)  # scan for lines
                else:
                    points[str(ival) + '-' + str(jval)] = xdat  # Если в ячейке T1 нету соответствующего T0
            except KeyError:
                pass
        i += 1
    return points


def lines_scan(xda, ivalu, jvalu, vecto):
    print('lines_scan')
    ikl, jml = numb(vecto)
    i1 = vecto
    if i1 > 4:
        rr1 = -4
    else:
        rr1 = 4
    mirvector1 = i1 + rr1  # считаем вектор в противоположном напаравлении
    xval = xda[0]
    if xval == 'X':
        kiter = -1
        while mirvector1 in points[str(ivalu - kiter*ikl) + "-" + str(jvalu - kiter*jml)]:# and (ivalu - kiter*ikl > 0) and (ivalu - kiter*ikl < sq) and (jvalu - kiter*jml > 0) and (jvalu - kiter*jml < sq):  # Проверяем, есть ли vector в точке T+1 по линии, соседней + проверка выхода за границу
            lineX[str(ivalu - kiter*ikl) + '-' + str(jvalu - kiter*jml) + '-' + str(vecto)] = xval  # Заносим точку T+1 с mirvector в lineX
            lineX[str(ivalu) + '-' + str(jvalu) + '-' + str(vecto)] = xval  #
            if len(lineX) >= int(lintowin):
                print(f'Win X! line = {len(lineX)} XXXXXXXXXXXXXXXXXXXXXXXXXXXx')
            kiter += 1
    elif xval == '0':
        kiter1 = -1
        while mirvector1 in points[str(ivalu - kiter1*ikl) + "-" + str(jvalu - kiter1*jml)] and (ivalu - kiter1*ikl > 0) and (ivalu - kiter1*ikl < sq) and (jvalu - kiter1*jml > 0) and ( jvalu - kiter1*jml < sq):  # Проверяем, есть ли vector в точке T+1 по линии, соседней с проверкой выхода за границу
            line0[str(ivalu - kiter1*ikl) + '-' + str(jvalu - kiter1*jml) + '-' + str(vecto)] = xval  # Заносим точку T+1 с mirvector в lineX
            line0[str(ivalu) + '-' + str(jvalu) + '-' + str(vecto)] = xval  #
            if len(line0) >= int(lintowin):
                print(f'Win 0! line = {len(line0)} 0000000000000000000')
            kiter1 += 1

    return lineX, line0


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
        QtCore.QTimer.singleShot(0, self.pushButton_6.setFocus)
        app = QApplication(sys.argv)
        window = QWidget()
        window.show()
        self.pixmap = QPixmap(img_file_full)  #
        self.label_95.setPixmap(self.pixmap)

    print('Start Game TikTakToe multicell variant')
    lintowin = input('input cell in line to win ')  # how cell to win
    points = {}  # dictionary i, j they have vector for each point
    lineX = {}  # dictionary kur kaupem sujungtas taskus su X
    line0 = {}  # dictionary kur kaupem sujungtas taskus su 0
    lineSX = {}  # dictionary kur kaupem sujungtas linijos su X
    lineS0 = {}  # dictionary kur kaupem sujungtas linijos su 0
    #  Понятие vector направление соседства одноименной ячейки. подобно направлениям стрелок на механических часах
    #  1 с лева, 2 - с лева - вверх, 3 - вверх, 4 - вверх - вправо
    # Taip jeigu paspaustas X or 0 pasirinktam langeleje




    sq = int(input('input X size of playng deck X x X = '))
    ttt = 1
    while True:
        if ttt % 2 != 0:
            print('You play X')
            #  global xvalue
            xvalue = 'X'
        else:
            print('You play 0')
            #  global xvalue
            xvalue = '0'
        xdate = ['']
        play = input('please input Your step in format i-j = ')
        ivalue = int(play.split('-')[0])  # Counter i, axis X
        jvalue = int(play.split('-')[1])  # Counter j, axis Y
        xdate[0] = xvalue
        # points[str(ivalue) + '-' + str(jvalue)] = xdate  # insert X or 0 in point with coordinates i,j
        points_scan(xdate, ivalue, jvalue)
        print(points)
        print(f'lineX = {lineX}')
        print(f'line0 = {line0}')
        ttt += 1


if __name__ == "__main__":
    #   import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
