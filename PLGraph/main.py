import os
import tkinter as tk
from tkinter.constants import BOTH, BOTTOM, CENTER, E, END, LEFT, NO, RAISED, RIGHT, ROUND, TOP, VERTICAL, W, X, Y, YES
from tkinter.ttk import Entry, Frame, Button, Label, Radiobutton, Scrollbar, Style, Treeview
from PIL import Image, ImageTk
from math import *
from random import choice
from pyglet import font

# get Unit on Axis


def getUnit(scale, standard=200):
    # convert scale to scientific notation
    exponent = floor(log10(standard/scale))
    mantissa = (standard/scale)/(10**exponent)
    # return Unit with (1 or 2 or 5)*10^(exponent), round to down floor
    if mantissa < 2:
        return 1, exponent
    elif mantissa < 5:
        return 2, exponent
    else:
        return 5, exponent

# main class extend tkinter.Frame


class Application(tk.Frame):
    # initialize
    def __init__(self, master=None):
        # verify that expression is valid
        def verifyFunc(func):
            self.errorLabel['text'] = ''
            if not func:
                return 0
            try:
                x = 0
                y = eval(func)
            except ValueError:
                return 1
            except:
                self.errorLabel['text'] = 'We dont\'t support this expression format'
                return 1
            return 1

        # add an expression
        def addFunc(event=None):
            funcText = entry.get()
            if not verifyFunc(funcText):
                return
            color = choice(range(5))
            self.inputTree.insert(parent='', index='end', image=self.imgCl[color], values=(
                entry.get(), 'Yes', 3, color, '__'))
            entry.delete(0, END)

        # delete all expression
        def deleteAll():
            for func in self.inputTree.get_children():
                self.inputTree.delete(func)
            entry.delete(0, END)
            self.updateGraph()

        # delete selected expression
        def deleteOne(event=None):
            if not self.selected:
                return
            self.inputTree.delete(self.selected)
            self.selected = None
            entry.delete(0, END)
            self.updateGraph()

        # change selected expression attributes
        def configFunc():
            if not self.selected:
                return
            # show switch button

            def showSwitch():
                idColor = int(configValues[3])
                if configValues[1] == 'Yes':
                    showButton.config(image=self.offImg)
                    showLabel.config(fg='grey')
                    configValues[1] = 'No'
                    idColor = 6
                else:
                    showButton.config(image=self.onImg)
                    showLabel.config(fg='green')
                    configValues[1] = 'Yes'
                self.inputTree.item(
                    self.selected, image=self.imgCl[idColor], values=tuple(configValues))
                self.updateGraph()
            # change thickness:

            def setThickness():
                configValues[2] = thicknessSpin.get()
                self.inputTree.item(self.selected, values=tuple(configValues))
                self.updateGraph()
            # set graph color

            def setColor():
                configValues[3] = int(self.changeColor.get())
                self.inputTree.item(
                    self.selected, image=self.imgCl[configValues[3]], values=tuple(configValues))
                self.updateGraph()
            # apply the changes

            def apply():
                thicknesss = int(thicknessSpin.get())
                if 1 <= thicknesss <= 10:
                    configValues[2] = thicknesss
                configValues[3] = int(self.changeColor.get())
                self.inputTree.item(self.selected, values=tuple(configValues))
                self.updateGraph()
                self.changeColor = None
                configBox.destroy()

            # create a configure window
            configBox = tk.Toplevel(self.master)
            configBox.geometry("250x350+500+200")
            configBox.title('Configure')
            configBox.iconbitmap('image/setting.png')

            # get graph information
            configValues = self.inputTree.item(self.selected, 'values')
            configValues = list(configValues)

            # Label of expression with graph color
            funcLabel = tk.Label(configBox, text=configValues[0], font=('STIX Two Text', 20),
                                 fg='black', bd=1, bg='white')
            funcLabel.pack(pady=5)

            # on and off switch icon
            self.onImg = ImageTk.PhotoImage(Image.open(
                "image/on.png").resize((40, 40), Image.LANCZOS))
            self.offImg = ImageTk.PhotoImage(Image.open(
                "image/off.png").resize((40, 40), Image.LANCZOS))
            # show switch button to change shoving truth
            showButton = tk.Button(
                configBox, bd=0, image=self.onImg, command=showSwitch)
            showLabel = tk.Label(configBox, text='Show', font=('None', 16))
            showButton.place(relx=0.7, rely=0.2)
            showLabel.place(relx=0.15, rely=0.21)
            # set default value
            if configValues[1] == 'Yes':
                showButton.config(image=self.onImg)
                showLabel.config(fg="green")
            else:
                showButton.config(image=self.offImg)
                showLabel.config(fg="grey")

            # thickness text
            thicknessLb = tk.Label(
                configBox, text='Thickness', font=('None', 16))
            thicknessLb.place(relx=0.15, rely=0.4)

            # set default thickness
            defaultVar = tk.StringVar()
            defaultVar.set(configValues[2])
            # thickness spin box to change thickness
            thicknessSpin = tk.Spinbox(configBox, from_=1, to=10,
                                       textvariable=defaultVar, command=setThickness)
            thicknessSpin.config(width=3, font=('None', 16))
            thicknessSpin.place(relx=0.7, rely=0.4)

            # change color and set default change color
            self.changeColor = tk.StringVar()
            self.changeColor.set(configValues[3])

            # 6 color selection button
            Radiobutton(configBox, image=self.imgCl[0], variable=self.changeColor, value=0,
                        command=setColor).place(relx=0.1, rely=0.6)
            Radiobutton(configBox, image=self.imgCl[1], variable=self.changeColor, value=1,
                        command=setColor).place(relx=0.1, rely=0.8)
            Radiobutton(configBox, image=self.imgCl[2], variable=self.changeColor, value=2,
                        command=setColor).place(relx=0.4, rely=0.6)
            Radiobutton(configBox, image=self.imgCl[3], variable=self.changeColor, value=3,
                        command=setColor).place(relx=0.4, rely=0.8)
            Radiobutton(configBox, image=self.imgCl[4], variable=self.changeColor, value=4,
                        command=setColor).place(relx=0.7, rely=0.6)
            Radiobutton(configBox, image=self.imgCl[5], variable=self.changeColor, value=5,
                        command=setColor).place(relx=0.7, rely=0.8)

            # apply button to apply changes
            applyButton = tk.Button(
                configBox, text='Apply', bd=2, command=apply)
            applyButton.pack(padx=50, side=BOTTOM, pady=5,)

        # option
        def option():
            pass

        # select an expression
        def select(event=None):
            self.errorLabel['text'] = ''
            entry.delete(0, END)
            self.selected = self.inputTree.focus()
            values = self.inputTree.item(self.selected, 'values')
            entry.insert(0, values[0])

        # update change
        def update(event=None):
            func = entry.get()
            if not verifyFunc(func):
                return
            if not self.selected:
                return
            values = self.inputTree.item(self.selected, 'values')
            self.inputTree.item(self.selected, values=(
                entry.get(), values[1], values[2], values[3], values[4]))
            self.selected = None
            entry.delete(0, END)

        def addNupdate(event=None):
            if self.selected:
                update(event)
            else:
                addFunc(event)
            self.updateGraph()

        def resize(event=None):
            self.updateGraph()
        # I don't know this code meaning
        super().__init__(master)
        self.master = master

        # set something on Window
        master.geometry("1200x600")
        master.title("PhongLuu Graph")
        master.iconbitmap("image/icon.ico")

        # create a menubar on top and toolbar below
        self.menubar = tk.Menu(self.master)
        self.master.config(menu=self.menubar)
        self.toolbar = Frame(self.master, relief=RAISED)
        self.toolbar.pack(side=TOP, fill=X)
        # create a menu option on menubar (not use)
        self.createMenu()

        # create a style for treeview (input expression)
        treeStyle = Style()
        treeStyle.configure("Treeview", font=(
            'STIX Two Text', 20), rowheight=40)
        treeStyle.map('Treeview', background=[('selected', '#60a830')])

        # input Frame include input expression(s) and its scroll bar
        self.inputFrame = Frame(self.master)
        self.inputFrame.pack(side=LEFT, fill=Y)

        # input scrollbar
        self.inputSb = Scrollbar(self.inputFrame)
        self.inputSb.pack(side=RIGHT, fill=Y)

        # input tree = input expression(s)
        # expression attributes:
        # 1. Func: string of expression
        # 2. Show: truth value of shoving expression graph
        # 3. Thickness: graph thickness
        # 4. Color: graph color
        # 5. Shape: shape of graph, '__' is solid line
        self.inputTree = Treeview(
            self.inputFrame, show="tree", yscrollcommand=self.inputSb.set)
        self.inputTree['column'] = (
            "Func", "Show", "Thickness", "Color", "Shape")
        self.inputTree.column("#0", width=50, anchor='center')
        self.inputTree.column("Func", anchor="w", width=260)
        self.inputTree["displaycolumns"] = ("Func")
        self.inputTree.pack(side=LEFT, fill=Y)

        # linked scroll bar and input tree
        self.inputSb.configure(command=self.inputTree.yview)

        # expression that being selected
        self.selected = None

        # color code of graph
        # 0:red:'#ed2939'
        # 1:green:'#03ac13'
        # 2:blue:'#1338be'
        # 3:cyan:'#0098aa'
        # 4:violet:'#710193'
        # 5:yellow:'#fdd017'
        self.colors = ('#ed2939', '#03ac13', '#1338be',
                       '#0098aa', '#710193', '#fdd017')
        self.imgCl = []
        self.imgCl.append(ImageTk.PhotoImage(Image.open(
            "image/red.png").resize((24, 24), Image.LANCZOS)))
        self.imgCl.append(ImageTk.PhotoImage(Image.open(
            "image/green.png").resize((24, 24), Image.LANCZOS)))
        self.imgCl.append(ImageTk.PhotoImage(Image.open(
            "image/blue.png").resize((24, 24), Image.LANCZOS)))
        self.imgCl.append(ImageTk.PhotoImage(Image.open(
            "image/cyan.png").resize((24, 24), Image.LANCZOS)))
        self.imgCl.append(ImageTk.PhotoImage(Image.open(
            "image/violet.png").resize((24, 24), Image.LANCZOS)))
        self.imgCl.append(ImageTk.PhotoImage(Image.open(
            "image/yellow.png").resize((24, 24), Image.LANCZOS)))
        self.imgCl.append(ImageTk.PhotoImage(Image.open(
            "image/no_fill.png").resize((24, 24), Image.LANCZOS)))

        # position of Originpos in x axis and y axis
        self.O_x = 300
        self.O_y = 200
        # ratio of size in pixel and 1 unit in axis
        self.Scale = 50

        # position of mouse cursor when moving graph and countPos (read self.movingPressL)
        self.movPos = None
        self.countPos = 0

        # Label to wider toolbar
        widel = Label(self.toolbar, text="", font=(None, 28))
        widel.grid(row=0, column=0, padx=5)

        # option button (option tool) and its icon
        self.optnImg = ImageTk.PhotoImage(Image.open(
            "image/option.png").resize((21, 21), Image.LANCZOS))
        self.optnButton = Button(
            self.toolbar, image=self.optnImg, command=option)
        self.optnButton.grid(row=0, column=1, padx=15, sticky=E)

        # setting button (setting tool) and its image
        self.setImg = ImageTk.PhotoImage(Image.open(
            "image/setting.png").resize((21, 21), Image.LANCZOS))
        self.setButton = Button(
            self.toolbar, image=self.setImg, command=configFunc)
        self.setButton.grid(row=0, column=2, padx=5)

        # delete button (delete tool) and its icon
        self.delImg = ImageTk.PhotoImage(Image.open(
            "image/delete.png").resize((21, 21), Image.LANCZOS))
        self.delButton = Button(
            self.toolbar, image=self.delImg, command=deleteOne)
        self.delButton.grid(row=0, column=3, padx=5)

        # input box to edit expression
        fxl = Label(self.toolbar, text="f =", font=("STIX Two Text", 16))
        fxl.grid(row=0, column=4, padx=0)

        entry = Entry(self.toolbar, font=('Cambria', 16), width=30)
        entry.grid(row=0, column=5, padx=10)

        # done button (done tool) and its icon
        self.doneImg = ImageTk.PhotoImage(Image.open(
            "image/done.png").resize((21, 21), Image.LANCZOS))
        self.doneButton = Button(
            self.toolbar, image=self.doneImg, command=addNupdate)
        self.doneButton.grid(row=0, column=6, padx=5)

        # delete all button (delete all tool) and its icon
        self.delAImg = ImageTk.PhotoImage(Image.open(
            "image/delete_all.png").resize((21, 21), Image.LANCZOS))
        self.delAButton = Button(
            self.toolbar, image=self.delAImg, command=deleteAll)
        self.delAButton.grid(row=0, column=7, padx=5)

        # error label to show invalid expression error
        self.errorLabel = tk.Label(
            self.toolbar, text="", font=('None', 12), fg='red')
        self.errorLabel.grid(row=0, column=8, padx=20)

        # coordinate label to show coordinate of mouse cursor
        self.coorStr = tk.StringVar()
        self.coorStr.set(123)
        self.coorLabel = tk.Label(self.toolbar, text=self.coorStr)
        self.coorLabel.grid(row=0, column=9)

        # graph Frame inculde graph canvas
        self.graFrame = Frame(self.master)
        self.graFrame.pack(fill=BOTH, expand=YES)

        # graph canvas to draw graph
        self.graCanvas = tk.Canvas(self.graFrame, bg="white")
        self.graCanvas.pack(fill=BOTH, expand=YES)
        self.graCanvas.update()
        self.updateGraph()

        # main window event
        # 1. input box event:
        # 	When you enter a expression, this expression will be added into input tree or update selected expression
        # 2. input tree event
        # 	When you double-click or enter on input tree, expresstion will be selected and grab to input box
        # 3. graph canvas event
        #	3.1. When you scroll mouse, graph zoom in or out
        #	3.2. When you drag and clicking, graph move
        #	3.3. When you release mouse button, movPos record is deleted
        # 	3.4. When you click icon on graph
        # 4. main window event
        # 	When you resize window
        entry.bind('<Return>', addNupdate)
        self.inputTree.bind('<Double-Button-1>', select)
        self.inputTree.bind('<Return>', select)

        self.graCanvas.bind('<MouseWheel>', self.wheelingMouse)
        self.graCanvas.bind('<B1-Motion>', self.movingPressL)
        self.graCanvas.bind('<ButtonRelease-1>', self.releasePress)
        self.graCanvas.bind('<Button-1>', self.quickConfig)

        self.master.bind('<Configure>', resize)
        self.pack()

    def createMenu(self):
        # main menu (empty)
        mainMenu = tk.Menu(self.menubar)
        self.menubar.add_cascade(label="Menu", menu=mainMenu)
        # option menu (empty)
        modeMenu = tk.Menu(self.menubar)

    def drawAxis(self):
        Unit = getUnit(self.Scale)

        UnitPx = int(10**Unit[1]*Unit[0]*self.Scale)

        # draw horizontal line and vertical line
        if Unit[0] == 2:
            for i in range(13):
                y_mark = self.O_y % UnitPx + UnitPx*(i-1)
                for j in range(1, 4):
                    self.graCanvas.create_line(0, y_mark + j*UnitPx//4,
                                               1800, y_mark + j*UnitPx//4, fill='#f0f0f0', width=1)
            for i in range(23):
                x_mark = self.O_x % UnitPx + UnitPx*(i-1)
                for j in range(1, 4):
                    self.graCanvas.create_line(x_mark + j*UnitPx//4, 0,
                                               x_mark + j*UnitPx//4, 1000, fill='#f0f0f0', width=2)
        else:
            for i in range(13):
                y_mark = self.O_y % UnitPx + UnitPx*(i-1)
                for j in range(1, 5):
                    self.graCanvas.create_line(0, y_mark + j*UnitPx//5,
                                               1800, y_mark + j*UnitPx//5, fill='#f0f0f0', width=1)
            for i in range(23):
                x_mark = self.O_x % UnitPx + UnitPx*(i-1)
                for j in range(1, 5):
                    self.graCanvas.create_line(x_mark + j*UnitPx//5, 0,
                                               x_mark + j*UnitPx//5, 1000, fill='#f0f0f0', width=2)

        for i in range(23):
            x_mark = self.O_x % UnitPx + UnitPx*i
            self.graCanvas.create_line(
                x_mark, 0, x_mark, 1000, fill='#c8c8c8', width=2)

        for i in range(13):
            y_mark = self.O_y % UnitPx + UnitPx*i
            y_axis = round((self.O_y//UnitPx-i)*Unit[0]*10**Unit[1], 10)
            self.graCanvas.create_line(
                0, y_mark, 1800, y_mark, fill='#c8c8c8', width=2)

        # draw axis
        self.graCanvas.create_line(
            0, self.O_y, 1800, self.O_y, fill='black', width=2)
        self.graCanvas.create_line(
            self.O_x, 0, self.O_x, 1000, fill='black', width=2)

    def Plotting(self):
        def drawFunc(values):
            if values[1] != 'Yes':
                return
            posXY = []
            for x_px in range(0, 1800, 5):
                x = (x_px - self.O_x)/self.Scale
                y = None
                try:
                    y = eval(values[0])
                except:
                    continue
                y_px = int(-y*self.Scale + self.O_y)
                posXY.append((x_px, y_px))
                if len(posXY) == 3:
                    posXY.pop(0)
                    self.graCanvas.create_line(posXY[0][0], posXY[0][1], posXY[1][0], posXY[1][1],
                                               fill=self.colors[values[3]], width=values[2], capstyle=ROUND, joinstyle=ROUND)
        for child in self.inputTree.get_children():
            drawFunc(self.inputTree.item(child)['values'])

    def unitNicon(self):
        Unit = getUnit(self.Scale)
        UnitPx = int(10**Unit[1]*Unit[0]*self.Scale)
        width = self.graCanvas.winfo_width()
        height = self.graCanvas.winfo_height()
        # write unit
        if 12 <= self.O_y <= height:
            for i in range(23):
                x_mark = self.O_x % UnitPx + UnitPx*i
                x_axis = round((i-self.O_x//UnitPx)*Unit[0]*10**Unit[1], 10)
                if abs(x_axis) > 1E-9:
                    self.graCanvas.create_text(
                        x_mark, self.O_y+10, font=('Calibri', 11), text=f'{x_axis}')
                else:
                    self.graCanvas.create_text(
                        x_mark-10, self.O_y+10, font=('Calibri', 11), text='0')
        else:
            self.graCanvas.create_rectangle(
                0, 0, 1800, 12, fill='white', outline='white')
            for i in range(23):
                x_mark = self.O_x % UnitPx + UnitPx*i
                x_axis = round((i-self.O_x//UnitPx)*Unit[0]*10**Unit[1], 10)
                if abs(x_axis) > 1E-9:
                    self.graCanvas.create_text(
                        x_mark, 6, font=('Calibri', 11), text=f'{x_axis}')
                else:
                    self.graCanvas.create_text(
                        x_mark, 6, font=('Calibri', 11), text='0')

        if 40 <= self.O_x <= width:
            for i in range(13):
                y_mark = self.O_y % UnitPx + UnitPx*i
                y_axis = round((self.O_y//UnitPx-i)*Unit[0]*10**Unit[1], 10)
                if abs(y_axis) > 1E-9:
                    self.graCanvas.create_text(
                        self.O_x-10, y_mark, font=('Calibri', 11), text=f'{y_axis}')
        else:
            self.graCanvas.create_rectangle(
                0, 0, 40, 1000, fill='white', outline='white')
            for i in range(13):
                y_mark = self.O_y % UnitPx + UnitPx*i
                y_axis = round((self.O_y//UnitPx-i)*Unit[0]*10**Unit[1], 10)
                self.graCanvas.create_text(
                    20, y_mark, font=('Calibri', 11), text=f'{y_axis}')

        self.homeImg = tk.PhotoImage(file='image/home.png')
        self.graCanvas.create_image(width-50, height-100, image=self.homeImg)
        self.ziImg = tk.PhotoImage(file='image/zoom_in.png')
        self.graCanvas.create_image(width-50, height-60, image=self.ziImg)
        self.zoImg = tk.PhotoImage(file='image/zoom_out.png')
        self.graCanvas.create_image(width-50, height-20, image=self.zoImg)

    def updateGraph(self):
        self.graCanvas.delete("all")
        self.drawAxis()
        self.Plotting()
        self.unitNicon()
        self.graCanvas.update()

    def wheelingMouse(self, event=None):
        newScale = self.Scale*(event.delta/600 + 1)
        newScale = float('%.2g' % newScale)
        if newScale <= 0.04:
            self.errorLabel.config(text='Minimum zooming')
            return
        elif newScale > 200000:
            self.errorLabel.config(text='Maximum zooming')
            return
        self.errorLabel.config(text='')
        rate = newScale/self.Scale
        self.Scale = newScale
        self.O_x = int(event.x*(1-rate) + rate*self.O_x)
        self.O_y = int(event.y*(1-rate) + rate*self.O_y)
        self.updateGraph()

    def movingPressL(self, event=None):
        if not self.movPos:
            self.movPos = event.x, event.y
        if self.countPos == 5:
            self.O_x += event.x - self.movPos[0]
            self.O_y += event.y - self.movPos[1]
            self.movPos = event.x, event.y
            self.countPos = 0
            self.updateGraph()
        self.countPos += 1

    def releasePress(self, event=None):
        self.movPos = None

    def quickConfig(self, event=None):
        width = self.graCanvas.winfo_width()
        height = self.graCanvas.winfo_height()

        if (width-65 < event.x < width-35) and (height-115 < event.y < height-85):
            self.O_x = width//2
            self.O_y = height//2
            self.Scale = 101
            self.updateGraph()
        elif (width-65 < event.x < width-35) and (height-75 < event.y < height-45):
            newScale = self.Scale*(1.2)
            newScale = float('%.2g' % newScale)
            if newScale > 200000:
                self.errorLabel.config(text='Maximum zooming')
                return
            self.Scale = newScale
            self.updateGraph()
        elif (width-65 < event.x < width-35) and (height-35 < event.y < height-5):
            newScale = self.Scale*(0.8)
            newScale = float('%.2g' % newScale)
            if newScale <= 0.04:
                self.errorLabel.config(text='Minimum zooming')
                return
            self.Scale = newScale
            self.updateGraph()
        self.errorLabel.config(text='')


font.add_file("Font/STIXTwoText-Italic.ttf")

root = tk.Tk()
app = Application(master=root)
app.mainloop()

