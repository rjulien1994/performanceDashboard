from module.icon import *
from PIL import ImageFilter
import time

class meterIcon(icon):
    def __init__(self, size, name, units='%', labels=[0,50,100], rotRange=[7*math.pi/4, math.pi/4], outline=True, color=(255,0,0),fontColor=False, labelColor=False, subLabel=False):
        icon.__init__(self, name, size, color)   #create basic icon
           
        self.rotRange = rotRange                 #speed meters rotate
        
        self.labelColor = labelColor if labelColor else [self.color]*len(labels) #list for color per dent
        self.fontColor = fontColor if fontColor else self.color
        
        self.labels = labels #stored as attributes in case of dynamic bk change
        self.outline = outline
        self.units = units
        self.subLabel = subLabel if subLabel else 0
        
        #This icon only has 2 elements, a unmovable bk and a rotating indicator
        self.bk = self.makeBK()   #initiate state of meter
        self.indicator = self.makeIndicator()#self, radius=40, color=self.color
        
        
        self.pastA = None
        self.direction = 1 if self.rotRange[1]-self.rotRange[0]>0 else -1
        self.timeStamp = time.time()
        self.display = self.indicator.rotate(180*rotRange[0]/math.pi)
    
    def makeBK(self): 
        #We create the markings and title
        meter = self.addLayers(self.makeTitle(), self.makeLabel(self.labels))
        
        if self.outline:   #We add the outline if required
            meter = self.addLayers(meter, self.drawCircle(center=[50,50], r1=45, r2=50, color=self.color, steps=10))
            meter = self.addLayers(meter, self.drawCircle(center=[50,50], r1=0, r2=9, color=self.color, steps=10))
            
        return meter
        
    def makeLabel(self, labels, numSub=False, colors=False, opacity=230):
        img = self.newFilter()
        colors = colors if colors else self.labelColor #Use class default if not specified
        numSub = numSub if numSub else self.subLabel
        
        m = int((len(labels)-1)*(numSub+1)+1)
        s = (self.rotRange[1]-self.rotRange[0])/(m-1)
        r1, r2, r3, r4 = [44, 40, 37, 30]
        
        for i in range(m):
            vector = np.array([math.sin(self.rotRange[0] + i*s), math.cos(self.rotRange[0] + i*s)])
            if i%(numSub+1) == 0:
                idx = i//(numSub+1)
                img = self.addLayers(img, 
                                     self.drawLine((50+vector*r1, (50+vector*r3)), 3, colors[idx], opacity), 
                                     self.drawTxt(labels[idx], 50+vector*r4, colors[idx], 7,opacity=opacity))
            else:
                img = self.addLayers(img, self.drawLine((50+vector*r1, (50+vector*r2)), 1.5, colors[idx], opacity))
        
        return img
            
              
    def makeTitle(self, color=False, r=23, txtSize=[7,5]):
        color = color if color else self.fontColor
        txtAngle = (self.rotRange[0]+self.rotRange[1])/2
        txtPos = np.array([50+math.sin(txtAngle)*r,50+math.cos(txtAngle)*r])
        
        return self.addLayers(self.drawTxt(self.name, txtPos, color, txtSize[0]), self.drawTxt(self.units, txtPos+[0,7], color, txtSize[1]))
        
    
    def makeIndicator(self, radius=41, color=False, op=210):
        color = color if color else self.color
        
        newImg = self.addLayers(  #indicator made of a triangle, a line and a circle
            self.drawPolygon([(50,50+radius), (50+radius/12, 50), (50-radius/12, 50)], color=color, opacity=op),
            self.drawLine(((50,50),(50,50+radius)),0.5,(125,125,125),opacity=op),
            self.drawCircle(r1=0, r2=3.5, color=(125,125, 125), steps=1)
        )
    
        return newImg
    
    def update(self, load=0):
        angle = self.rotRange[0] + (self.rotRange[1]-self.rotRange[0])*load/100
        if self.pastA == None:
            self.pastA = angle
            self.timeStamp = time.time()
        elif self.direction*self.pastA > self.direction*angle:
            newAngle = self.pastA + self.direction*math.pi*(self.timeStamp-time.time())/2
            angle = newAngle if self.direction*newAngle > self.direction*angle else angle
            self.timeStamp = time.time()
        elif self.direction*self.pastA < self.direction*angle:
            newAngle = self.pastA - self.direction*math.pi*(self.timeStamp-time.time())/2
            angle = newAngle if self.direction*newAngle < self.direction*angle else angle
            self.timeStamp = time.time()
        else:
            self.timeStamp = time.time()
            return False

        self.pastA = angle
        self.display = self.indicator.rotate(180*angle/math.pi)
        return self.display
        
    def preview(self, color=(0,0,0,255),load=0): #returns all our elems for design purposes
        self.update(load)
        return self.addLayers(self.newFilter(color), self.setUp(), self.display)
    
    def setUp(self): #should only be ran once since unmovable
        return self.bk
    
    def __call__(self, load=0): #this return the indicator at load val
        display = self.update(load)
        return display


cpuMeter = meterIcon([500,500],'CPU', '%', 
                     labels=[0, 20, 40, 60, 80, 100], subLabel=3,
                     rotRange=[7*math.pi/4, math.pi/4],
                     color=(0,50,250), 
                     labelColor=[(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(255,0,255)],
                     fontColor=(255,255,255),
                     outline=False)


class lcdIcon(icon):
    def __init__(self, name, size, valPos=[50,50], color=(0,0,255), fontColor=(255,255,255)):
        icon.__init__(self, name, size, color)
        
        self.fontColor = fontColor
        self.valPos = valPos
        
        self.units = ''
        self.value = 0.0
        
        #The elements are the single color bk, the info icon/name, the displayed value and its unit
        self.bk = self.addLayers(self.makeBk(self.color), self.makeTitle())
        
        self.unitDisplay = self.makeUnits(self.units)
        self.valueDisplay = self.makeValue(value=self.value,pos=self.valPos)
        self.display = self.addLayers(self.unitDisplay, self.valueDisplay)

    
    def makeBk(self, color):
        return self.addLayers(self.newFilter(color=(255,255,255)+(255,)),self.newFilter(color=color+(235,)))
    
    def makeTitle(self, title=False, color=False, pos=[10,50]):
        color = color if color else self.fontColor
        title = title if title else self.name
        
        return self.drawTxt(title, pos, color, 90)
    
    def makeUnits(self, units, pos=[90,50], color=False):
        color = color if color else self.fontColor
        return self.drawTxt(units, pos, color, 90)

    
    def makeValue(self, value, pos, color=False):
        color = color if color else self.fontColor
        return self.drawTxt(value, pos, color, 70)
    
    def update(self, displayIn):
        
        if displayIn == (self.value, self.units):#if value unchanged, no update to save cpu usage
            return False
        if type(displayIn[0]) is float: #Floats will have a max of 2 decimals
            displayIn = (format(displayIn[0], '.2f'), displayIn[1])
            
        
        if displayIn[0] != self.value: #change displayed value if different
            self.value = displayIn[0]
            self.valueDisplay = self.makeValue(value=self.value,pos=self.valPos)
        if displayIn[1] != self.units: #change units if different
            self.units = displayIn[1]
            self.unitDisplay = self.makeUnits(self.units)
        
        self.display = self.addLayers(self.unitDisplay, self.valueDisplay) #place value and unit in display
        
        return self.display
        
        
    def preview(self, displayIn=(0.0,'')):
        return self.addLayers(self.setUp(), self(displayIn))
    
    def setUp(self):
        return self.bk
    
    def __call__(self, displayIn=(0.0,'')):
        display = self.update(displayIn)
        return display


class indicatorIcon(icon):
    def __init__(self, name, size, link, rot=0,color=(255,0,0), bkColor=(0,0,0), baseColor=(255,255,255)):
        icon.__init__(self, name, size, color)
        
        self.baseColor = baseColor
        self.bkColor = bkColor
        
        self.bk = self.pasteImg(self.newFilter(self.baseColor+(180,)),size=90)
        self.indicator = self.fetchImg(link, rotation=rot)
        
        self.state = True
        self.on = self.newFilter(self.color+(210,))
        self.off = self.newFilter(self.color+(100,))
        
    def fetchImg(self, link, color=False, rotation=0):
        newImg = Image.open(link).rotate(rotation)   #get img
        color = color if color else self.bkColor
        
        Filter = self.pasteImg(newImg, size=90)
        
        filterArr = np.array(Filter)
        filterArr[:,:,3] = 255 - filterArr[:,:,3] #fetch and inverse aplha level
        filterArr[:,:,:3] = color
        
        return Image.fromarray(filterArr).filter(ImageFilter.GaussianBlur(1))
    
    def update(self, state):
        if self.state == state:#if state doesn't change no need to compute new image
            return False
        self.state = state
        return self.addLayers(self.on if self.state else self.off, self.indicator)
    
    def preview(self, val=False):
        return self.addLayers(self.setUp(), self(val))
    
    def setUp(self):
        return self.bk
    
    def __call__(self, p=False):
        display = self.update(p)
        return display