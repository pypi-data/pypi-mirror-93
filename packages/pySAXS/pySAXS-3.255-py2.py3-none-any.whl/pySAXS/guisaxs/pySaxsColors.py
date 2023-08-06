from matplotlib import colors
import random
#import numpy

'''
module for matplotlib colors
'''
BASIC_COLORS=['#1f77b4', '#d62728','#ff7f0e', '#2ca02c',   \
              'm','#0000ff','#17becf','#00ff00','#ff00ff',\
              '#8c564b',  'goldenrod','#0080ff', \
              '#00ffff','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf',\
              '#ff007f','g','#808080','#990000','#994c00','#999900',\
              '#4c0099','#990099']
def rgb2luminance(r,g,b):
        return (0.2126*r) + (0.7152*g) + (0.0722*b)

def name2luminance(name):
    cc=colors.ColorConverter()
    rgb=cc.to_rgb(name)
    return rgb2luminance(rgb[0],rgb[1],rgb[2])

def listOfColors():
    '''
    return the RGB list of colors  with luminance <=0.4
    '''
    k=list(colors.cnames.keys())
    l=[]
    for name in k:
        #print name,
        if name2luminance(name)<=.4:
            #print "append ", name
            #l.append(name)
            l.append(colors.cnames[name])
    #l.sort()
    return l

def listOfColorsNames():
    '''
    return the list of colors NAMES with luminance <=0.4
    '''
    k=list(colors.cnames.keys())
    l=[]
    for name in k:
        #print name,
        if name2luminance(name)<=.4:
            #print "append ", name
            #l.append(name)
            l.append(name)
    #l.sort()
    return l

def listOfColorsDict():
    k=list(colors.cnames.keys())
    d={}
    for name in k:
        #print name,
        if name2luminance(name)<=.4:
            d[name]=colors.cnames[name]
    return d

def getColorRGB(name):
    if name in colors.cnames:
        return colors.cnames[name]
    else:
        return colors.cnames['black']
    
    
class pySaxsColors():
    
    def __init__(self):
        self.rgbColorsList=BASIC_COLORS
        self.nameColorList=[]
        self.colorDict={}
        self.n=-1#random.randint(0,len(self.rgbColorsList)-1)
        
        ''''k=colors.cnames.keys()
        for name in k:
            #print name,
            if name2luminance(name)<=.4:
                #print "append ", name
                #l.append(name)
                self.rgbColorsList.append(colors.cnames[name])#rgb code
                self.nameColorList.append(name)#name
                self.colorDict[name]=colors.cnames[name]'''
        
    def getColor(self,n=None):
        '''
        return a color name from the list of colors
        if n> length of list of colors, return at the beginning
        if n is None, return a random colors from the list
        '''
        
        if n is None:
            n=self.n+1#random.randint(0,len(self.rgbColorsList)-1)
            self.n=n
           
        t=divmod(n,len(self.rgbColorsList)) #return the no of color in the list
        #print self.rgbColorsList[t[1]]
       
        return self.rgbColorsList[t[1]]
    
if __name__ == "__main__":
    import sys
    from matplotlib import pyplot
    #if sys.version_info.major>=3:
    from pySAXS.guisaxs import pySaxsColors
    #else :
    #    import pySaxsColors
    pyC=pySaxsColors.pySaxsColors()
      
    pyplot.figure(figsize=(10,6))
    ax = pyplot.axes()
    # Setting the background color
    ax.set_facecolor("#EBEBF2")

    from numpy import *
    x=arange(-10,10,0.1)
    y=sin(x)
    for i in range(len(BASIC_COLORS)):
        y=y+0.2
        c=BASIC_COLORS[i]#pyC.getColor()
        
        pyplot.plot(x, y,color=c, label=str(c))
    #pyplot.rcParams['axes.facecolor']="#EBEBF2"
    #pyplot.set_facecolor()
    pyplot.legend()
    pyplot.show()
