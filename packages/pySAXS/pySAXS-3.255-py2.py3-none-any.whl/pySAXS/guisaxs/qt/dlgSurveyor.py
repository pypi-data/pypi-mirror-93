from PyQt5 import QtCore, QtGui, QtWidgets, uic

#from PyQt4.Qt import QString
from fileinput import filename
from pyFAI import azimuthalIntegrator
from pySAXS.guisaxs import dataset
from pySAXS.guisaxs.qt import preferences
from pySAXS.guisaxs.qt import QtMatplotlib
from pySAXS.guisaxs.qt import dlgAbsoluteI
from pySAXS.guisaxs.qt import dlgAutomaticFit
import matplotlib.colors as colors
from pySAXS.tools import FAIsaxs
from pySAXS.tools import filetools
import os
import sys
from scipy import ndimage
if sys.version_info.major>=3:
    import configparser 
else:
    import ConfigParser as configparser
from pySAXS.guisaxs.qt.dlgAbsoluteI import dlgAbsolute
from matplotlib.patches import Circle
from PyQt5 import QtTest
from pySAXS.guisaxs import pySaxsColors


AUTOMATIC_FIT=False


def my_excepthook(type, value, tback):
    # log the exception here
    #print value
    #print tback
    # then call the default handler
    sys.__excepthook__(type, value, tback)

sys.excepthook = my_excepthook

#from reportlab.graphics.widgets.table import TableWidget
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.patches as patches
from matplotlib.lines import Line2D 
#from spyderlib.widgets.externalshell import namespacebrowser
from time import *
import fabio
import numpy
import os.path
import pyFAI
import sys
import threading
import glob
import fnmatch

import pySAXS
from  pySAXS.LS import SAXSparametersXML
from pySAXS.guisaxs.qt import dlgQtFAITest



ICON_PATH=pySAXS.__path__[0]+os.sep+'guisaxs'+os.sep+'images'+os.sep 

HEADER=['name','x','z','exposure','Trans. Flux','Incid. Flux']
FROM_EDF=['Comment','x','z','count_time','pilroi0','pilai1']
FROM_RPT=['filename','samplex','samplez',"exposure","transmitted flux","incident flux"]

#IMAGE_PARAMS={"edf":FROM_EDF,"tiff":FROM_RPT} 
IMAGE_TYPE=['*.edf*','*.TIFF*','*.tif','*.tiff']



class SurveyorDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, parameterfile=None, outputdir=None):
        QtWidgets.QWidget.__init__(self, parent)
        #self.ui = dlgSurveyorui.Ui_surveyorDialog()
        self.ui = uic.loadUi(pySAXS.UI_PATH+"dlgSurveyor.ui", self)#
        #print experimentName
        self.setWindowTitle('Continuous Radial averaging tool for pySAXS')
        if parent is not None:
            # print "icon"
            self.setWindowIcon(parent.windowIcon())
        
        '''self.experimentName=experimentName
        if EXPERIMENT_PARAMS.has_key(experimentName):
            self.FROM_EXPERIMENT=EXPERIMENT_PARAMS[experimentName][1]
        else:
            self.FROM_EXPERIMENT=None
        '''
        #plt=self.ui.matplotlibwidget
        
        self.parent = parent
        self.plotapp= None
        self.printout = None
        self.whereZ=False
        self.workingdirectory = None
        self.fai=None
        self.faiMemory=None
        self.lastDatas=None
        
        self.pixmapExcl = QtGui.QPixmap(ICON_PATH+'exclamation.png')
        self.pixmapValid = QtGui.QPixmap(ICON_PATH+'tick.png')
        
        
        
        self.plt=self.ui.matplotlibwidget.figure
        self.plt.patch.set_facecolor('White')
        self.canvas = FigureCanvas(self.plt)
        #self.axes = self.plt.gca()
        self.axes = self.plt.add_subplot(111)#subplots()
        self.clbar=None#(imgplot)
        self.plt.tight_layout()
        #self.plt.subplots(constrained_layout=True)
        
        #self.ui.setupUi(self)
        self.ui.paramFileButton.clicked.connect(self.OnClickparamFileButton)
        self.ui.changeDirButton.clicked.connect(self.OnClickchangeDirButton)
        #QtCore.QObject.connect(self.ui.STARTButton, QtCore.SIGNAL("clicked()"), self.OnClickSTARTButton)
        #QtCore.QObject.connect(self.ui.STOPButton, QtCore.SIGNAL("clicked()"), self.OnClickSTOPButton)
        #self.ui.plotChkBox.clicked.connect(self.OnClickPlotCheckBox)
        self.ui.btnExtUpdate.clicked.connect(self.updateListInit)
        self.ui.tableWidget.cellClicked[int, int].connect(self.cellClicked)
        self.ui.tableWidget.cellDoubleClicked[int, int].connect(self.cellDoubleClicked)
        self.ui.btnDisplaySelected.clicked.connect(self.btnDisplayClicked)
        self.ui.btnZApply.clicked.connect(self.btnZApplyClicked)
        self.ui.btnReset.clicked.connect(self.btnZResetClicked)
        self.ui.btnDisplayAV.clicked.connect(self.btnDisplayAVClicked)
        self.ui.btnProcessSelection.clicked.connect(self.btnProcessSelectionClicked)
        self.ui.btnProcessALL.clicked.connect(self.btnProcessALLClicked)
        self.ui.paramViewButton.clicked.connect(self.OnClickparamViewButton)
        self.ui.btnCenterOfMass.clicked.connect(self.OnClickCenterOfMassButton)
        self.ui.btnExportList.clicked.connect(self.OnClickExportList)
        self.ui.navi_toolbar = NavigationToolbar(self.ui.matplotlibwidget, self)
        self.ui.verticalLayout_2.insertWidget(0,self.ui.navi_toolbar)#verticalLayout_2
        l=self.ui.navi_toolbar.actions()
        #remove the Pan tool
        l=self.ui.navi_toolbar.actions()
        for i in l:
            #print i.text()
            if i.text()=='Pan':
                panAction=i
            if i.text()=='Customize':
                customizeAction=i
            if i.text()=='Subplots':
                subplotAction=i
            
        #self.ui.navi_toolbar.removeAction(panAction)
        self.ui.navi_toolbar.removeAction(customizeAction)
        self.ui.navi_toolbar.removeAction(subplotAction)
        #--Autoscale
        self.AutoscaleAction= QtWidgets.QAction('Autoscale', self)
        self.AutoscaleAction.triggered.connect(self.OnAutoscale)
        self.ui.navi_toolbar.addAction(self.AutoscaleAction)
        #-- fix scale
        self.FixScaleAction= QtWidgets.QAction(QtGui.QIcon(ICON_PATH+'magnet.png'),'Fix Scale', self)
        self.FixScaleAction.setCheckable(True)
        self.FixScaleAction.setChecked(False)
        self.FixScaleAction.triggered.connect(self.OnButtonFixScale)
        self.ui.navi_toolbar.addAction(self.FixScaleAction)
        
        self.SelectedFile=None
        self.ui.labelSelectedFIle.setText("")
        self.ui.btnDisplaySelected.setEnabled(False)
        self.ui.btnDisplayAV.setEnabled(False)
        self.ui.radioButton_lin.setChecked(True)
        self.ui.radioButton_lin.toggled.connect(lambda:self.btnStateLinLog(self.radioButton_lin))
        #self.ui.radioButton_log.toggled.connect(lambda:self.btnStateLinLog(self.radioButton_log))
        self.DISPLAY_LOG=False
        self.EXPORT_LIST=[]
        
        self.ui.chkDisplayBeam.clicked.connect(self.OnClickDisplayBeam)
        self.ui.chkDisplayCircles.clicked.connect(self.btnDisplayClicked)
        #self.ui.btnGetBeamXY.clicked.connect(self.OnClickGetBeamXY)
        self.ui.btnBeamApply.clicked.connect(self.OnClickButtonBeam)
        #self.ui.btnTransferParams.clicked.connect(self.OnClickButtonTransferParams)
        self.ui.edit_Q.textChanged.connect(self.btnDisplayClicked)
        self.ui.edit_dd.textChanged.connect(self.btnDisplayClicked)
        self.ui.chkDisplayMaskFile.clicked.connect(self.btnDisplayClicked)
        self.ui.btnResetGeom.clicked.connect(self.btnResetGeometry)
        
        if AUTOMATIC_FIT:
            self.ui.btnAutomaticFit.setEnabled(True)
            self.automaticFitApp = dlgAutomaticFit.dlgAutomaticFit(parent)
            #self.automaticFitApp.show()
            self.ui.btnAutomaticFit.clicked.connect(self.btnDisplayAutomaticFitClicked)
            self.ui.btnPAF.setEnabled(True)
            self.ui.btnPAF.clicked.connect(self.btnProcessALLClicked)
        #--- absolute intensities
        self.ui.btnCheckSolvent.clicked.connect(self.btnCheckSolventClicked)
        if self.parent is None:
            self.ui.chkSubSolvent.setEnabled(False)
            self.ui.btnCheckSolvent.setEnabled(False)
        else:
            if self.parent.referencedata is not None:
                self.ui.solventEdit.setText(str(self.parent.referencedata))
            
        
        
        self.parameterfile=parameterfile
        try:
            if self.parameterfile is not None and self.parameterfile!="":
                self.ui.paramTxt.setText(str(parameterfile))
        except:
            pass
            
        
            
         #-- get preferences
        self.pref=preferences.prefs()
        
        if parent is not None:
            self.printout = parent.printTXT
            self.workingdirectory = parent.workingdirectory
            self.pref=self.parent.pref
            #print("import pref")
            #print(self.pref)
            #print(self.pref.getName())
            try:
                if self.pref.fileExist():
                    self.pref.read()
                    #print "file exist"
                    dr=self.pref.get('defaultdirectory',section="guisaxs qt")
                    #print "dr :",dr
                    if dr is not None:
                        self.workingdirectory=dr
                        #print 'set wd',dr
                        self.ui.DirTxt.setText(str(self.workingdirectory))
                    pf=self.pref.get('parameterfile',section="pyFAI")
                    
                    if pf is not None:
                        self.parameterfile=pf
                        self.ui.paramTxt.setText(str(self.parameterfile))
                        try:
                            self.OnClickButtonTransferParams()
                        except:
                            print("problem when trying to read parameters")
                    
                    ext=self.pref.get('fileextension',section="pyFAI")
                    if ext is not None:
                        self.ui.extensionTxt.setText(ext)
                    
                
                else:
                    self.pref.save()
            except:
                print("couldnt reach working directory ")
                return
            
            
        else :
            self.workingdirectory = "Y:/2017/2017-08-24-OT" #for debugging
            self.ui.DirTxt.setText(self.workingdirectory)   #for debugging
            
        #print(self.workingdirectory)
        self.imageToolWindow = None
        self.updateListInit()
        self.fp = str(self.ui.DirTxt.text())
        txt=""
        for i in IMAGE_TYPE:
            txt+=i+" "
        self.ui.extensionTxt.setText(txt)
        '''self.qfsw = QtCore.QFileSystemWatcher()
        self.fp = str(self.ui.DirTxt.text())
        if self.fp!='':
            self.qfsw.addPath(self.fp)
            QtCore.QObject.connect(self.qfsw,QtCore.SIGNAL("directoryChanged(QString)"),self.onFileSystemChanged)
            #self.qfsw.directoryChanged.connect(self.updateListInit)
        '''
        self._fileSysWatcher    = QtCore.QFileSystemWatcher()
        if self.fp!='':
            if os.path.isdir(self.fp):
                self._fileSysWatcher.addPath(self.fp)
                self._fileSysWatcher.directoryChanged.connect(self.slotDirChanged)
                
        
        
        
    @QtCore.pyqtSlot("QString")   
    def slotDirChanged(self, path):
        #print(path, " changed !")
        self.updateListInit()      
        
    
    def OnClickparamFileButton(self):
        '''
        Allow to select a parameter file
        '''
        fd = QtWidgets.QFileDialog(self)
        #old=self.ui.paramTxt.text()
        filename = fd.getOpenFileName(directory=self.workingdirectory)[0]
        #self.workingdirectory = filename
        # print filename
        if filename=='':
            return
        self.ui.paramTxt.setText(filename)
        # self.ui.editor_window.setText(plik)
        self.OnClickButtonTransferParams()
        self.radialPrepare()

    def OnClickSTARTButton(self):
        '''
        Used when start button is clicked
        '''
        print("start")
        self.ui.progressBar.setRange(0,0)
        #print "start2"
        self.radialPrepare()
        #self.ui.progressBar.setValue(100)
        
        self.ui.STOPButton.setEnabled(True)
        self.ui.STARTButton.setDisabled(True)
        if self.ui.refreshTimeTxt.text() == '':
            t = 30
        else :
            t = float(self.ui.refreshTimeTxt.text())    
        #print(time)
        self.t = Intervallometre(t, self.updateList, self)
        self.t.start()
        
    def OnClickSTOPButton(self):
        '''
        Used when stop button is clicked
        '''
        print("stop")
        #self.ui.progressBar.setValue(0)
        self.ui.progressBar.setRange(0,1)
        self.ui.STARTButton.setEnabled(True)
        self.ui.STOPButton.setDisabled(True)
        self.t.stop()
        
    def OnClickchangeDirButton(self):
        '''
        Allow to select a directory
        '''
        #QFileDialog
        #fd = QtWidgets.QFileDialog(self, directory=self.workingdirectory)
        #fd.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        dir=QtWidgets.QFileDialog.getExistingDirectory(directory=self.workingdirectory)
        #if fd.exec_() == 1:
        #print fd.selectedFiles()
        #dir = str(fd.selectedFiles().first())
        #dir = str(fd.selectedFiles()[0])
        #print(dir)
        if dir=='':
            return
        if not(os.path.isdir(dir)):
            return
        # dir=fd.getOpenFileName()
        self.ui.DirTxt.setText(dir)
        self.workingdirectory = dir
        self.updateListInit()
        
        try:
            self.pref.set('defaultdirectory', self.workingdirectory,section="guisaxs qt")
            self.pref.save()
        except:
            pass
        '''    
        l=self.qfsw.directories()
        print "previous watched directories :",list(l)
        self.qfsw.removePaths(l)
        self.qfsw.addPath(dir)
        l=self.qfsw.directories()
        print "Now watched directories :",list(l)
        '''
        #print("la")
        l=self._fileSysWatcher.directories()
        #print("previous watched directories :",list(l))
        if len(l)>0:
            self._fileSysWatcher.removePaths(l)
        self._fileSysWatcher.addPath(dir)
        l=self._fileSysWatcher.directories()
        #print("now watched directories :",list(l))
            
    def cellClicked(self,row,col):
        self.SelectedFile=str(self.ui.tableWidget.item(row,0).text())
        self.ui.labelSelectedFIle.setText(self.workingdirectory+os.sep+self.SelectedFile)
        #print self.workingdirectory+os.sep+self.SelectedFile
        self.ui.btnDisplaySelected.setEnabled(True)
        self.ui.btnDisplayAV.setEnabled(True)
        
    def cellDoubleClicked(self,row,col):
        self.SelectedFile=str(self.ui.tableWidget.item(row,0).text())
        self.ui.labelSelectedFIle.setText(self.workingdirectory+os.sep+self.SelectedFile)
        #print self.workingdirectory+os.sep+self.SelectedFile
        self.ui.btnDisplaySelected.setEnabled(True)
        self.ui.btnDisplayAV.setEnabled(True)
        self.btnDisplayClicked()
        
    def btnDisplayClicked(self):
        '''
        display the image
        '''
        self.displayImage()
    
    def displayImage(self):
        '''
        display the image
        '''
        self.axes.cla() 
        if self.SelectedFile is None:
            return
        try:
            fi=self.workingdirectory+os.sep+self.SelectedFile
            self.img = fabio.open(fi) # Open image file
        except:
            print("pySAXS : unable to open imagefile : "+self.workingdirectory+os.sep+self.SelectedFile)
            #QtWidgets.QMessageBox.information(self,"pySAXS", "unable to open imagefile : "+self.workingdirectory+os.sep+self.SelectedFile, buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.NoButton)
            return
        
        D=self.img.data
        if self.ui.chkDisplayMaskFile.isChecked() and self.mad is not None:
            D = numpy.logical_not(self.mad) * D
        xmax, ymax = numpy.shape(D)
        extent = 0, xmax, 0, ymax
        if self.whereZ:
            zmin=float(self.ui.edtZmin.text())
            zmax=float(self.ui.edtZmax.text())
            D=numpy.where(D<=zmin,zmin,D)
            D=numpy.where(D>zmax,zmax,D)
        else:
            self.ui.edtZmin.setText(str(D.min()))
            self.ui.edtZmax.setText(str(D.max()))
        norm=colors.LogNorm(vmin=D.min(), vmax=D.max())
        if self.DISPLAY_LOG:
            zmin=float(self.ui.edtZmin.text())
            if zmin<=0:
                zmin=0.1
                self.ui.edtZmin.setText("0.1")
            zmax=float(self.ui.edtZmax.text())
            D=numpy.where(D<=zmin,zmin,D)
            D=numpy.where(D>zmax,zmax,D)
            norm=colors.LogNorm(vmin=D.min(), vmax=D.max())
            #--- display the mask
            if self.ui.chkDisplayMaskFile.isChecked() and self.mad is not None:
                imgplot=self.axes.imshow(numpy.logical_not(self.mad)*D,cmap="jet",norm=norm)
            else:
                imgplot=self.axes.imshow(D,cmap="jet",norm=norm)
                    
            #print "mode log"#,norm=colors.LogNorm(vmin=D.min(), vmax=D.max()))            # Display as an image  norm=colors.LogNorm(vmin=Z1.min(), vmax=Z1.max()),
        else:
            #--- display the mask
            if self.ui.chkDisplayMaskFile.isChecked() and self.mad is not None:
                imgplot=self.axes.imshow(numpy.logical_not(self.mad)*D,cmap="jet")#,norm=norm)
            else:
                imgplot=self.axes.imshow(D,cmap="jet")#,norm=norm)
            
        #imgplot.set_cmap('nipy_spectral')
        
        #--- display the mask
        '''if self.ui.chkDisplayMaskFile.isChecked():
            #   
            #self.imgMask = fabio.open(self.workingdirectory+os.sep+self.SelectedFile)
            if self.mad is not None:
                #print("mask exist in memory")
                aa=self.ui.sliderTransparency.value()/100.0
                #print(aa)
                self.axes.imshow(numpy.logical_not(self.mad)*D,cmap="jet",alpha=aa)#,extent=extent)
        '''        
        #--- fix scale
        if self.FixScaleAction.isChecked():
            #axes limits should have been memorized
            self.axes.set_xlim((self.xlim_min,self.xlim_max))
            self.axes.set_ylim((self.ylim_min,self.ylim_max))
        if self.clbar is None :
            self.clbar=self.plt.colorbar(imgplot,shrink=0.5)
        else:
            try:
                self.clbar.remove()
            except:
                pass
            self.clbar=self.plt.colorbar(imgplot,shrink=0.5)
        
                
        #---- display the beam (or not)
        if self.ui.chkDisplayBeam.isChecked():
            #draw a cross
            #try:#if text is not float
            BeamX=float(self.ui.edtBeamX.text())
            BeamY=float(self.ui.edtBeamY.text())
            xmax,ymax=numpy.shape(D)
            #print xmax, ymax
            #print plt.axes
            #except:
            #print "text is not float"
            #BeamX=0.0
            #BeamY=0.0
        
            x1, y1 = [BeamX, 0], [BeamX, ymax] #vertical
            x2, y2 = [0,BeamY], [xmax, BeamY]
            #self.axes.plot(x1, y1, x2, y2, marker = 'o')
            
            # Create a Rectangle patch
            #rect = patches.Rectangle((0, 0),BeamX, BeamY,linewidth=1,edgecolor='r',facecolor='none')
            #rect2 = patches.Rectangle((BeamX, BeamY),xmax, ymax,linewidth=1,edgecolor='r',facecolor='none')
            
            line1=Line2D([BeamX-20,BeamX+20],[BeamY,BeamY],linewidth=1,color='r')
            line2=Line2D([BeamX,BeamX],[BeamY-20,BeamY+20],linewidth=1,color='r')

            # Add the lines to the Axes
            self.axes.add_line(line1)
            self.axes.add_line(line2)
            
        
        
        #---- display the circles
        if self.ui.chkDisplayCircles.isChecked():
            #draw circle to Q
            '''
            OLD METHOD
            
            try:
                Q=float(self.ui.edit_Q.text())
                lam=float(self.ui.edit_wavelength.text())
                L=float(self.ui.edit_dd.text())
                pixelSize=float(self.ui.edit_pixelsize.text())
                sizemax=max(xmax,ymax)
                /*** from ImageJ
                qnextorder=qfirstorder*i;
                theta=Math.asin((qnextorder*lambda)/(4*pi))*2;
                // ------  calculate width and height
                ellipse_height=2*L*Math.tan(theta)/pixelSize;
                ellipse_width=(L*2*Math.sin(theta)*Math.cos(theta)*Math.sin(alpha_rad))/(Math.pow(Math.sin(alpha_rad), 2)-Math.pow(Math.sin(theta), 2));
                ellipse_width=ellipse_width/pixelSize;
                ***/
                theta=numpy.arcsin((Q*lam)/(4*numpy.pi))*2
                ellipse_height=2*L*numpy.tan(theta)/pixelSize
                #display circles
                for ccNumber in range(0,int(sizemax*2/ellipse_height)+1):
                    CC=Circle((BeamX, BeamY),ccNumber*ellipse_height/2, color="white",linewidth=1,linestyle="--",fill=False)#E,alpha=0.5)
                    self.axes.add_patch(CC)
            except:
                pass
            '''
            #--- NEW METHOD USING CONTOUR
            #get an array of q
            qim=self.fai.array_from_unit(shape=numpy.shape(self.img),unit="q_A^-1")
            #using contour
            #wich q max ?
            Q=float(self.ui.edit_Q.text())
            posq=numpy.arange(Q,qim.max(),Q) #array of q 
            CS=self.axes.contour(qim, levels=posq, cmap="autumn", linewidths=1, linestyles="dashed")
            self.axes.clabel(CS, inline=True, fontsize=10)#,fmt='%1.4f A-1')
            
            
        # Display the image
        self.plt.tight_layout()
        self.ui.matplotlibwidget.draw()
        '''except:
            pass'''
        #pyplot.show()                       # Show GUI window
    
    def btnDisplayAVClicked(self):
        if self.SelectedFile is None:
            return
        self.radialAverage(self.workingdirectory+os.sep+self.SelectedFile)
        
    def OnAutoscale(self):
        #print('autoscale')
        sh=self.img.data.shape
        plt=self.ui.matplotlibwidget
        plt.axes.set_ylim((sh[0],0))
        plt.axes.set_xlim((0,sh[1]))
        self.xlim_min,self.xlim_max=plt.axes.get_xlim()
        self.ylim_min,self.ylim_max=plt.axes.get_ylim()
        plt.draw()
    
    def OnButtonFixScale(self):
        #print("OnButtonFixScale")
        #memorize the current scale"
        plt=self.ui.matplotlibwidget
        self.xlim_min,self.xlim_max=plt.axes.get_xlim()
        self.ylim_min,self.ylim_max=plt.axes.get_ylim()
        #print self.xlim_min,self.xlim_max," - ",self.ylim_min,self.ylim_max
            
    def btnZApplyClicked(self):
        try:
            self.zmin=float(self.ui.edtZmin.text())
            zmax=float(self.ui.edtZmax.text())
            self.whereZ=True
            self.btnDisplayClicked()
            #print zmin, zmax
        except:
            pass
    def btnZResetClicked(self):
        self.whereZ=False
        self.btnDisplayClicked()
    
    def btnStateLinLog(self,b):
        #print("toggled")
        if b.text() == "lin":
            if b.isChecked() == True:
                self.DISPLAY_LOG=False
            else:
                self.DISPLAY_LOG=True
                #print "zmin text :",self.ui.edtZmin.text()
                if float(self.ui.edtZmin.text())<=0:
                    self.ui.edtZmin.setText("0.1")
                    
        self.whereZ=True
        self.btnDisplayClicked()
                
        '''if b.text() == "log":
            if b.isChecked() == True:
                self.DISPLAY_LOG=True
                if float(self.ui.edtZmin.text())<=0:
                    self.ui.edtZmin.setText("1")
            else:
                self.DISPLAY_LOG=False'''
            #self.btnDisplayClicked()
        
    def OnClickGetBeamXY(self):
        '''
        try to get Beam X Y from parameter file
        '''
        if self.ui.paramTxt.text()=="":
            QtWidgets.QMessageBox.information(self,"pySAXS", "Parameter file is not specified", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.NoButton)
            return
        
        filename = self.ui.paramTxt.text()
        if not os.path.exists(filename):
            self.printTXT(filename + ' does not exist')
            QtWidgets.QMessageBox.information(self,"pySAXS", str(filename) + " does not exist", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.NoButton)
            return
        if self.fai is None:
            self.radialPrepare()
        self.fai.setGeometry(filename)
        self.ui.edtBeamY.setText(str(self.fai._xmldirectory['user.centery']))
        self.ui.edtBeamX.setText(str(self.fai._xmldirectory['user.centerx']))
        self.ui.chkDisplayBeam.setChecked(True)
        #display beam
        #self.OnClickButtonBeam()
    
    def OnClickButtonTransferParams(self):
        #print('transfer params')
        if self.ui.paramTxt.text()=="":
            QtWidgets.QMessageBox.information(self,"pySAXS", "Parameter file is not specified", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.NoButton)
            return
        
        filename = self.ui.paramTxt.text()
        if not os.path.exists(filename):
            self.printTXT(filename + ' does not exist')
            QtWidgets.QMessageBox.information(self,"pySAXS", str(filename) + " does not exist", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.NoButton)
            return
        #if self.fai is None:
        self.radialPrepare()
        self.fai.setGeometry(filename)
        self.ui.edtBeamY.setText('%6.2f'%self.fai._xmldirectory['user.centery'])
        self.ui.edtBeamX.setText('%6.2f'%self.fai._xmldirectory['user.centerx'])
        self.ui.edit_pixelsize.setText("%6.4f" %(self.fai._xmldirectory['user.PixelSize']))
        self.ui.edit_wavelength.setText("%6.4f" %self.fai._xmldirectory['user.wavelength'])
        self.ui.edit_dd.setText('%6.4f'%(self.fai._xmldirectory['user.DetectorDistance']))
        self.ui.edit_maskfile.setText(str(self.fai._xmldirectory['user.MaskImageName']))
        self.faiMemory=self.fai #keep geometry in memory
        self.displayImage()
    
    def OnClickButtonBeam(self):
        #print('on click button beam')
        self.ui.chkDisplayBeam.setChecked(True)
        p=self.fai.getFit2D()
        #print(p)
        BeamX=float(self.ui.edtBeamX.text())
        BeamY=float(self.ui.edtBeamY.text())
        L=float(self.ui.edit_dd.text())
        #self.fai.set_dist(L/100)
        self.fai.setFit2D(directDist=L*10, centerX=BeamX, centerY=BeamY,
                 tilt=p['tilt'], tiltPlanRotation=p['tiltPlanRotation'],
                 pixelX=p['pixelX'], pixelY=p['pixelY'], splineFile=p['splineFile'])
        #print(self.fai.getFit2D())
        #--simply redraw the image
        self.displayImage()
    
    def btnResetGeometry(self):
        '''
        reset geometry
        '''
        self.OnClickButtonTransferParams()
        
    def updateList(self):
        '''
        Update the list
        '''
        #print("refresh")
        #print '-UPDATE LIST'
        self.ext = str(self.ui.extensionTxt.text())
        if self.ext == '':
              self.ext = '*.*'
        self.fp = str(self.ui.DirTxt.text())
        #print self.fp
        listoffile = self.getList(self.fp, self.ext)
        #print listoffile
        files=sorted(listoffile,reverse=True)
        #print files
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setRowCount(len(listoffile))
        headerNames = ["File", "date", "processed", "new"]
        self.ui.tableWidget.setHorizontalHeaderLabels(headerNames)
        self.ui.tableWidget.setColumnWidth(0, 220)
        self.ui.tableWidget.setColumnWidth(1, 150)
        self.ui.tableWidget.setColumnWidth(2, 70)
        self.ui.tableWidget.setColumnWidth(3,50)
        i = 0
        for name in files:
            self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(name))
            self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(listoffile[name][0])))
            self.ui.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(str(listoffile[name][1])))
            self.ui.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(str(listoffile[name][2])))
            self.ui.tableWidget.setRowHeight(i, 20)
            if not listoffile[name][1] :
                try :
                    self.radialAverage(self.fp + os.sep+ name)
                except:
                    print("unable to average on file :",name)
                
            i += 1
        #self.timer()
        self.listoffileVerif = glob.glob(os.path.join(self.fp, self.ext))#filetools.listFiles(self.fp,self.ext)
        self.listoffileVerif = listoffile
        if len(listoffile)>0:
            self.cellClicked(0,0)
            self.btnDisplayClicked()
        else:
            self.SelectedFile=None
            self.ui.labelSelectedFIle.setText("")
            self.ui.btnDisplaySelected.setEnabled(False)
            self.ui.btnDisplayAV.setEnabled(False)
        #print "list updated"

    def updateListInit(self):
        '''
        Update the initial List WITHOUT treatment 
        '''
        #print('generate list')
        
        #self.ext = str(self.ui.extensionTxt.text())
        #if self.ext == '':
        #      self.ext = '*.*'
        #listoffile=[]
        self.fp = os.path.normpath(str(self.ui.DirTxt.text()))
        try:
            listoffile,files=self.getList(self.fp)#get a dictionnary
        except:
            listoffile={}
            files=[]
            
        #    print('erreur %s'%self.fp)
        files=sorted(listoffile,reverse=True) #get a sorted list of the dictionnary
        #print(files)
        
        
        self.ui.tableWidget.setRowCount(len(listoffile))
        headerNames = ["File", "date", "processed", "new"]
        #if self.FROM_EXPERIMENT is not None:
        headerNames+=HEADER
        self.EXPORT_LIST=[headerNames]
        self.ui.tableWidget.setColumnCount(len(headerNames))
        self.ui.tableWidget.setHorizontalHeaderLabels(headerNames)
        self.ui.tableWidget.setColumnWidth(0, 220)
        self.ui.tableWidget.setColumnWidth(1, 150)
        self.ui.tableWidget.setColumnWidth(2, 70)
        self.ui.tableWidget.setColumnWidth(3,50)
        '''for n in range(len(FROM_EDF_HEADER)):
             self.ui.tableWidget.setColumnWidth(4+n,50)'''
        i = 0
        #print self.EXPORT_LIST
        ll=[]
        iconTrue=QtGui.QIcon(ICON_PATH+'check-mark-small.png')
        iconFalse=QtGui.QIcon(ICON_PATH+'error-icon-small.png')
        iconNew=QtGui.QIcon(ICON_PATH+'new.png')
        for name in files:
            ll=[name]+listoffile[name]
            self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(name))
            self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(listoffile[name][0])))#date
            #icon = QtGui.QIcon(QtGui.QPixmap("image_path"))
            
            '''item = QtGui.QTableWidgetItem(icon, "")        # Second argument
            >> (required !) is text
            >>         self.tableWidget.setItem(0, 0, item)
            '''
            if listoffile[name][1]:
                self.ui.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(iconTrue,""))
            else:
                self.ui.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(iconFalse,""))
            #self.ui.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(str(listoffile[name][1])))
            if listoffile[name][2]:
                self.ui.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(iconNew,""))
            else:
                self.ui.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(iconTrue,""))
            
            #self.ui.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(str(listoffile[name][2])))
            self.ui.tableWidget.setRowHeight(i, 20)          
            if HEADER is not None:
                #display information from edf
                
                infos=self.getInformationFromImage(name)
                for j in range(len(infos)):
                    self.ui.tableWidget.setItem(i, 4+j, QtWidgets.QTableWidgetItem(infos[j]))
                #print infos
                ll+=infos
            i += 1
            self.EXPORT_LIST.append(ll)
        #self.listoffileVerif = glob.glob(os.path.join(self.fp, self.ext))#filetools.listFiles(self.fp,self.ext)
        self.listoffileVerif = listoffile
        #display first
        try:
            if len(listoffile)>0:
                if self.ui.chkAutomaticDisplayFirst.isChecked():
                    #print 'display first'
                    self.cellClicked(0,0)
                    self.btnDisplayClicked()
                
                if self.ui.chkAutomaticAV.isChecked():
                    self.cellClicked(0,0)
                    self.btnDisplayClicked()
                    self.btnDisplayAVClicked()
            else:
                self.SelectedFile=None
                self.ui.labelSelectedFIle.setText("")
                self.ui.btnDisplaySelected.setEnabled(False)
                self.ui.btnDisplayAV.setEnabled(False)
            #print self.EXPORT_LIST
        except:
            pass
    def getfiles(self,dirpath):
        a = [s for s in os.listdir(dirpath)
             if os.path.isfile(os.path.join(dirpath, s))]
        a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
        return a
        
    def getList(self, fp):
        #print "getlist, ",fp
        #print os.path.join(self.fp, self.ext)
        #listoffile = glob.glob(os.path.abspath(self.fp)+os.sep+self.ext)#filetools.listFiles(fp, ext)
        listoffile=[]
        if self.fp=='':
            return []
        for file in os.listdir(self.fp):
            for ext in IMAGE_TYPE:
                if fnmatch.fnmatch(file,ext):
                    #print(file)
                    listoffile.append(os.path.abspath(self.fp)+os.sep+file)
        #listoffile.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
        #print "end glob : ",listoffile
        files = {}
        ttdict={}
        for name in listoffile:
            '''print(name)
            
            (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(name)
            print("last modified: %s" % time.ctime(mtime))
            '''
            fich = filetools.getFilename(name)
            try:
                dt = filetools.getModifiedDate(name)
            except:
                dt=None
            newfn = filetools.getFilenameOnly(name)
            try:
                tt=os.path.getmtime(os.path.join(self.fp, name))
            except:
                tt=None
            ttdict[tt]=fich
            ficTiff = newfn
            newfn += '.rgr'
            # print newfn
            if filetools.fileExist(newfn) :
                proc = True
                new = False
            else:              
                proc = False
                new = True
            files[fich] = [dt, proc, new,tt]    
        #print "end of getlist: ",files
        ttsorted=sorted(ttdict,reverse=True) #get a sorted list of the dictionnary
        #print(ttsorted)
        filessorted=[]
        for i in ttsorted:
            filessorted.append(ttdict[i])
        #print(filessorted)
        return files,filessorted
    
    
    def printTXT(self, txt="", par=""):
        '''
        for printing messages
        '''
        if self.printout == None:
            print((str(txt) + str(par)))
        else:
            self.printout(txt, par)

    def radialPrepare(self):
        #print('radial prepare')
        self.fai = FAIsaxs.FAIsaxs()
        filename = self.ui.paramTxt.text()
        #print(filename)
        if not os.path.exists(filename):
            self.printTXT(filename + ' does not exist')
            return
        outputdir = self.ui.DirTxt.text()
        self.fai.setGeometry(filename)
        print('set geometry')
        print('maskfile : '+self.fai.getMaskFilename())
        '''self.qDiv = self.fai.getProperty('user.qDiv')
        if self.qDiv is None:
            self.qDiv = 1000'''
        try:
            self.mad = self.fai.getIJMask()
            self.ui.maskvalid.setPixmap(self.pixmapValid)
            #print('get ij mask')
        except:
            print('problem mask not found')
            self.mad=None
            self.ui.maskvalid.setPixmap(self.pixmapExcl)
        maskfilename = self.fai.getMaskFilename()
  
    def radialAverage(self, imageFilename,plotRefresh=True):
        if self.fai is None :
            self.radialPrepare()
        t0=time()
        '''im = fabio.open(imageFilename)
        #try:
        SAXSparametersXML.saveImageHeader(im.header,imageFilename)
        self.printTXT("Header file saved")
        #except :
        #        self.printTXT("Error on Header file saving")
        newname = filetools.getFilenameOnly(imageFilename) + ".rgr"
        qtemp, itemp, stemp = self.fai.integrate1d(im.data, self.qDiv, filename=newname, mask=self.mad, error_model="poisson")
        print time()-t0, " s"
        '''
        im,q,i,s,newname=self.fai.integratePySaxs(imageFilename, self.mad, self.printTXT)#, self.qDiv)
        self.fai.saveGeometry(imageFilename)#save rpt
        if im is None:
            return
        #try:
            
        self.OnClickPlotCheckBox()
        if self.parent is None:
            #if pySaxs windows exist
            self.plotapp.addData(q, i, label=imageFilename)#,error=s)
            self.plotapp.replot()
        else:
            myname=filetools.getFilename(imageFilename)
            if 'Comment' in im.header:
                    comment=im.header['Comment']
                    if comment !='' :
                        myname+="-"+comment
            #color management
            col=None
            if myname in self.parent.data_dict:
                col=self.parent.data_dict[myname].color#keep the color from parent
            else :
                col=pySaxsColors.pySaxsColors().getColor(len(self.parent.data_dict)) #get a new color
            #create new datas
            self.parent.data_dict[myname]=dataset.dataset(myname,q,i, imageFilename,error=s,type='saxs',image="Image",color=col)
            if plotRefresh: 
                self.parent.redrawTheList()
            #automatic Plot
            '''if plotRefresh: 
                if self.ui.plotChkBox.isChecked():
                    self.parent.Replot()
            '''
            self.parent.Replot()
            #automatic absolute I
            if self.ui.chkAutomaticAbsolute.isChecked():
                #print("-------------------hello")
                
                param=dlgAbsoluteI.getTheParameters(myname, self.parent, self.workingdirectory) #get the param
                #print(param)
                #print(myname)
                #print(type(param))
                if param is not None:
                    param.calculate_All()
                    if self.ui.chkSubSolvent.isChecked():
                        referencedata=self.parent.referencedata
                    else:
                        referencedata=None
                    #get the thickness
                    try:
                        thickness=float(self.ui.thicknessEdit.text())
                    except:
                        thickness=None
                    #get the background
                    try:
                        background_by_s=float(self.ui.backgdEdit.text())   
                    except:
                        background_by_s=None
                    newname_scaled=dlgAbsoluteI.OnScalingSAXSApply(self.parent, dataname=myname, parameters=param.parameters,\
                                                                   referencedata=referencedata,thickness=thickness,\
                                                                   background_by_s=background_by_s)#, backgroundname, referencedata)
                    self.parent.data_dict[myname].parameters=param
                    self.parent.data_dict[myname].checked=False
                    myname= newname_scaled
                else:
                    print("not found")
                if plotRefresh:
                    self.parent.redrawTheList()
                    self.parent.Replot()
            self.lastDatas=myname
            #automatic saving
            if plotRefresh:
                if self.ui.chkAutomaticSaving.isChecked():
                    if self.parent.DatasetFilename!="":
                        self.parent.OnFileSave()   
        #except:
        #    print "Error plot"
    
    def btnProcessALLClicked(self):
        #Process all files in the list
        st=self.ui.chkAutomaticAV.isChecked()
        self.ui.chkAutomaticAV.setChecked(False)
        if AUTOMATIC_FIT:
            self.automaticFitApp.clearResult()
        #get the list
        #ll=[]
        n=self.ui.tableWidget.rowCount()
        self.ui.progressBar.setMaximum(n)
        for row in range(0,n):
            #ll.append()
            name=str(self.ui.tableWidget.item(row,0).text())
            name=self.workingdirectory+os.sep+name
            self.radialAverage(name,plotRefresh=False)
            self.ui.progressBar.setValue(row)
            if AUTOMATIC_FIT:
                self.btnDisplayAutomaticFitClicked()
                QtTest.QTest.qWait(500)
        #print("LIST : " ,ll)
        #uncheck some box
        
        #process
        
            
        self.radialAverage(name,plotRefresh=True)
        self.ui.progressBar.setValue(0)
        self.ui.chkAutomaticAV.setChecked(st)
        
    def btnProcessSelectionClicked(self):
         #Process all files in the list
        st=self.ui.chkAutomaticAV.isChecked()
        self.ui.chkAutomaticAV.setChecked(False)
        if AUTOMATIC_FIT:
            self.automaticFitApp.clearResult()
        #get the list
        #ll=[]
        n=self.ui.tableWidget.rowCount()
        self.ui.progressBar.setMaximum(n)
        #print(list(self.ui.tableWidget.selectedIndexes()))
        for item in self.ui.tableWidget.selectedIndexes():
            #ll.append()
            row=item.row()
            name=str(self.ui.tableWidget.item(row,0).text())
            #print(name)
            name=self.workingdirectory+os.sep+name
            self.radialAverage(name,plotRefresh=False)
            #self.ui.progressBar.setValue(row)
            if AUTOMATIC_FIT:
                self.btnDisplayAutomaticFitClicked()
                QtTest.QTest.qWait(500)
                
        #process last
        self.radialAverage(name,plotRefresh=True)
        self.ui.progressBar.setValue(0)
        self.ui.chkAutomaticAV.setChecked(st)
        
            
    def OnClickPlotCheckBox(self):
        pass
        '''if self.parent is None:
            if self.ui.plotChkBox.isChecked():
                self.plotapp=QtMatplotlib.QtMatplotlib()
                self.plotapp.show()
            else:
                self.plotapp.close()'''
    
    def OnClickDisplayBeam(self):
        '''
        user clicked on display beam
        '''
        #print "chk"
        #--simply redraw the image
        self.btnDisplayClicked()

    def OnClickparamViewButton(self):
        filename=str(self.ui.paramTxt.text())
        if filename is not None and filename !='':
            self.dlgFAI=dlgQtFAITest.FAIDialogTest(self.parent,filename,None,feedback=self.feedbackFromView)
            self.dlgFAI.show()

    def feedbackFromView(self,filename=None):
        if filename is not None:
            ret=QtWidgets.QMessageBox.question(self, "pySAXS", "Apply parameter file %s ?"%filename,
                                              buttons=QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No,
                                              defaultButton=QtWidgets.QMessageBox.Yes)
            if ret==QtWidgets.QMessageBox.Yes:
                self.ui.paramTxt.setText(filename)
                self.OnClickButtonTransferParams()

    def getInformationFromImage(self,filename):
        '''
        get the information from image
        (header if EDF, or rpt file if TIFF)
        '''
        d=self.ui.DirTxt.text()
        filename=self.workingdirectory+os.sep+filename
        
        try:
            im=fabio.open(filename)
        except:
            #file not exist
            return []
        l=[]
        #get extension
        EXTE=filetools.getExtension(filename).lower()
        if EXTE=='edf':
            #EDF type file
            for n in FROM_EDF:
                try:
                    l.append(str(im.header[n])) 
                except:
                    l.append("?")
        else:
            l=[]
            #print('#no information in edf')
        #OTHER (datas in RPT)
        #try to read the rpt ?
        #l=[]
        #print('try to read rpt')

        rpt=configparser.ConfigParser()
        txt="?"
        filenameRPT=filetools.getFilenameOnly(filename)+'.rpt'
        if not(filetools.fileExist(filenameRPT)):
            #no rpt
            #print("no rpt")
            return l
        test=rpt.read(filenameRPT)
        if len(test)==0:
                print('error when reading file :', filenameRPT)
                return l
            
        lrpt=[]
        for n in FROM_RPT:
                try:
                    #print(n)
                    lrpt.append(str(rpt.get('acquisition',n)))
                    #print(str(rpt.get('acquisition',n)))
                except:
                    lrpt.append("?")
        if len(l)==0:
            return lrpt
        #try to merge l and lrpt
        for n in range(len(l)):
            if l[n]=='?':
                l[n]=lrpt[n]
        return l

    def OnClickCenterOfMassButton(self):
        '''
        calculate the center of mass
        '''
        #self.axes.set_xlim((self.xlim_min,self.xlim_max))
        #self.axes.set_ylim((self.ylim_min,self.ylim_max))
        plt=self.ui.matplotlibwidget
        xlim_min,xlim_max=plt.axes.get_xlim()
        ylim_max,ylim_min=plt.axes.get_ylim()
        im=self.img.data[int(ylim_min):int(ylim_max),int(xlim_min):int(xlim_max)]
        #print int(self.ylim_min),int(self.ylim_max),int(self.xlim_min),int(self.xlim_max)
        CenterOM=ndimage.measurements.center_of_mass(im)#, labels, index)
        #print CenterOM[0]+ylim_min,CenterOM[1]+xlim_min
        
        self.ui.chkDisplayBeam.setChecked(True)
        self.ui.edtBeamX.setText("%6.2f"%(CenterOM[1]+xlim_min))
        self.ui.edtBeamY.setText("%6.2f"%(CenterOM[0]+ylim_min))
        self.btnDisplayClicked()
        
        
    def OnClickExportList(self):
        '''
        export the list
        '''
        #print "toto"
        fd = QtWidgets.QFileDialog(self)
        filename,ext = fd.getSaveFileName(self,"export list",directory=self.workingdirectory,\
                                      filter="Text files(*.txt);;All files (*.*)")
        #self.workingdirectory = filename
        #print(filename)
        if filename:
            #save
            f=open(filename,'w')
            for row in self.EXPORT_LIST:
                tt=""
                for n in row:
                    tt+=str(n)+'\t'
                #print(tt)
                f.write(tt+"\n")
            f.close()
            #print filename, " saved"
    
    def btnDisplayAutomaticFitClicked(self):
        self.automaticFitApp.tryFitThis(self.lastDatas)
        
    def btnCheckSolventClicked(self):
        if self.parent.referencedata is not None:
                self.ui.solventEdit.setText(str(self.parent.referencedata))
        
    
    def closeEvent(self, event):
        '''
        when window is closed
        '''
        l=self._fileSysWatcher.directories()
        #print "previous watched directories :",list(l)
        self._fileSysWatcher.removePaths(l)
        
        #print "close"
        #save the preferences
        if self.parent is not None:
                #self.parent.pref.set("outputdir",section="pyFAI",value=str(self.ui.outputDirTxt.text()))
                self.pref.set("parameterfile",section="pyFAI",value=str(self.ui.paramTxt.text()))
                self.pref.set('defaultdirectory',section="guisaxs qt",value=str(self.ui.DirTxt.text()))
                self.pref.set('fileextension',section="pyFAI",value=str(self.ui.extensionTxt.text()))
                self.pref.save()
        try:
            self.t.stop()
            
        except:
            pass

class Intervallometre(threading.Thread):
 
    def __init__(self, duree, fonction, parent=None):
        threading.Thread.__init__(self)
        self.duree = duree
        self.fonction = fonction
        self.parent = parent
        self.encore = True
        
    def run(self):
        print('start')
        while self.encore:
            #self.fonction()
            self.parent.updateList()
            self.slip(self.duree)
            '''if self.parent is not None:
                try:
                    val=self.parent.ui.progressBar.value()
                    if val+10>self.parent.ui.progressBar.maximum():
                        self.parent.ui.progressBar.setValue(0)
                    else:
                        self.parent.ui.progressBar.setValue(val+10)
                except:
                    pass'''
    def stop(self):
        self.encore = False
        
    def slip(self,t,intt=1.0):
        if t<intt:
            sleep(t)
            return
        t0=time()
        #print t0,time()-t0
        #self.parent.ui.progressBar.setMaximum(t)
        while t-(time()-t0)>intt:
            #print("+", end=' ')
            #self.parent.ui.progressBar.setValue(t-(time()-t0))
            if self.encore:
                sleep(intt)
                ''''if self.parent is not None:
                    try:
                        val=self.parent.ui.progressBar.value()
                        if val+10>self.parent.ui.progressBar.maximum():
                            self.parent.ui.progressBar.setValue(0)
                        else:
                            self.parent.ui.progressBar.setValue(val+10)
                    except:
                        pass'''
            else:
                return
        sleep(t-(time()-t0))
        
        
        
        
if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  myapp = SurveyorDialog()
  myapp.show()
  sys.exit(app.exec_())
  
