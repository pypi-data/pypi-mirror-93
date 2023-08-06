'''
Created on Feb 12, 2019

@author: Bartosz Lew <bartosz.lew@umk.pl>
'''

import os,sys
from PyQt5 import QtCore
PROGRAM_NAME="Acoustic Oscillations Viewer"
COMPANY_NAME="Torun Centre for Astronomy"
PROGRAM_VERSION='0.1 alpha'

class mySettings(QtCore.QSettings):
    def __init__(self,parent=None):
        super(mySettings,self).__init__(COMPANY_NAME,PROGRAM_NAME, parent=parent)


