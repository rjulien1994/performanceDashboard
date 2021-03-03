import numpy as np
import math
from PIL import Image, ImageDraw, ImageFont

class icon(object):   #The dashboard will consist of icons which have a name size and default color
    def __init__(self, name, size, color):
        self.name = name
        self.size = np.array(size) #x and y size of the desired img
        self.color = color
    
    #We create base methods to ease image creation
    def drawCircle(self, center=[50,50], r1=0, r2=50, color=False, steps=10): #return a fading circle filled from r1 to r2 
        circle = self.newFilter()                                             #if steps = 1 -> no Fading
        Filter = self.newFilter()
        draw = ImageDraw.Draw(Filter)
        
        color = (color if color else self.color) + (int(math.floor(300/steps)),)
        center = np.array(center)
        
        for s in range(1, steps+1):#we draw the outline with a fading
            r = r1 + s*(r2-r1)/steps
            w = r - r1
            draw.ellipse((tuple(self.size*(center-r)/100),tuple(self.size*(center+r)/100)), fill=color)
            circle = Image.alpha_composite(circle, Filter)
            
        if r1 > 0:
            draw = ImageDraw.Draw(circle)
            draw.ellipse((tuple(self.size*(center-r1)/100),tuple(self.size*(center+r1)/100)), fill=(0,0,0,0))
            
        return circle
    
    def drawPolygon(self, corners, color=False, opacity=255, outline=(125,125,125)):
        color = color if color else self.color
        
        Filter = self.newFilter()
        draw = ImageDraw.Draw(Filter)
        corners = [tuple(np.array(corner)*self.size/100) for corner in corners]
        
        draw.polygon(corners, fill=color+(opacity,), outline=outline+(opacity,))
        
        return Filter
    
    def drawTxt(self, txt, center, color, txtSize, font="arial.ttf", opacity=255): #center of txt in %
        Filter = self.newFilter()
        draw = ImageDraw.Draw(Filter)
        fnt = ImageFont.truetype(font, int(txtSize*self.size[1]/100)) #font size based on img height
        
        if txt != '':
            txt = str(txt) #So we can directly feed int and floats
            center = np.array(center)*self.size/100
            center[0] -= fnt.getmask(txt).getbbox()[2]/2 #center txt
            center[1] -= 1.1*fnt.size/2 
            center[0] = min(center[0], self.size[0]-fnt.getmask(txt).getbbox()[2]-self.size[0]/100)
            center[0] = max(center[0], 0+self.size[0]/100)
            draw.text(tuple(center), txt, fill=color+(opacity,), font=fnt)
        
        return Filter
    
    def drawLine(self, posInfo, width, color, opacity=255):
        img = self.newFilter()
        draw = ImageDraw.Draw(img)
        
        width = int(width*self.size[0]/100) #so input is in % but of any type
        color = color + (opacity,)
        start = tuple(np.array(posInfo[0])*self.size/100)
        end = tuple(np.array(posInfo[1])*self.size/100)
        
        draw.line((start, end), width=width, fill=color)
        
        return img
    
    def addLayers(self, *layers):
        img = self.newFilter()
        for layer in layers:
            img = Image.alpha_composite(img, layer)
        return img
    
    def pasteImg(self, image, pos=[50,50], size=False):
        if size:
            size = self.size*np.array(size)/100 #size given in %
        
            imgSize = np.array(image.size)
            newSize = np.array(imgSize/max(imgSize/size))
            image = image.resize(newSize.astype(int)) #resize while keeping ratio
            image = image.convert('RGBA')
        
        c = np.array(pos)*self.size/100
        box = [int(x) for x in list(c-np.array(image.size)/2)+list(c+np.array(image.size)/2)]
  
        Filter = self.newFilter()  #paste image on bk
        Filter.paste(image,box=box,mask=image)
        
        return Filter
        
    def newFilter(self, color=(0,0,0,0)): 
        return Image.new('RGBA', tuple(self.size), color=color)