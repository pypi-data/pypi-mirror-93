'''
Created on Feb 11, 2019

@author: blew
'''
import pkg_resources
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui,uic
from PyQt5.QtCore import QSettings
from acomod import global_settings

class PreferencesWindow(QtWidgets.QDialog):
    preferencesSignal = QtCore.pyqtSignal(str)

    def __init__(self,parent=None):
        super(PreferencesWindow, self).__init__()
        try:
            self.ui=uic.loadUi('preferences.ui', self)
        except:
            self.ui=uic.loadUi(pkg_resources.resource_filename('acomod','preferences.ui'), self)
#         self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        settings=global_settings.mySettings(self)
        self.ui.doubleSpinBox_sampling.setValue(settings.value('sampling',44100,type=float))
        self.ui.doubleSpinBox_plotRefreshRate.setValue(settings.value('plotRefreshRate',5,type=float))
        self.ui.doubleSpinBox_soundSpeed.setValue(settings.value('soundSpeed',343,type=float))
        self.ui.spinBox_plotPointsCount.setValue(settings.value('plotPointsCount',500,type=int))
        self.ui.spinBox_maximumMinPoints.setValue(settings.value('maximumMinPoints',10,type=int))
        self.ui.buttonBox.accepted.connect(self.on_accept)
        self.ui.buttonBox.rejected.connect(self.on_reject)


    @QtCore.pyqtSlot()
    def on_accept(self):
        settings=global_settings.mySettings(self)
        settings.setValue('sampling',self.ui.doubleSpinBox_sampling.value())
        settings.setValue('plotRefreshRate',self.ui.doubleSpinBox_plotRefreshRate.value())
        settings.setValue('soundSpeed',self.ui.doubleSpinBox_soundSpeed.value())
        settings.setValue('plotPointsCount',self.ui.spinBox_plotPointsCount.value())
        settings.setValue('maximumMinPoints',self.ui.spinBox_maximumMinPoints.value())

#         self.settings.writeSettings()
#         self.settings.sync()
#         del self.settings
        print("Settings saved")
        self.preferencesSignal.emit("Settings saved") # why connecting to this signal from the
        # invoking class causes segfault ?
        
    @QtCore.pyqtSlot()
    def on_reject(self):
        print("Settings not saved")
        self.preferencesSignal.emit("Settings not saved")
