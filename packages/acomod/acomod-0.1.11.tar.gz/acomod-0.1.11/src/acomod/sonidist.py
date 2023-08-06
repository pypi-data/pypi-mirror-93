'''
Created on Feb 10, 2019

@author: Bartosz Lew <bartosz.lew@protonmail.com>
'''
import os,sys
sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))  

# from PyQt5 import sip
from PyQt5 import QtWidgets 
from acomod import MainWindow

sys._excepthook = sys.excepthook
def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = exception_hook



def main():
    app = QtWidgets.QApplication(sys.argv)
    progMainWindow = MainWindow.MainWindow()
    progMainWindow.show()
    try:
        sys.exit(app.exec_())
    except:
        print("exiting")
        raise

if __name__ == '__main__':
    main()
    