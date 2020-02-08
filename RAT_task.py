#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
author: Elijah Xu
"""

import sys

import xlrd
import xlwt
import random
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
import sys

##init
msgOne = "If you are ready, please enter “space” key to go on"
fresh_time = 4
# 构造一个 80 的乱序列
list = []
for i in range(80):
    list.append(i)
random.shuffle(list)

workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('test')
workbook.save('answer.xls')

#构造列乱序
dict_List = {}
print_List = []
filename = "answer.xlsx"
## init end

class Example(QWidget):

    Flag = -1 #标示当前处在哪个界面 2:提示界面，3:展示字母界面，4:回答界面
    time_Flag = -1 #初始化
    loopCounter = 40
    current_list = []

    def __init__(self):
        super().__init__()
        self.textBoxEdit = QLineEdit()
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(self.textBoxEdit, 1, 0)
        self.setLayout(self.grid)
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('TEST')
        self.timer = QTimer()
        self.timer.timeout.connect(self.ReStart)
        self.Flag = 1
        self.show()

    def ReStart(self):
        print("restart")
        self.textBoxEdit.hide()
        self.loopCounter = self.loopCounter - 1
        str_TextBox = "Trial" + str(40 - self.loopCounter + 1) + ": " + msgOne
        self.msgOne.hide()
        self.msgOne = QLabel(str_TextBox)
        self.msgOne.show()
        self.Flag = 2
        self.grid.addWidget(self.msgOne, 0, 0)

    def startTimer(self):
        self.timer.start(45000) # 5000 单位是毫秒， 即 5 秒
        print("start timer")
    
    def endTimer(self):   
        self.timer.stop()

    def keyPressEvent(self, event):
        #这里event.key（）显示的是按键的编码
        print("按下：" + str(event.key()))
        if (event.key() == Qt.Key_Enter - 1):  #这里换成回车
            if self.Flag != 1:
                return

            if self.time_Flag == -1:
                self.startTimer()
                print("start")
                self.time_Flag = 1
            
            self.textBoxEdit.hide()
            str_TextBox = "Trial" + str(40 - self.loopCounter + 1) + ": " + msgOne
            self.msgOne = QLabel(str_TextBox)
            self.Flag = 2
            self.grid.addWidget(self.msgOne, 0, 0)
            
        if (event.key() == 16777250):  #这里换成回车
            #这里event.key（）显示的是按键的编码
            print("按下：Ctrl")
            if self.Flag < 1:
                return

            if self.Flag == 1:
                self.textBoxEdit.hide()
                self.msgOne.hide()
                str_TextBox = "Trial" + str(40 - self.loopCounter + 1) + ": " + msgOne
                self.msgOne = QLabel(str_TextBox)
                self.msgOne.show()
                self.Flag = 2
                self.grid.addWidget(self.msgOne, 0, 0)
            elif self.Flag == 2:
                self.current_list = print_List[40 - self.loopCounter]
                str_TextBox = ""
                for i in range(len(self.current_list)):
                    str_TextBox = str_TextBox +self.current_list[i]  
                self.msgOne.hide()
                self.msgOne = QLabel(str_TextBox)
                self.msgOne.show()
                self.Flag = 3
                self.grid.addWidget(self.msgOne, 0, 0)
            elif self.Flag == 3:
                self.textBoxEdit.setText("")
                self.textBoxEdit.show()
                self.msgOne.hide()
                self.msgOne = QLabel("please write your answer，and then enter ”space” key to the next tral.")
                self.msgOne.show()
                self.Flag = 4
                self.grid.addWidget(self.msgOne, 0, 0)
                self.grid.addWidget(self.textBoxEdit, 1, 0, 1, 1)
                self.loopCounter = self.loopCounter - 1
            elif self.Flag == 4:
                answer = self.textBoxEdit.text()
                check_Answer(answer, self.current_list, 40 - self.loopCounter - 1)
                self.textBoxEdit.hide()
                self.msgOne.hide()
                str_TextBox = "Trial" + str(40 - self.loopCounter + 1) + ": " + msgOne
                self.msgOne = QLabel(str_TextBox)
                self.msgOne.show()
                self.Flag = 2
                self.grid.addWidget(self.msgOne, 0, 0)

def readExcel():
    wb = xlrd.open_workbook("RAT_Task.xlsx") #打开文件
    sheet1 = wb.sheet_by_index(0)
    nrows = sheet1.nrows
    ncols = sheet1.ncols
    print(nrows)
    print(ncols)
    row_value_old = []
    row_value_new = []

    for i in range(nrows):
        if i != 0:
            row = sheet1.row_values(i)
            row_value_old.append(row)
        else:
            row = sheet1.row_values(i)
    
    for i in range(len(row_value_old)):
        row = row_value_old[list[i]]
        row_value_new.append(row)

    for i in range(len(row_value_new)):
        row = row_value_new[i]
        row_new = row[1:4]
        random.shuffle(row_new)
        print_List.append(row_new)
        dict_List[row[len(row)-1]] = row_new
    
def check_Answer(answer, ori_list, line):
    right_answer = "False"

    for key,value in dict_List.items():
        if key == answer:
            right_answer = "True"
            break
    
    worksheet.write(line, 0, answer)
    worksheet.write(line, 1, ori_list)
    worksheet.write(line, 2, right_answer)
    workbook.save('answer.xls')



    
if __name__ == '__main__':
    readExcel()
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())





