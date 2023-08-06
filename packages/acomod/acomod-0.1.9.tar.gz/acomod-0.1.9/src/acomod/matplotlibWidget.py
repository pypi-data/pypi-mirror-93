'''
Created on Feb 11, 2019

@author: blew
'''
from PyQt5 import QtWidgets, QtCore, QtGui,uic
import sys

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
from acomod import global_settings
import copy
from scipy.signal import argrelextrema

class MatplotlibWidget(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, Npeaks=1):
        super(MatplotlibWidget, self).__init__(Figure(figsize=(width, height), dpi=dpi))
        self.setParent(parent)
        
        fig = self.figure
        self.axes = fig.add_subplot(111)
        self.settings=global_settings.mySettings(self)
        self.cs=self.settings.value("soundSpeed",type=float)
        self.Npeaks=Npeaks
        
#         self.

#         self.mkplot()

#         FigureCanvas.__init__(self, fig)

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        self.updateGeometry()

        self.updatablePlotArtists=[]
        self.plotLabels=None
        self.rawFnPlot=None
        self.avgFnPlot=None
        self.maxFnPlot=None
        self.rawFn=None
        self.avgFn=None
        self.sumFn=None
        self.maxFn=None
        self.dataCount=0
#         self.axis.clear()

        self.currentMaximum=0
        self.configurePlotAxes()



    def configurePlotAxes(self):
        settings=global_settings.mySettings(self)
        self.plotPointsCount=settings.value("plotPointsCount",type=int)
        self.axes.set_xlabel('Frequency [Hz]')
        self.axes.set_ylabel('Power [$Hz^{-1}$]')
        if settings.value("Logarithmic_scale_X",type=bool):
            self.axes.set_xscale("log")
        else:
            self.axes.set_xscale("linear")
            
        if settings.value("Logarithmic_scale_Y",type=bool):
            self.axes.set_yscale("log")
        else:
            self.axes.set_yscale("linear")
        
        self.resetRanges()
        self.draw()
         
    @QtCore.pyqtSlot()
    def clearData(self):
        self.rawFn=None
        self.sumFn=None
        self.maxFn=None
        self.plotLabels=None
        self.dataCount=0
        self.selectedMaxima=None

    def find_maxima(self, fn,Npeaks,maximumMinPoints=10):
        m,=argrelextrema(fn[:,1], np.greater,order=maximumMinPoints)
#         print(m)
#         print(len(m))
        
        return fn[:,0][m],fn[:,1][m]
#         pass

    def plot_labels(self,X,Y):
        if not hasattr(X,'__iter__'):
            X=[X]
        if not hasattr(Y,'__iter__'):
            Y=[Y]
#         print(X,Y)
        for x,y in zip(X,Y):
            vl=self.axes.axvline(x,lw=1, color='c')
            self.updatablePlotArtists.append(vl)
            l=self.cs/x
#             offset=10
            t=self.axes.text(x,y,' {0:.1f} Hz\n {1:.3f} m'.format(x,l), fontsize=14)
#             t=self.axes.text(x,y,'{0:.1f} Hz'.format(x))
            self.updatablePlotArtists.append(t)
            


    def binFn(self,Fn):
#         bs=len(Fn) // self.plotPointsCount
        settings=global_settings.mySettings(self)
        self.plotPointsCount=settings.value("plotPointsCount",type=int)
        
        f,e1=np.histogram(Fn[:,0], self.plotPointsCount,weights=Fn[:,1])
        x=[(e1[i]+e1[i+1])/2 for i in range(len(e1)-1)]
#         y=[(y[i]*e2[i]/+y[i+1])/2 for i in range(len(Fn-1))]
        return x,f

    def resetRanges(self):
        if type(self.rawFn)!=type(None):
            self.axes.set_xlim(min(self.rawFn[:,0]),max(self.rawFn[:,0]))        

#             if type(self.maxFn)!=type(None):
            self.axes.set_ylim(min(self.rawFn[:,1]),max(self.maxFn[:,1]))        


    def selectMaxima(self,n):
        if n>0:
            self.selectedMaxima=np.sort(self.sortedMaxima[:self.Npeaks],order='f')
        else:
            self.selectedMaxima=[]
            
    def plotMaxima(self):
        plotLabels, =self.axes.plot(self.selectedMaxima['f'],self.selectedMaxima['P'],'ko')
        self.updatablePlotArtists.append(plotLabels)
        
    def nextMaximum(self):
        self.currentMaximum=(self.currentMaximum+1) % len(self.selectedMaxima)

    def previousMaximum(self):
        self.currentMaximum=(self.currentMaximum-1) % len(self.selectedMaxima)

    @QtCore.pyqtSlot(list,list)
    def mkplot(self,x=None,y=None):
        if type(x)!=type(None) and type(y)!=type(None):
            x=np.asarray(x,dtype=float)
            y=np.asarray(y,dtype=float)
            self.rawFn=np.vstack((x,y)).T
    #         sys.exit()
            # calculate sum
            if type(self.sumFn)==type(None):
                self.sumFn=np.array([x,y],dtype=float).T
                self.maxFn=np.zeros(len(self.sumFn)*2).reshape(-1,2)
            else:
                self.sumFn+=np.array([x,y],dtype=float).T
            self.dataCount+=1
                
                
            # calculate average
            self.avgFn=self.sumFn/self.dataCount
    
            # calculate maximal values
            self.maxFn=np.array([ [x[0],max(x[1],y[1])] for x,y in zip(self.rawFn,self.maxFn) ])
    #         print(self.maxFn)



        #
        # find maxima
        # 
        self.Npeaks=self.settings.value("Npeaks",10,int)
        if type(self.maxFn)!=type(None):
            maximumMinPoints=self.settings.value("maximumMinPoints",type=int)
            maxx,maxy=self.find_maxima(self.maxFn,self.Npeaks,maximumMinPoints)

            L=[ self.cs/x for x in maxx]
    #             t=self.axes.text(x,y,'{0:.1f} Hz\n{1:.3f} m'.format(x,l))
            self.sortedMaxima=np.sort(np.array([(x,y,l) for x,y,l in zip(maxx,maxy,L)], dtype=[('f',float),('P',float),('L',float)]), 
                                 axis=0, order='P')[::-1]
            self.selectMaxima(self.Npeaks)
    #         self.sortedMaxima=np.sort(self.sortedMaxima, order='f')
    #         print(sortedMaxima)
    #         print(sortedMaxima['x'],sortedMaxima['y'])
        
            if self.Npeaks>0:
                print("Maxima frequencies and corresponding lengths, sorted according to decreasing spectral power [(Hz,m)]:")
                print(self.selectedMaxima[['f','L','P']])





        


        #
        # remove updatable artists            
        #
        while len(self.updatablePlotArtists)>0:
            self.updatablePlotArtists[0].remove()
            self.updatablePlotArtists.pop(0)

#         if self.rawFnPlot!=None:
#             self.rawFnPlot.remove()
#             self.rawFnPlot=None # this is not needed but for purity

        #
        # plot
        #
        if type(self.maxFn)!=type(None):
            self.plotPointsCount=self.settings.value("plotPointsCount",type=int)
            bs=len(self.rawFn)//self.plotPointsCount
            if bs<1:
                bs=1
    #         x,y=self.binFn(np.array([x,y],dtype=float).T)
            x,y=self.rawFn[::bs][:,0],self.rawFn[::bs][:,1]
            rawFnPlot, =self.axes.plot(x,y,'k-')
            self.updatablePlotArtists.append(rawFnPlot)
    
            if self.settings.value("PlotAverage",type=bool):
                x,y=self.avgFn[::bs][:,0],self.avgFn[::bs][:,1]
    #             x,y=self.binFn(self.avgFn)
                avgFnPlot, =self.axes.plot(x,y,'g-', zorder=10, lw=2)
    #             avgFnPlot, =self.axes.plot(self.avgFn[:,0],self.avgFn[:,1],'g-', zorder=10, lw=2)
                self.updatablePlotArtists.append(avgFnPlot)
            if self.settings.value("PlotMaximalValues",type=bool):
                x,y=self.maxFn[::bs][:,0],self.maxFn[::bs][:,1]
    #             x,y=self.binFn(self.maxFn)
                maxFnPlot, =self.axes.plot(x,y,'r-', zorder=20)
    #             avgFnPlot, =self.axes.plot(self.maxFn[:,0],self.maxFn[:,1],'r-', zorder=20)
                self.updatablePlotArtists.append(maxFnPlot)
    



            #
            # plot maxima
            #
            if self.Npeaks>0:
                self.plotMaxima()

        
            #
            # plot labels
            #
    #         self.plot_labels(self.selectedMaxima['f'],self.selectedMaxima['P'])
    #         print(self.selectedMaxima['P'][self.currentMaximum])
            if self.Npeaks>0:
                if self.currentMaximum>=self.Npeaks:
                    self.currentMaximum=self.Npeaks-1
                if len(self.selectedMaxima['f'])>self.currentMaximum:
                    self.plot_labels(self.selectedMaxima['f'][self.currentMaximum],self.selectedMaxima['P'][self.currentMaximum])
    
            self.resetRanges()
            self.draw()
        
#         sd.play(y, 11600)
#         sd.default.samplerate = self.ui.doubleSpinBox_sampling.value()
#         sd.play(y)

        
