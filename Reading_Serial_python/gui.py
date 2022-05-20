import tkinter
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog


mygui = Tk()
mygui.geometry("600x600")
mygui.title('Supermarket assistant')

label = Label(mygui, text = "Welcome", width = 10, fg = "black", font = "Castellar")  
label.place(x = 300, y = 50) 

img= (Image.open("image.png"))
resized_image= img.resize((450,308), Image.ANTIALIAS)
img = ImageTk.PhotoImage(resized_image)
panel = Label(mygui, image=img)
panel.place(x = 75, y = 100)


def files():
    mygui.filename = filedialog.askopenfilename(initialdir = '/Users/thomasneaverson/Desktop/MTRX2700/Major_Project/Reading_Serial_python/magnet.csv')

button1=tkinter.Button(mygui, text="View Stocktake", command = files)
button1.place(x=250, y = 500, width = 100, height = 50)

button2=tkinter.Button(mygui, text="button2")
button2.place(x=100, y=500, width = 100, height = 50)

button3=tkinter.Button(mygui, text="button3")
button3.place(x=400, y=500, width = 100, height = 50)


def updateImage():
    img2 = ImageTk.PhotoImage(Image.open("image.png"))
    panel.configure(image=img2)
    panel.image = img2
    mygui.after(1, updateImage)


# mygui.after(1, updateImage)
mygui.mainloop()

