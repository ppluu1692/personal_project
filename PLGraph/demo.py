from os import error
import tkinter as tk
from tkinter.constants import BOTH, E, END, LEFT, NO, RAISED, RIGHT, TOP, VERTICAL, X, Y, YES
from tkinter.ttk import Entry, Frame, Button, Label, Scrollbar, Style, Treeview
from PIL import Image, ImageTk
from math import *
from random import choice

def getUnit(scale, standard=200):
	exponent = floor(log10(standard/scale))
	mantissa = (standard/scale)/(10**exponent)
	if mantissa < 2:
		return 1, exponent
	elif mantissa < 5:
		return 2, exponent
	else:
		return 5, exponent

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master

		master.geometry("1200x600")
		master.title("PhongLuu Graph")
		master.iconbitmap("image/icon.ico")

		self.menubar = tk.Menu(self.master)
		self.master.config(menu = self.menubar)
		self.toolbar = Frame(self.master, relief=RAISED)
		self.toolbar.pack(side=TOP, fill=X)
		self.createMenu()
	
		mathStyle = Style()
		mathStyle.configure("Treeview", font=('Cambria', 20), rowheight=40)
		mathStyle.map('Treeview', background=[('selected', '#60a830')])

		self.inputFrame = Frame(self.master, width=200)
		self.inputFrame.pack(side=LEFT, fill=None)

		self.inputSb = Scrollbar(self.inputFrame)
		self.inputSb.pack(side=RIGHT, fill=Y)

		lb = Label(self.inputFrame, text="123")
		lb.pack()

		self.selected = None

		self.colors = ('red', 'green', 'blue', 'cyan', 'magenta', 'yellow')
		self.O_x = 300
		self.O_y = 200
		self.Scale = 50

		self.movPos = None
		self.countPos = 0

		def checkFunc(func):
			self.errorLabel['text'] = ''
			if not func:
				return 0
			try:
				x = 0
				y = eval(func)
			except ZeroDivisionError or ValueError:
				return 1
			except:
				self.errorLabel['text'] = 'We dont\'t support this expression format'
				return 0
			return 1

		def addFunc(event=None):
			funcText = entry.get()
			if not checkFunc(funcText):
				return
			self.inputTree.insert(parent='', index='end', values=entry.get())
			entry.delete(0, END)

		def deleteAll():
			for func in self.inputTree.get_children():
				self.inputTree.delete(func)
			entry.delete(0, END)

		def deleteOne(event=None):
			if not self.selected:
				return
			self.inputTree.delete(self.selected)
			self.selected = None
			entry.delete(0, END)

		def configFunc():
			pass

		def option():
			pass

		def select(event=None):
			self.errorLabel['text'] = ''
			entry.delete(0, END)
			self.selected = self.inputTree.focus()
			values = self.inputTree.item(self.selected, 'values')
			entry.insert(0, values[0])

		def update(event=None):
			func = entry.get()
			if not checkFunc(func):
				return
			if not self.selected:
				return
			self.inputTree.item(self.selected, values=entry.get())
			self.selected = None
			entry.delete(0, END)

		def addNupdate(event=None):
			if self.selected:
				update(event)
			else:
				addFunc(event)

		widel = Label(self.toolbar, text="", font=(None, 28))
		widel.grid(row=0, column=0, padx=5)
		
		self.optnImg = ImageTk.PhotoImage(Image.open("image/option.png").resize((21, 21), Image.ANTIALIAS))
		self.optnButton = Button(self.toolbar, image=self.optnImg, command=option)
		self.optnButton.grid(row=0, column=1, padx=15, sticky=E)

		self.setImg = ImageTk.PhotoImage(Image.open("image/setting.png").resize((21, 21), Image.ANTIALIAS))
		self.setButton = Button(self.toolbar, image=self.setImg, command=configFunc)
		self.setButton.grid(row=0, column=2, padx=5)

		self.delImg = ImageTk.PhotoImage(Image.open("image/delete.png").resize((21, 21), Image.ANTIALIAS))
		self.delButton = Button(self.toolbar, image=self.delImg, command=deleteOne)
		self.delButton.grid(row=0, column=3, padx=5)

		fxl = Label(self.toolbar, text="f =", font=("Cambria Italic", 16))
		fxl.grid(row=0, column=4, padx=0)

		entry = Entry(self.toolbar, font=('Cambria', 16), width=30)
		entry.grid(row=0, column=5, padx=10)

		self.doneImg = ImageTk.PhotoImage(Image.open("image/done.png").resize((21, 21), Image.ANTIALIAS))
		self.doneButton = Button(self.toolbar, image=self.doneImg, command=addNupdate)
		self.doneButton.grid(row=0, column=6, padx=5)

		self.delAImg = ImageTk.PhotoImage(Image.open("image/delete_all.png").resize((21, 21), Image.ANTIALIAS))
		self.delAButton = Button(self.toolbar, image=self.delAImg, command=deleteAll)
		self.delAButton.grid(row=0, column=7, padx=5)

		self.errorLabel = tk.Label(self.toolbar, text="", font=('None', 12), fg='red')
		self.errorLabel.grid(row=0, column=8, padx=20)
		

	def createMenu(self):
		# main menu (empty)
		mainMenu = tk.Menu(self.menubar)
		self.menubar.add_cascade(label="Menu", menu=mainMenu)
		# option menu (empty)
		modeMenu = tk.Menu(self.menubar)


root = tk.Tk()
app = Application(master=root)
app.mainloop()


