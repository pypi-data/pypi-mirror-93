'''
Created on Feb 15, 2019

@author: Bartosz Lew <bartosz.lew@umk.pl>
'''
import pkg_resources

import PyQt5.QtWidgets
from PyQt5 import QtWidgets 
from PyQt5 import QtCore, QtGui,uic
from PyQt5.QtCore import pyqtSignal,pyqtSlot, QSettings
import os,sys
import numpy as np
import scipy.io.wavfile as wf

from acomod import global_settings
from acomod import resources
from acomod import recordSignal
from acomod import preferences
from acomod import matplotlibWidget

class MainWindow(QtWidgets.QMainWindow):
    newSoundFileSelected = QtCore.pyqtSignal(str)
    
#     newSampleSignal = QtCore.pyqtSignal(list,list)

    def __init__(self,parent=None):
        super(MainWindow, self).__init__()
#         try:
#             self.ui=uic.loadUi('MainWindow.ui', self)
#         except:
        self.ui=uic.loadUi(pkg_resources.resource_filename('acomod','MainWindow.ui'), self)
            
#         self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
#         self.ui=Ui_MainWindow()
#         self.ui.setupUi(self)
#         self.ui.pushButton.clicked.disconnect()
#         self.ui.pushButton.clicked.connect(self.on_pushButton_clicked)

        self.settings=global_settings.mySettings(self)



        '''
        
        SETTING WIDGETS
        
        '''


        self.matplotlibWidget=matplotlibWidget.MatplotlibWidget(Npeaks=self.settings.value('Npeaks',1,type=int),
                                                                parent=self)
        self.ui.gridLayout.addWidget(self.matplotlibWidget,0,0)
#         self.ui.gridLayout.addWidget(QPushButton("1"),0,0)

#         self.matplotlibWidget.canvas.draw()
#         print(self.ui.doubleSpinBox_sampling.value())

        
        '''
        SETTINGS GUI STUFF
        '''
        
        

        self.ui.actionLogarithmic_scale_X.setChecked(self.settings.value('Logarithmic_scale_X',False,type=bool))
        self.ui.actionLogarithmic_scale_Y.setChecked(self.settings.value('Logarithmic_scale_Y',False,type=bool))
        self.ui.actionPlotAverage.setChecked(self.settings.value('PlotAverage',False,type=bool))
        self.ui.actionPlotMaximalValues.setChecked(self.settings.value('PlotMaximalValues',False,type=bool))
        self.ui.spinBox_Npeaks.setValue(self.settings.value('Npeaks',1,type=int))
        self.ui.doubleSpinBox_recordingLength.setValue(self.settings.value('recordingLength',1,type=float))

        self.sampling_freq=self.settings.value("sampling",44100, type=float)
        self.soundSpeed=self.settings.value("soundSpeed",343.0,type=float)
        self.recordingLength=self.settings.value("recordingLength",1.0,type=float)

        self.resize(self.settings.value("size", QtCore.QSize(840, 700)))
        self.move(self.settings.value("pos", QtCore.QPoint(50, 50)))


        '''
        
        CONNECTIONS
        
        '''
#         self.ui.
#         self.ui.actionLogarithmic_scale_X.toggled[bool].connect(self.on_actionLogarithmic_scale_X_toggled)
#         self.ui.actionLogarithmic_scale_Y.toggled[bool].connect(self.on_actionLogarithmic_scale_Y_toggled)
#         self.ui.actionPlotAverage.toggled[bool].connect(self.on_actionPlotAverage_toggled)
#         self.ui.actionPlotMaximalValues.toggled[bool].connect(self.on_actionPlotMaximalValues_toggled)
        self.ui.spinBox_Npeaks.valueChanged[int].connect(self.on_NpeaksValueChanged)

#         self.ui.actionPlay.toggled[bool].connect(self.on_actionPlay_toggled)

        '''
        
        STATUS BAR INFO
        
        '''
        self.statusBar = PyQt5.QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)
#         self.statusBar.showMessage("Ready",2000)
        self.statusBar.showMessage("Ready")

        
#         self.ui.frame.setStyleSheet("background-color: rgb(200, 255, 255)")

#         plotWidget=MatplotlibWidget()
#         self.ui.frame.layoutVertical.addWidget(self.)
#         self.layoutVertical = QtGui.QVBoxLayout(self)



        '''
        
        Sources of sound
        
        '''
        self.soundFileName=None

#         self.show()
        
        
        '''
        
        Internal data
        
        '''
        self.recorded_data={'samples' : []}
        
    '''
    
    
    Slots and methods
    
    
    '''
        

    @QtCore.pyqtSlot()
    def show_statusBarMsg(self,msg,timeout=2000):
        print(msg)
        self.statusBar.showMessage(msg,timeout)


            
    def on_NpeaksValueChanged(self,n):
        settings=global_settings.mySettings(self)
        settings.setValue("Npeaks",n)
#         self.matplotlibWidget.selectMaxima(n)
#         self.matplotlibWidget.plotMaxima()
#         self.matplotlibWidget.draw()
        self.matplotlibWidget.mkplot()


    def cleanUp(self):
        if self.ui.actionRecord.isChecked():
            print("Disconnecting thread")
            self.dataTh.newSamplePowerSignal.disconnect()
            msg="Waiting for data thread to finish...please wait"
            print(msg)
            self.show_statusBarMsg(msg=msg,timeout=0)
#             self.dataTh.exit()
            event=QtCore.QEventLoop(self)
            self.dataTh.finished.connect(event.quit)
            self.dataTh.generateNew=False # let the thread die
            event.exec_()
            self.ui.actionRecord.toggled.disconnect()
            self.ui.actionRecord.setChecked(False)

    @QtCore.pyqtSlot()
    def dataTh_finished(self):
        print('data thread has finished')



#     @QtCore.pyqtSlot()
#     def Quit(self):
#         print("I am in quit")
#         self.close()
#         if self.dataTh.wait(1000):
#             self.dataTh.terminate()

    '''
    
    
    Events
    
    
    '''
    def closeEvent(self, ce):
        print("Close requested")
        self.cleanUp()
#         self.fileQuit()
#         self.ui.action_Quit.triggered.disconnect()
        print("Saving settings")
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        self.settings.setValue("Npeaks",self.ui.spinBox_Npeaks.value())
        self.settings.setValue("recordingLength",self.ui.doubleSpinBox_recordingLength.value())

        del self.settings
#         self.on_action_Quit_triggered()
#         ce.ignore()
#         pass
        ce.accept()


    def keyPressEvent(self, event):
#         if event.key() == QtCore.Qt.Key_Q:
#             print "Killing"
#             self.deleteLater()
        if event.key() == QtCore.Qt.Key_Left:
            self.matplotlibWidget.previousMaximum()
            print('Current maximum:', self.matplotlibWidget.currentMaximum)
            self.matplotlibWidget.mkplot()
        elif event.key() == QtCore.Qt.Key_Right:
            self.matplotlibWidget.nextMaximum()
            print('Current maximum:', self.matplotlibWidget.currentMaximum)
            self.matplotlibWidget.mkplot()
        event.accept()


    '''
    
    
    Actions
    
    
    '''
        
    @QtCore.pyqtSlot(bool)
    def on_actionRecord_toggled(self, isOn):
#         self.matplotlibWidget.setFocus()
        self.ui.frame.setFocus()
        print(isOn)
        if isOn:
#             self.sampling_freq=self.settings.value("sampling",44100, type=float)
#             self.soundSpeed=self.settings.value("soundSpeed",343.0,type=float)
#             self.plotRefreshRate=self.settings.value("plotRefreshRate",1.0,type=float)
# #             self.ui.doubleSpinBox_length.value()
#             self.dataTh=recordSignal.newSample(update_time=self.plotRefreshRate,
#                                                sampling_freq=self.sampling_freq,
#                                                soundSpeed=self.soundSpeed,
# #                                                parent=self
#                                                )
#             self.dataTh=recordSignal.newSample(
# #                                                parent=self
#                                                )
            self.dataTh=recordSignal.newSoundSample(recordingLength=self.ui.doubleSpinBox_recordingLength.value())
            self.dataTh.newSamplePowerSignal.connect(self.matplotlibWidget.mkplot)
            self.dataTh.newSampleSignal.connect(self.on_new_sample_captured)
            self.dataTh.finished.connect(self.dataTh_finished)
            self.recorded_data={'samples' : []}

            self.matplotlibWidget.clearData()
            print("Starting data thread")
            self.dataTh.start()
            print("Thread started")
            self.statusBar.showMessage("Recording")
#             x=np.arange(1000)
#             y=np.sin(x)
#             self.newSampleSignal.emit(list(x),list(y))
#         self.matplotlibWidget.mkplot()
        else:
            self.show_statusBarMsg("Stopping data thread",0)
            event=QtCore.QEventLoop()
            self.ui.setEnabled(False)
            self.dataTh.finished.connect(event.quit)
            self.dataTh.generateNew=False # let the thread die
            event.exec_()
            self.ui.setEnabled(True)
            self.show_statusBarMsg("Ready")
#             self.dataTh.terminate()
#             self.dataTh.newSampleSignal.disconnect()
            self.ui.actionSaveAs.setEnabled(True)
        print("exiting slot")
        self.show_statusBarMsg("Use arrow keys to select maximum",0)
        
        
    @QtCore.pyqtSlot(bool)
    def on_actionPlay_toggled(self, isOn):
        self.ui.frame.setFocus()

        if isOn:
            self.dataTh=recordSignal.newSoundSample(soundFile=self.soundFileName,
                                                    recordingLength=self.ui.doubleSpinBox_recordingLength.value())
            self.dataTh.newSamplePowerSignal.connect(self.matplotlibWidget.mkplot)
            self.dataTh.finished.connect(self.dataTh_finished)
            self.matplotlibWidget.clearData()
            print("Starting data thread")
            self.dataTh.start()
            print("Thread started")
            self.show_statusBarMsg("Playing "+self.soundFileName,0)
#             x=np.arange(1000)
#             y=np.sin(x)
#             self.newSampleSignal.emit(list(x),list(y))
#         self.matplotlibWidget.mkplot()
        else:
            self.show_statusBarMsg("Stopping data thread",0)
            event=QtCore.QEventLoop()
            self.ui.setEnabled(False)
            self.dataTh.finished.connect(event.quit)
            self.dataTh.generateNew=False # let the thread die
            event.exec_()
            self.ui.setEnabled(True)
            self.show_statusBarMsg("Ready")
#             self.dataTh.terminate()
#             self.dataTh.newSampleSignal.disconnect()
        print("exiting slot")
        
        
    @QtCore.pyqtSlot()
    def on_actionOpenFile_triggered(self):
#         fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '.',"Audio files (*.wav)")        
#         print(fname)

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        mysettings=global_settings.mySettings()
        prevFileName=mysettings.value("LastOpenedFile",".",type=str)
        print('prevFileName: %s' % prevFileName)
#         prevFileName=""
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Select audio file to load", prevFileName,"Audio files (*.wav);;All Files (*)", options=options)
        if fileName:
            print(fileName)
            mysettings.setValue("LastOpenedFile",fileName)
            self.soundFileName=fileName
            self.show_statusBarMsg("Selected sound file: "+fileName)
            self.newSoundFileSelected.emit(fileName)
            self.ui.actionPlay.setEnabled(True)
            self.ui.actionSaveAs.setEnabled(True)

    @QtCore.pyqtSlot()
    def on_actionSaveAs_triggered(self):
#         fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '.',"Audio files (*.wav)")        
#         print(fname)

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        mysettings=global_settings.mySettings()
        prevFileName=mysettings.value("LastSavedFile",".",type=str)
        print('prevFileName: %s' % prevFileName)
#         prevFileName=""
#         saveFileName = QtWidgets.QFileDialog.getExistingDirectory(self,"Select destination folder", prevFileName, options=options)
        saveFileName = QtWidgets.QFileDialog.getSaveFileName(self, "Save File",
                           prevFileName,options=options);
        if saveFileName[0]!='':
            saveFileName=saveFileName[0]
            print(saveFileName)
            mysettings.setValue("LastSavedFile",saveFileName)
            self.soundFileName=saveFileName
#             self.show_statusBarMsg("Not implemented yet")
#             self.show_statusBarMsg("Selected sound file: "+saveFileName)
#             self.newSoundFileSelected.emit(saveFileName)
#             self.ui.actionPlay.setEnabled(True)
            allsamples=[]
            for s in self.recorded_data['samples']:
                allsamples+=s
            print("All samples length {}".format(len(allsamples)))
            allsamples=np.asanyarray(allsamples, dtype=float)
            wf.write(saveFileName,int(mysettings.value('sampling',type=float)),allsamples)
            self.show_statusBarMsg("Saving to file {}".format(saveFileName))

        
    @QtCore.pyqtSlot()
    def on_action_Quit_triggered(self):
        self.cleanUp()
        
        self.close()


    @QtCore.pyqtSlot()
    def on_actionPreferences_triggered(self):
        prefs=preferences.PreferencesWindow()
#         prefs.preferencesSignal.connect(self.show_statusBarMsg)
        if prefs.exec_():
            self.show_statusBarMsg("Preferences saved")
        else:
            self.show_statusBarMsg("Cancelled")

#         prefs.show()



    @QtCore.pyqtSlot()
    def on_action_About_triggered(self):
        QtWidgets.QMessageBox.about(self, "About", "Resonant Frequency Viewer (v."+global_settings.PROGRAM_VERSION+")"+"""        

This program calculates and visualizes spectrum of acoustic waves provided from a microphone or from a sound file. 
It shows acoustic modes of resonating or rotating objects and relation to their length scales (dimensions) or rotation frequencies via provided speed of sound.

For example, the program can be used to estimate length of an excited metal bar, and to identify resonance frequencies
and the corresponding length scales of mechanical components (e.g. in a running car) or to test 1/f noise and microphonic effects in electrical devices the program runs on.

Copyright (2019) Bartosz Lew (bartosz.lew@protonmail.com)

"""
                                )



    @QtCore.pyqtSlot(bool)
    def on_actionLogarithmic_scale_X_toggled(self,tf):
        settings=global_settings.mySettings(self)
        settings.setValue('Logarithmic_scale_X',tf)
        self.matplotlibWidget.configurePlotAxes()

    @QtCore.pyqtSlot(bool)
    def on_actionLogarithmic_scale_Y_toggled(self,tf):
        settings=global_settings.mySettings(self)
        settings.setValue('Logarithmic_scale_Y',tf)
        self.matplotlibWidget.configurePlotAxes()

    @QtCore.pyqtSlot(bool)
    def on_actionPlotAverage_toggled(self,tf):
        settings=global_settings.mySettings(self)
        settings.setValue('PlotAverage',tf)
        self.matplotlibWidget.mkplot()

    @QtCore.pyqtSlot(bool)
    def on_actionPlotMaximalValues_toggled(self,tf):
#         print(tf)
        settings=global_settings.mySettings(self)
        settings.setValue('PlotMaximalValues',tf)
        self.matplotlibWidget.mkplot()

    @QtCore.pyqtSlot(bool)
    def on_actionFocus_on_plot_triggered(self,tf):
        self.ui.frame.setFocus()
        self.show_statusBarMsg("Use arrow keys to select maximum",0)

        
    @QtCore.pyqtSlot(list,list)
    def on_new_sample_captured(self,t,sig):
#         self.recorded_data['sample']=np.vstack([np.array(t),np.array(sig)]).T
        self.recorded_data['samples'].append(sig)

        print("Captured new sound sample ({} samples, duration {} s".format(
            len(t),t[-1]))
        print(len(self.recorded_data['samples']))

#     def write_to_file(self,):
