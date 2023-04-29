from tkinter import*
import test as gpt
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 520

root = Tk()
root.title('PhongLuu Graph')
# root.iocbitmap('image/icon.ico')


def rederText(text):
    my_canvas.create_text(100, SCREEN_HEIGHT, fill="darkblue",
                          font="Times 20 italic bold", text=text)
    my_canvas.update


def motion(event):
    global var
    x = (event.x-ORIGIN_POS[0])/SCALE
    y = (-event.y+ORIGIN_POS[1])/SCALE
    if event.x > SCREEN_WIDTH or event.y > SCREEN_HEIGHT or event.x < 10 or event.y < 40:
        x, y = 'Out', 'Out'
    var.set('{}, {}'.format(x, y))


def leftButton(event):
    global pointText
    text = ''
    for i in range(len(POINTS)):
        text += '{}. ({}, {}) \n'.format(i+1,
                                         POINTS[i][0]/SCALE, POINTS[i][1]/SCALE)
    pointText.set(text[:-1])


def transformPoint(point, inverser=False):
    global ORIGIN_POS, SCALE
    if inverser:
        return point[0]*SCALE+ORIGIN_POS[0], point[1]*SCALE+ORIGIN_POS[1]
    return (point[0]-ORIGIN_POS[0])/SCALE, (point[1]-ORIGIN_POS[1])/-SCALE


def drawAxis():
    global root
    my_canvas.create_rectangle(
        0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, fill='#032B08')
    my_canvas.create_line(
        0, ORIGIN_POS[1], SCREEN_WIDTH, ORIGIN_POS[1], fill='#009800', width=1)
    my_canvas.create_line(
        ORIGIN_POS[0], 0, ORIGIN_POS[0], SCREEN_HEIGHT, fill='#009800', width=1)
    for i in range(SCREEN_WIDTH//SCALE+1):
        my_canvas.create_line(ORIGIN_POS[0] % SCALE + SCALE*i, ORIGIN_POS[1]-5,
                              ORIGIN_POS[0] % SCALE + SCALE*i, ORIGIN_POS[1]+5, fill='#009800', width=1)
    for i in range(SCREEN_HEIGHT//SCALE+1):
        my_canvas.create_line(ORIGIN_POS[0]-5, ORIGIN_POS[1] % SCALE + SCALE*i,
                              ORIGIN_POS[0]+5, ORIGIN_POS[1] % SCALE + SCALE*i, fill='#009800', width=1)
    my_canvas.place(x=10, y=40)


def drawPoints(points):
    for point in points:
        x0 = point[0] + ORIGIN_POS[0]
        y0 = -point[1] + ORIGIN_POS[1]
        my_canvas.create_rectangle(x0-3, y0-3, x0+3, y0+3, fill='red')
    my_canvas.place(x=10, y=40)


def drawGraph(coefficients):
    print(coefficients)
    posXY = []
    for xA in range(SCREEN_WIDTH):
        xA = xA-ORIGIN_POS[0]
        yA = 0.0
        for j in range(len(coefficients)):
            yA += coefficients[j]*(xA**(len(coefficients)-j-1))
        xA = xA+ORIGIN_POS[0]
        yA = -yA+ORIGIN_POS[1]
        posXY.append((xA, yA))
        if len(posXY) == 3:
            posXY.pop(0)
            my_canvas.create_line(
                posXY[0][0], posXY[0][1], posXY[1][0], posXY[1][1], fill='white', width=2)
    my_canvas.place(x=10, y=40)


def changeOriginPos(padx, pady):
    global ORIGIN_POS
    ORIGIN_POS[0] += padx
    ORIGIN_POS[1] += pady


def select():
    global root, ON_SEL, ON_MOV, ON_ADD
    ON_SEL = True
    ON_MOV = False
    ON_ADD = False
    if ON_SEL:
        root.config(cursor="top_left_arrow")


def move():
    global root, my_canvas, ON_SEL, ON_MOV, ON_ADD
    ON_SEL = False
    ON_MOV = True
    ON_ADD = False
    if ON_MOV:
        root.config(cursor="fleur")
        pos = []

        def button_down(event):
            if ON_MOV:
                global ORIGIN_POS
                if len(pos) == 2:
                    pos.pop(0)
                pos.append((event.x, event.y))
                if len(pos) == 2:
                    print(ORIGIN_POS, (event.x, event.y))
                    ORIGIN_POS = ORIGIN_POS[0] + pos[1][0] - \
                        pos[0][0], ORIGIN_POS[1] + pos[1][1]-pos[0][1]
                    drawAxis()
                    if len(POINTS) >= 2:
                        master = gpt.find_function(POINTS)
                        result = gpt.solveSolution(master, len(POINTS))
                        if result == False:
                            POINTS.pop(-1)
                        else:
                            drawGraph(result)
                    drawPoints(POINTS)

        def button_motion(event):
            if len(pos) == 2 and ON_MOV:
                pos.pop(0)
                pos.pop(0)

        my_canvas.bind('<B1-Motion>', button_down)
        my_canvas.bind('<Motion>', button_motion)


def addPoint():
    global root, ON_SEL, ON_MOV, ON_ADD
    ON_SEL = False
    ON_MOV = False
    ON_ADD = True

    def pointsNgraph(event):
        if ON_ADD:
            if len(POINTS) <= 25:
                my_canvas.create_rectangle(
                    event.x-3, event.y-3, event.x+3, event.y+3, fill='red')
                POINTS.append((event.x-ORIGIN_POS[0], -event.y+ORIGIN_POS[1]))
            if len(POINTS) >= 2:
                master = gpt.find_function(POINTS)
                result = gpt.solveSolution(master, len(POINTS))
                drawAxis()
                if result == False:
                    POINTS.pop(-1)
                    if len(POINTS) >= 2:
                        master = gpt.find_function(POINTS)
                        result = gpt.solveSolution(master, len(POINTS))
                        drawGraph(result)
                else:
                    drawGraph(result)
                drawPoints(POINTS)
    if ON_ADD:
        root.config(cursor="cross")
        my_canvas.bind('<Button-1>', pointsNgraph)


ORIGIN_POS = (SCREEN_WIDTH//2, 100)
ON_SEL = False
ON_MOV = False
ON_ADD = False
POINTS = []
SCALE = 50

Select = Button(root, text="Sel.", bd=5, command=select)
Select.place(x=0, y=0)
Move = Button(root, text='Mov', bd=5, command=move)
Move.place(x=35, y=0)
AddPoint = Button(root, text='Add', bd=5, command=addPoint)
AddPoint.place(x=75, y=0)
root.geometry("1100x600")
my_canvas = Canvas(root, width=SCREEN_WIDTH,
                   height=SCREEN_HEIGHT, bg="#032B08")
my_canvas.place(x=10, y=40)
drawAxis()
var = StringVar()
root.bind('<Motion>', motion)
Coordinate = Label(root, textvariable=var, relief=RAISED)
Coordinate.config(height=1, font=("", 11), fg='blue')
Coordinate.place(relx=0, rely=1, anchor='sw')
pointText = StringVar()
root.bind('<Button-1>', leftButton)
Points = Label(root, textvariable=pointText, relief=RAISED)
Points.config(font=("", 11))
Points.place(x=SCREEN_WIDTH+50, y=100)
root.mainloop()
