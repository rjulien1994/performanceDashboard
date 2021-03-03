from module.indicators import *

class dashboard(icon):
    def __init__(self, name, size, color=(0,0,0)):
        print(name, size, color)
        icon.__init__(self, name, size, color)
        
        self.bk = self.newFilter(color)
        
        self.elements = {}
        
    def addElem(self, key, position, icon, value=None):
        self.elements[key] = [position, icon, value]
        
    def setUp(self): #Place all unmovable images in bk
        for key, value in self.elements.items():
            self.bk = self.addLayers(self.bk, self.pasteImg(value[1].setUp(), value[0]))
        return self.bk
            
    def update(self):
        items = {}
        for key, value in self.elements.items():
            load = value[2]()
            ic = value[1](load)
            if ic:
                items[key] = ic
            
        return items
    
    def preview(self):
        img = self.setUp()
        for key, upd in self.update().items():
            layer = self.pasteImg(upd, self.elements[key][0])
            img = self.addLayers(img, layer)
        return img
        
    def __call__(self):
        return self.update() 