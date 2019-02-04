 # -*- coding: utf-8 -*-

# Author: Christian Winkler
# Date: 04-02-2019

import numpy as np
import pandas as pd
#from shutil import copyfile


from PyQt4 import QtCore, QtGui
#from PyQt4.QtCore import QProcess
from PyQt4.QtCore import *
from PyQt4.QtGui import *
 
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

import sys
import os


 
class refcurv_simvascular(QWidget):
    def __init__(self, parent=None):
        super(refcurv_simvascular, self).__init__() 
        
        self.setWindowTitle("RefCurv for SimVascular")
        self.setWindowIcon(QIcon('refcurv_logo.png'))
    
        pal=QtGui.QPalette()
        role = QtGui.QPalette.Background
        pal.setColor(role, QtGui.QColor(255, 255, 255))
        self.setPalette(pal)
       
        #self.textEdit = QtGui.QLabel('None')

        self.loadPercButton = QtGui.QPushButton("Load Reference curves")
        self.loadPercButton.clicked.connect(self.loadRef)

         
        self.fileName = ''
        self.lastClicked = []
        self.number_plots = 0     
        self.chosen_point = 0

        

        self.figure_perc = Figure()
        self.pw_perc = FigureCanvas(self.figure_perc)
        self.nav = NavigationToolbar(self.pw_perc, self.pw_perc, coordinates=False)
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.pw_perc)
        layout.addWidget(self.loadPercButton)
        
        
        #self.center_window()
        

        
    def center_window(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        


    def pw_perc_click(self, event):
        self.ax_perc.clear()
        self.pw_perc.draw()
        
        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', event.button,
               event.x, event.y, event.xdata, event.ydata))
        #self.ax_perc.set_xlim([0, 100])
        #self.ax_perc.set_ylim([0, 50])
        self.ax_perc.plot(event.xdata, event.ydata,  color="r", marker="o", markersize = 5) 
        
        self.ax_perc.plot(self.lms_chart["x"].values, self.lms_chart["C3"].values, "k")
        self.ax_perc.plot(self.lms_chart["x"].values, self.lms_chart["C10"].values, "k" )
        self.ax_perc.plot(self.lms_chart["x"].values, self.lms_chart["C25"].values, "k" )
        self.ax_perc.plot(self.lms_chart["x"].values, self.lms_chart["C50"].values, "k" )
        self.ax_perc.plot(self.lms_chart["x"].values, self.lms_chart["C75"].values, "k" )
        self.ax_perc.plot(self.lms_chart["x"].values, self.lms_chart["C90"].values, "k" )
        self.ax_perc.plot(self.lms_chart["x"].values, self.lms_chart["C97"].values, "k" )
        
        self.ax_perc.set_xlim([0, self.lms_chart["x"].values[-1]* 1.2])
        self.ax_perc.set_ylim([0, self.lms_chart["C97"].values[-1] * 1.2]) 

        self.ax_perc.grid()
           
        self.pw_perc.draw()
        
        self.chosen_point = round(event.ydata, 2)
    
    def loadRef(self):
        self.filename = QtGui.QFileDialog.getOpenFileName(self,'Open File', ' ','*.csv')
        if self.filename:
            try:
                self.lms_chart = pd.read_csv(self.filename,sep =',', encoding = "ISO-8859-1")
                
                self.ax_perc = self.figure_perc.add_subplot(111)
                self.ax_perc.clear()
                
                self.ax_perc.plot(self.lms_chart["x"].values, self.lms_chart["C3"].values, "k")
                self.ax_perc.plot(self.lms_chart["x"].values, self.lms_chart["C10"].values, "k" )
                self.ax_perc.plot(self.lms_chart["x"].values, self.lms_chart["C25"].values, "k" )
                self.ax_perc.plot(self.lms_chart["x"].values, self.lms_chart["C50"].values, "k" )
                self.ax_perc.plot(self.lms_chart["x"].values, self.lms_chart["C75"].values, "k" )
                self.ax_perc.plot(self.lms_chart["x"].values, self.lms_chart["C90"].values, "k" )
                self.ax_perc.plot(self.lms_chart["x"].values, self.lms_chart["C97"].values, "k" )
                
                self.ax_perc.set_xlim([0, self.lms_chart["x"].values[-1]* 1.2])
                self.ax_perc.set_ylim([0, self.lms_chart["C97"].values[-1] * 1.2])
                
                self.ax_perc.grid()
                
                self.pw_perc.draw()

            except:
                print("reading error")

            print(self.filename) 
            self.figure_perc.canvas.mpl_connect('button_press_event', self.pw_perc_click)
            
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = refcurv_simvascular()
    main.show()
    sys.exit(app.exec_())
    


        

        