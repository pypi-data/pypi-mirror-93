from pyFAI import geometry
from pyFAI import azimuthalIntegrator
from pySAXS.tools.isNumeric import *
from pySAXS.tools import filetools
from  pySAXS.LS import SAXSparametersXML
import os
import numpy
import fabio
import sys
if sys.version_info.major>=3:
    import configparser 
else:
    import ConfigParser as configparser
import pySAXS


class FAIsaxs(azimuthalIntegrator.AzimuthalIntegrator):
    
    _xmldirectory={}
    
    def importIJxml(self,filename):
        '''
        import a dictionary object from ImageJ SAXS plugins xml file
        '''
        from xml.etree import ElementTree
        element=ElementTree.parse(filename)
        root=element.getroot()
        self._xmldirectory={}
        if root.tag!='ImageJprefs':
                raise RuntimeWarning("no ImageJ preference in this file !")
                return         
        for sube in root[0]:
            tag=sube.tag
            self._xmldirectory[tag]=sube.text
            if isNumeric(sube.text):
                    self._xmldirectory[tag]=float(sube.text)
        return 

    def setGeometry(self,filename=None):
        '''
        apply a geometry object from ImageJ SAXS dictionary
        '''
        #print("apply a geometry from IJ file")
        if filename is not None:
            self.importIJxml(filename)
        #g=geometry.Geometry()
        #print('open XML')
        centerX=self._xmldirectory['user.centerx']
        centerY=self._xmldirectory['user.centery']
        dd=self._xmldirectory['user.DetectorDistance']*10 #m->cm
        tilt=self._xmldirectory['user.alpha_deg']
        #print(tilt)
        if abs(float(tilt))>70.0:
            #comes from ImageJ plugin
            tilt=90-tilt
        '''if 'user.pyfai_tilt' in self._xmldirectory:
            tilt=self._xmldirectory['user.pyfai_tilt']'''
        if 'user.pyfai_tiltPlanRotation' in self._xmldirectory:
            tiltPlanRotation = self._xmldirectory['user.pyfai_tiltPlanRotation']
        else:
            tiltPlanRotation=0
        pixelX=self._xmldirectory['user.PixelSize']*1e4 #m->micron
        pixelY=pixelX
        wavelength=self._xmldirectory['user.wavelength']
        self.set_wavelength(wavelength*1e-10)
        self.setFit2D(dd,centerX=centerX,centerY=centerY,tilt=tilt,pixelX=pixelX,\
                      pixelY=pixelY,tiltPlanRotation=tiltPlanRotation)
        #print(self)
        #return g
    
    def saveGeometry(self,filename=None):
        '''
        save geometry parameters in filename.rpt
        if filename exist, append
        '''
        #import configparser
        rpt=configparser.ConfigParser()   
        #check if there is a associated rpt file
        newfn=filetools.getFilenameOnly(filename)
        newfn+='.rpt'
        try:
            r=rpt.read(newfn) #if r=[] rpt doesn't exist
            
            if not rpt.has_section('pyfai'):
                rpt.add_section('pyfai')
            rpt.set('pyfai','imagej.centerx',str(self._xmldirectory['user.centerx']))
            rpt.set('pyfai','imagej.centery',str(self._xmldirectory['user.centery']))
            rpt.set('pyfai',"imagej.DetectorDistance",str(self._xmldirectory['user.DetectorDistance']))
            rpt.set('pyfai',"imagej.alpha_deg",str(self._xmldirectory['user.alpha_deg']))
            rpt.set('pyfai',"imagej.PixelSize",str(self._xmldirectory['user.PixelSize']))
            rpt.set('pyfai',"imagej.wavelength",str(self._xmldirectory['user.wavelength']))
            rpt.set('pyfai',"imagej.MaskImageName",str(self._xmldirectory['user.MaskImageName']))
            rpt.set('pyfai',"imagej.qDiv",str(self._xmldirectory['user.QDiv']))
            f=open(newfn,'w')
            rpt.write(f)
            f.close()
            #print("write RPT",newfn)
        except:
            print('unable to write rpt file :',newfn)
        
    
    def saveGeometryRPT(self,filename,maskname=None,qdiv=None):
        '''
        save geometry as rpt file
        '''
        #import configparser
        rpt=configparser.ConfigParser()   
        #check if there is a associated rpt file
        newfn=filetools.getFilenameOnly(filename)
        newfn+='.rpt'
        r=rpt.read(newfn) #if r=[] rpt doesn't exist
        
        
        if not rpt.has_section('pyfai'):
            rpt.add_section('pyfai')
        
        
        out=self.getFit2D()
        rpt.set('pyfai','pyfai.centerx',str(out['centerX']))
        rpt.set('pyfai','pyfai.centery',str(out['centerY']))
        rpt.set('pyfai',"pyfai.DetectorDistance",str(out['directDist']/10))
        rpt.set('pyfai',"pyfai.alpha_deg",str(90-out['tilt']))
        rpt.set('pyfai',"pyfai.PixelSize",str(out['pixelX']/10000))
        rpt.set('pyfai',"pyfai.wavelength",str(self.get_wavelength()*1e9))
        if maskname is None:
            try:
                rpt.set('pyfai',"pyfai.MaskImageName",str(self._xmldirectory['user.MaskImageName']))
            except:
                pass
        else:
            rpt.set('pyfai',"pyfai.MaskImageName",str(maskname))
        if qdiv is None:
            try:
                rpt.set('pyfai',"pyfai.qDiv",str(self._xmldirectory['user.QDiv']))
            except:
                pass
        else:
            rpt.set('pyfai',"pyfai.qDiv",str(qdiv))
            
        f=open(newfn,'w')
        rpt.write(f)
        f.close()
        #print("write RPT",newfn)
    
    def saveGeometryOLD(self,filename=None):
        '''
        save geometry parameters in filename.rpt
        if filename exist, append
        '''
        #check if there is a associated rpt file
        newfn=filetools.getFilenameOnly(filename)
        newfn+='.rpt'
        #print newfn
        if filetools.fileExist(newfn):
            f=open(newfn,mode="a")
        else:
            f=open(newfn,mode='w')
        try:
            f.write("\n")
            f.write("#user.centerx="+str(self._xmldirectory['user.centerx'])+'\n')
            f.write("#user.centery="+str(self._xmldirectory['user.centery'])+'\n')
            f.write("#user.DetectorDistance="+str(self._xmldirectory['user.DetectorDistance'])+'\n')
            f.write("#user.alpha_deg="+str(self._xmldirectory['user.alpha_deg'])+'\n')
            f.write("#user.PixelSize="+str(self._xmldirectory['user.PixelSize'])+'\n')
            f.write("#user.wavelength="+str(self._xmldirectory['user.wavelength'])+'\n')
            f.write("#user.MaskImageName="+str(self._xmldirectory['user.MaskImageName'])+'\n')
            f.write("#user.qDiv="+str(self._xmldirectory['user.qDiv'])+'\n')
        except:
            pass
        f.close()
    
    def getIJMask(self,maskfilename=None):
        '''
        return a image from ImageJ mask defined in d (from xml)
        '''
        if maskfilename is None:
            if 'user.MaskImageName' in self._xmldirectory:
                maskfilename=self._xmldirectory['user.MaskImageName']
            else:
                raise RuntimeWarning("no mask defined")
        self._xmldirectory['user.MaskImageName']=maskfilename
        print('open mask')
        ma=fabio.open(maskfilename)
        mad=ma.data
        mad=mad.astype(bool)
        #mad=numpy.invert(mad)
        return mad

    
    def getMaskFilename(self):
        '''
        return mask filename
        '''
        return self.getProperty('user.MaskImageName')
        
    
    def getProperty(self,property):
        if property in self._xmldirectory:
            return self._xmldirectory[property]
        else:
            return None
        
    def saveGeometryXML(self,filename,centerx,centery,detectordistance,alpha,pixelsize,wavelength,maskfile,\
                        qdiv,tiltPlanRotation=None,tiltPyFAI=None):
        f=open(filename,'w')
        f.write("<ImageJprefs><user>")
        f.write('<user.centerx>'+str(centerx)+'</user.centerx>')
        f.write('<user.centery>'+str(centery)+'</user.centery>')
        f.write('<user.PixelSize>'+str(pixelsize)+'</user.PixelSize>')
        f.write('<user.wavelength>'+str(wavelength)+'</user.wavelength>')
        f.write('<user.DetectorDistance>'+str(detectordistance)+'</user.DetectorDistance>')
        f.write('<user.alpha_deg>'+str(alpha)+'</user.alpha_deg>')
        f.write('<user.QDiv>'+str(qdiv)+'</user.QDiv>')
        f.write('<user.MaskImageName>'+maskfile+'</user.MaskImageName>')
        if tiltPlanRotation is not None:
            f.write('<user.pyfai_tiltPlanRotation>' + str(tiltPlanRotation) + '</user.pyfai_tiltPlanRotation>')
        if tiltPyFAI is not None:
            f.write('<user.pyfai_tiltPyFAI>' + str(tiltPyFAI) + '</user.pyfai_tiltPyFAI>')

        f.write('</user></ImageJprefs>')
        f.close()
    
    def integratePySaxs(self,imageFilename,mad,printTXT,outputdir=None,qDiv=None):
        '''
        for integration in pySAXS
        '''
        
        if qDiv is None:
            qDiv=self.getProperty('user.QDiv')
        if qDiv is None:
            qDiv=1000
        #manage filename
        name=filetools.getFilename(filetools.getFilenameOnly(imageFilename))
        if outputdir is not None :
            newname=outputdir+os.sep+name+".rgr"
        else:
            newname=filetools.getFilenameOnly(imageFilename) + ".rgr"
        #-- opening data
        
        try:
            im=fabio.open(imageFilename)
        except:
            printTXT('error in opening ',imageFilename)
            im=None
        if im is not None:
            printTXT(imageFilename+' opened')
            try:
                SAXSparametersXML.saveImageHeader(im.header,imageFilename)
                printTXT("Header file saved")
            except :
                printTXT("Error on Header file saving")
                
            #print numpy.shape(im.data)
            qDiv=int(qDiv)
            qtemp,itemp,stemp=self.integrate1d(im.data,qDiv,filename=newname,mask=mad,error_model="poisson",unit="q_A^-1",)
            q=qtemp
            i=itemp
            s=stemp
            q=qtemp[numpy.nonzero(itemp)]
            i=itemp[numpy.nonzero(itemp)]
            s=stemp[numpy.nonzero(itemp)]
            '''isnotNan=numpy.where(~numpy.isnan(s))
            s=s[isnotNan]
            q=q[isnotNan]
            i=i[isnotNan]
            '''
            self.saveGeometry(imageFilename)#save rpt
        return im, q,i,s,newname
        