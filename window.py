import tkinter as tk
from PIL import ImageTk
from setUp import *
 
window = tk.Tk()

width, height = dash.size
x, y = width/2, height/2

canvas = tk.Canvas(window, width=width, height=height, bg="black")
canvas.pack(expand='true')

BKImg = ImageTk.PhotoImage(dash.setUp())
bk = canvas.create_image(x, y, image=BKImg)

cvElems = {}
    
def updateDash():
    pc.update()
    updates = dash()
    for key in updates.keys():#position, iconObj, value
        img = ImageTk.PhotoImage(updates[key])
        x, y = np.array(dash.elements[key][0])*dash.size/100
        cvElems[key] = [img, canvas.create_image(x, y, image=img)]
    
    window.after(500, updateDash)

updateDash()
window.title('My Title')
        
window.mainloop()
