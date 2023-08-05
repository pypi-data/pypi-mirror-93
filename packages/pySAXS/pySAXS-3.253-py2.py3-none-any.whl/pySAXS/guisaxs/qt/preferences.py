'''
a module to manage preference
'''
import sys
if sys.version_info.major>=3:
    import configparser 
else:
    import ConfigParser as configparser

from os import path
from os.path import expanduser
import os
'''
[guisaxs qt]
defaultdirectory : qlksjdqlksd
recent : qdsqdjqkls
'''


KEYS=['defaultdirectory','recent']
SECTION='guisaxs qt'
MEMORY=5

class prefs():
    
    def __init__(self,filename='guisaxs.ini',section=None):
        self.filename=home = expanduser("~")+os.sep+filename #by default search in user home
        if section is None:
            self.section=SECTION
        else:
            self.section=section
        #populate dict wth empty values
        self.parser = configparser.SafeConfigParser()
        self.parser.add_section(self.section)
        for name in KEYS:
            self.parser.set(self.section,name,'')
        
        self.recent=[] #keep in memory the x last files
    
    def getName(self):
        return self.filename
    
    def fileExist(self,filename=None):
        '''
        return True if preference file exist
        '''
        if filename is not None:
            #change filename
            self.filename=filename
        return path.exists(self.filename)
    
    def save(self,filename=None):
        '''
        save preferences in filename
        '''
        #print("save pref in : ",filename)
        if filename is not None:
            #change filename
            self.filename=filename
        f=open(self.filename,'w')
        print("save pref in : ",path.abspath(self.filename))   
        self.parser.write(f)
        f.close()
        #cfgfile.close()
    
    def read(self,filename=None):
        '''
        read preferences from filename
        '''
        #print("read preferences")
        if filename is not None:
            #change filename
            self.filename=filename
        self.parser = configparser.SafeConfigParser()
        print("read pref in : ",path.abspath(self.filename))   
        self.parser.read(self.filename)
        rec=self.get('recent')
        #print rec
        self.recent=[]
        if rec is not None: #old recent management
            rec=rec.replace("'",'')
            rec=rec.replace(" ",'')
            rec=rec.split(',')
            #print rec
            for f in rec:
                if f!='':
                    self.recent.append(path.normpath(f))#normalize path
        #new recent management
        for i in range(MEMORY):
            rec=self.get('recent'+str(i))
            if rec is None:
                break
            self.recent.append(path.normpath(rec))

    def get(self,name,section=None,defaultValue=None):
        '''
        get the specified preferences
        if the key name don't exist, return None
        '''
        if section is None:
            section=self.section
        if self.parser.has_option(section,name):
            return self.parser.get(section, name)
        else:
            if defaultValue is not None:
                return defaultvalue
            else:
                return None
    def getSet(self,name,section=None,defaultValue=None):
        '''
        get the specified preferences
        if the key name don't exist, return None
        '''
        if section is None:
            section=self.section
        if self.parser.has_option(section,name):
            return self.parser.get(section, name)
        else:
            if defaultValue is not None:
                #pref doesn't exist
                if not self.parser.has_section(section):
                    self.parser.add_section(section)
                    self.parser.set(section, name, str(defaultValue))
                return defaultValue
            else:
                return None
    
    def set(self,name,value,section=None):
        '''
        set the preference
        '''
        if section is None:
            section=self.section
        #print "set prefs : ",name,value,section
        if not self.parser.has_section(section):
            self.parser.add_section(section)
            
        self.parser.set(section, name, value)
        
    def getRecentFiles(self):
        '''
        return the list of recent files
        '''
        return self.recent
    
    def getLastFile(self):
        if len(self.recent)>0:
            return self.recent[0]
        else:
            return None

    def addRecentFile(self,filename):
        '''
        add a recent file
        '''
        #print filename
        filename=path.normpath(filename)
        if filename in self.recent:
            #already in recent
            return False
        #print filename
        #print self.recent
        nl=[filename]
        self.recent=nl+self.recent[:MEMORY-1]
        '''print self.recent
        st=str(self.recent)
        st=st.strip('[]\'')
        st=st.replace("'",'')
        print st'''
        #self.set('recent',st)
        #new recent management
        for i in range(len(self.recent)):
            self.set('recent'+str(i),self.recent[i])
        
        return True
        