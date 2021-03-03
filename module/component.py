import time

class component(object): #create a base class with min req attributes and methods
    def __init__(self, name, reference, rate=1):
        self.name = name #each component will have a name and a ref to fetch data
        self.ref = reference
        
        self.timeStamp = time.time()  #to keep track of updates
        self.refreshRate = rate
        
        self.info = {'name': [lambda: self.name, self.name, False, True]} #Dict to return info on component (could be a switch instead)
        
    def __call__(self, att='name'): #make the obj callable
        return self.info[att][1]
    
    def addAtt(self, att, f, delta=False, noRefresh=False): #So that sub class can add attributes to call function
        try:
            self.info[att] = [f, f(), delta, noRefresh] #method, state, dt, refresh
        except:
            self.info[att] = [f, 0, delta, noRefresh] 
            
    def getAtts(self):  #return list of callable attributes currently in component
        return list(self.info.keys())
    
    def refresh(self): #checks if time to refresh class info
        if 1/self.refreshRate < time.time()-self.timeStamp:
            t = self.timeStamp
            self.timeStamp = time.time()
            return self.timeStamp - t
        return False
    
    def update(self):         #We use the method to update state regularly
        dt = self.refresh()   #We can now update and fetch state separatly
        if dt:
            for att, val in self.info.items():
                if val[3]:
                    continue
                if val[2]:
                    self.info[att][1] = (val[0](dt) + self.info[att][1])/2
                else:
                    self.info[att][1] = (val[0]() + self.info[att][1])/2 #reduce damping