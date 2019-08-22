from tkinter import *
root = Tk()
 
lbl = Label(root, text="이름")
lbl.grid(row=0, column=0)
txt = Entry(root)
txt.grid(row=0, column=1)
lb2 = Label(root, text="dddd")
lb2.grid(row=1, column=0)
txt1 = Entry(root)
txt1.grid(row=1, column=1)
btn = Button(root, text="Save", width=15)
btn.grid(row=2, column=1)
 
root.mainloop()

