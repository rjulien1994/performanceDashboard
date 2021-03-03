from module.component import *
import psutil
import GPUtil
import platform
import urllib.request
import numpy as np

class cpu(component):  #We create cpu as a class as one could track multiple cpus by changing reference
    def __init__(self, reference=psutil,refreshRate=4, name=False):
        component.__init__(self, name if name else self.getName(), reference, refreshRate) #call component constructor
        
        self.addAtt('coresLoad', lambda: np.array([p for c, p in enumerate(self.ref.cpu_percent(percpu=True, interval=None))])) 
        self.addAtt('load', lambda: self.ref.cpu_percent())
        self.addAtt('frequency', lambda: self.ref.cpu_freq().current)   #We add the methods and states of the cpu
              
    def getName(self):   #For cpu if no name given we can fetch the model
        try:             #Inheritance allows adding or overridding methods of the parent class
            cpuModel = platform.processor()
            form = {' Family': ':',' Model ': '.',' Stepping ': '.'}
            for key, tr in form.items():
                cpuModel = cpuModel.replace(key, tr)
            return cpuModel[:cpuModel.index(',')]
        except:
            return 'CPU'


class gpu(component): #We can easily att anyNumber of attributes to an object and it doesn't have to use reference
    def __init__(self, reference=lambda: GPUtil.getGPUs()[0], refreshRate=0.5):
        component.__init__(self, reference().name, reference, refreshRate)
        
        self.addAtt('size', lambda: self.ref().memoryTotal*1024*1024, noRefresh=True)
        self.addAtt('temperature', lambda: self.ref().temperature)
        self.addAtt('used', lambda: self.ref().memoryUsed*1024*1024)
        self.addAtt('load', lambda: self.ref().load*100)
        self.addAtt('memLoad', lambda: 100*self('used')/self('size'))
        #Althought it is the info that interested me the most it is quiet cpu heavy



class network(component): #For integrity it is better that each att only return a single value
    def __init__(self, reference=psutil.net_io_counters, name="Network", refreshRate=4):
        component.__init__(self, name, reference, refreshRate)
        
        self.addAtt('localIP', lambda: psutil.net_if_addrs()["Ethernet"][1].address, noRefresh=True)
        self.addAtt('publicIP', lambda: urllib.request.urlopen('https://ident.me').read().decode('utf8'), noRefresh=True)
        self.addAtt('downRate', lambda dt=1: (self.ref().bytes_recv - (self('downTotal') if self('downTotal')!=None else 0))/dt, delta=True)
        self.addAtt('upRate', lambda dt=1: (self.ref().bytes_sent - (self('upTotal') if self('upTotal') else 0))/dt, delta=True)
        self.addAtt('downTotal', lambda: self.ref().bytes_recv)
        self.addAtt('upTotal', lambda: self.ref().bytes_sent)



class memory(component): #memory can be SSD, HHD, RAM or cloud
    def __init__(self, reference, name, refreshRate=1):
        component.__init__(self, name, reference, refreshRate)
        
        self.addAtt('size', lambda: self.ref().total, noRefresh=True)
        self.addAtt('used', lambda: self.ref().used)
        self.addAtt('load', lambda: 100*self('used')/self('size'))



