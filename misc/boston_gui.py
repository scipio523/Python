from Tkinter import *

root=Tk()

photo=PhotoImage(file="penguin.gif")
label=Label(root,image=photo)
label.pack()

root.mainloop()