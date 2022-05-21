import tkinter as tk
import time
import threading
from multiprocessing import Process
import random
import os
from functools import partial


def changefill(canevas, state, idcell):
    if state == 0:
        canevas.itemconfig(idcell, fill='white')
    else:
        canevas.itemconfig(idcell, fill='green')


class MyThread(threading.Thread):
    def __init__(self, Threadid, function, startline):
        threading.Thread.__init__(self)
        self.threadID = Threadid
        self.startline = startline
        self.function = function

    def run(self):
        print("running thread n" + str(self.threadID))
        self.function(self.startline)
        print("exiting thread n" + str(self.threadID))


class MainFrame(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        x_coord = int(self.winfo_screenwidth() / 2) - 600
        y_coord = int(self.winfo_screenheight() / 2 - 390)
        self.geometry("{}x{}+{}+{}".format(1200, 750, x_coord, y_coord))
        """Graphique elements"""
        self.controlwin = tk.Toplevel()
        self.controlwin.iconify()
        # Labels
        labeltitle = tk.Label(self.controlwin, text="Paramètres", font=("Arial", 12))
        labeltitle.grid(row=0, column=0, columnspan=2)
        labeldensity = tk.Label(self.controlwin, text="Densité de départ:", font=("Arial", 9))
        labeldensity.grid(row=1, column=0)
        labelgeneration = tk.Label(self.controlwin, text="Nombre de generation:", font=("Arial", 9))
        labelgeneration.grid(row=2, column=0)
        self.labelcountgen = tk.Label(self, text="Generation 0", font=("Arial", 9))
        self.labelcountgen.grid(row=0, column=1)
        # Buttons
        btnclearmatrice = tk.Button(self.controlwin, text="Matrice vierge", command=self.clearmatrice)
        btnclearmatrice.grid(row=3, column=0, columnspan=2)
        btnfillmatrice = tk.Button(self.controlwin, text="Remplir la matrice", command=self.initmatrice)
        btnfillmatrice.grid(row=4, column=0, columnspan=2)
        #btnnextgen = tk.Button(self.controlwin, text="Next Generation", command=self.nextmatricestate)
        btnnextgen = tk.Button(self.controlwin, text="Next Generation", command=self.evolve)
        btnnextgen.grid(row=5, column=0)
        btnlauch = tk.Button(self.controlwin, text="Launch", command=self.launchetime)
        btnlauch.grid(row=5, column=1)
        btnshowparamwin = tk.Button(self, text="Parametre", command=self.showparamwin)
        btnshowparamwin.grid(row=1, column=0)
        # Entries
        self.entrydensity = tk.Entry(self.controlwin)
        self.entrydensity.insert(tk.END, "30")
        self.entrydensity.grid(row=1, column=1)
        self.entrygeneration = tk.Entry(self.controlwin)
        self.entrygeneration.insert(tk.END, "100")
        self.entrygeneration.grid(row=2, column=1)
        """Graphique data"""
        self.graphiquematrice = tk.Canvas(self, height=740, width=1000, bg='white')
        self.graphiquematrice.bind('<MouseWheel>', self.zoomwithmousewheel)
        self.windimention = [1200, 750]
        self.generation = 100
        """Matrice"""
        self.matrice = []
        self.actcoord = []
        self.firstquarter = []
        self.secondquarter = []
        self.thirdquarter = []
        self.fourthquarter = []
        self.newmatrice = []
        self.cellids = []
        self.dimention = [70, 100]
        self.density = 66
        self.scale = 10
        self.bind('<<Myevent>>', self.changecolor)
        self.initmatrice()

    """Init Methodes"""
    def initmatrice(self):
        self.dimention = [40, 40]
        self.matrice = []
        self.cellids = []
        self.graphiquematrice.grid(row=1, column=1, rowspan=10)
        self.density = int(self.entrydensity.get())
        for line in range(self.dimention[0]):
            self.matrice.append([])
            self.cellids.append([])
            for col in range(self.dimention[1]):
                chance = random.randrange(1, 100, 1)
                if chance <= self.density:
                    self.matrice[line].append(1)
                    self.cellids[line].append(self.graphiquematrice.create_rectangle(col*self.scale, line*self.scale, (col+1)*self.scale, (line+1)*self.scale, outline='black', fill='green'))
                else:
                    self.matrice[line].append(0)
                    self.cellids[line].append(self.graphiquematrice.create_rectangle(col*self.scale, line*self.scale, (col+1)*self.scale, (line+1)*self.scale, outline='black', fill='white'))
                self.graphiquematrice.tag_bind(self.cellids[line][col], '<Button-1>', partial(self.changestateonclick, self.cellids[line][col]))

    def reset(self):
        for line in range(self.dimention[0]):
            for col in range(self.dimention[1]):
                self.graphiquematrice.delete(self.cellids[line][col])
        self.initmatrice()
        #os.system('cls')
        #self.printmatrice()

    def clearmatrice(self):
        for line in range(self.dimention[0]):
            for col in range(self.dimention[1]):
                self.graphiquematrice.itemconfig(self.cellids[line][col], fill='white')
    """Calcul Next generation"""
    def launchetime(self):
        self.generation = int(self.entrygeneration.get())
        for i in range(self.generation):
            #os.system('cls')
            #print("Generation " + str(i))
            #self.printmatrice()
            self.labelcountgen.config(text="Generation " + str(i + 1))
            #self.nextmatricestate()
            self.evolve()
            self.update()
            #time.sleep(0.1)

    def getneighboor(self, coord):
        neighboor = []
        for i in range(3):
            lineindex = coord[0] + i - 1
            if lineindex == -1:
                lineindex = self.dimention[0] - 1
            elif lineindex == self.dimention[0]:
                lineindex = 0
            for j in range(3):
                colindex = coord[1] + j - 1
                if colindex == -1:
                    colindex = self.dimention[1] - 1
                elif colindex == self.dimention[1]:
                    colindex = 0
                if lineindex != coord[0] or colindex != coord[1]:
                    neighboor.append(self.matrice[lineindex][colindex])
        return neighboor

    def nextcellstate(self, coord):
        state = self.matrice[coord[0]][coord[1]]
        neighboor = self.getneighboor(coord)
        alive = 0
        dead = 0
        for one in neighboor:
            if one == 0:
                dead += 1
            else:
                alive += 1
        if alive == 3:
            return 1
        elif alive == 2:
            return state
        else:
            return 0

    def nextfirstquarterstate(self, quarter, lock):
        self.firstquarter = []
        start = 0
        for line in range(quarter):
            self.firstquarter.append([])
            for col in range(self.dimention[1]):
                self.firstquarter[line].append(self.nextcellstate([line, col]))
                """
                with lock:
                    #self.actcoord = [line, col]
                #    self.event_generate('<<Myevent>>', when='tail', state=self.firstquarter[line][col])
                    if self.firstquarter[line][col] == 0:
                        self.graphiquematrice.itemconfig(self.cellids[line][col], fill='white')
                    else:
                        self.graphiquematrice.itemconfig(self.cellids[line][col], fill='green')
                        """

    def nextsecondquarterstate(self, quarter, lock):
        self.secondquarter = []
        start = quarter
        for line in range(quarter):
            self.secondquarter.append([])
            for col in range(self.dimention[1]):
                self.secondquarter[line].append(self.nextcellstate([line + start, col]))
                """
                with lock:
                    if self.secondquarter[line][col] == 0:
                        self.graphiquematrice.itemconfig(self.cellids[line][col], fill='white')
                    else:
                        self.graphiquematrice.itemconfig(self.cellids[line][col], fill='green')
                        """

    def nextthirdquarterstate(self, quarter, lock):
        self.thirdquarter = []
        start = quarter * 2
        for line in range(quarter):
            self.thirdquarter.append([])
            for col in range(self.dimention[1]):
                self.thirdquarter[line].append(self.nextcellstate([line + start, col]))
                """
                with lock:
                    if self.thirdquarter[line][col] == 0:
                        self.graphiquematrice.itemconfig(self.cellids[line + start][col], fill='white')
                    else:
                        self.graphiquematrice.itemconfig(self.cellids[line + start][col], fill='green')
                        """

    def nextfourthquarterstate(self, quarter, lock):
        self.fourthquarter = []
        start = quarter * 3
        for line in range(quarter):
            self.fourthquarter.append([])
            for col in range(self.dimention[1]):
                self.fourthquarter[line].append(self.nextcellstate([start + line, col]))
                """
                with lock:
                    if self.firstquarter[line][col] == 0:
                        self.graphiquematrice.itemconfig(self.cellids[start + line][col], fill='white')
                    else:
                        self.graphiquematrice.itemconfig(self.cellids[start + line][col], fill='green')
                        """

    def evolve(self):
        self.newmatrice = []
        threads = []
        lock = threading.Lock()
        quarter = int(self.dimention[0] / 4)
        threads.append(threading.Thread(target=self.nextfirstquarterstate, args=(quarter, lock)))
        threads.append(threading.Thread(target=self.nextsecondquarterstate, args=(quarter, lock)))
        threads.append(threading.Thread(target=self.nextthirdquarterstate, args=(quarter, lock)))
        threads.append(threading.Thread(target=self.nextfourthquarterstate, args=(quarter, lock)))
        i = 0
        for t in threads:
            try:
                t.start()
            except:
                print("Error: not able to lauch thread " + str(i))
            i += 1
        for t in threads:
            t.join()
        self.matrice = self.firstquarter + self.secondquarter + self.thirdquarter + self.fourthquarter
        for line in range(self.dimention[0]):
            for col in range(self.dimention[1]):
                changefill(self.graphiquematrice, self.matrice[line][col], self.cellids[line][col])
                if self.matrice[line][col] == 0:
                    self.graphiquematrice.itemconfig(self.cellids[line][col], fill='white')
                else:
                    self.graphiquematrice.itemconfig(self.cellids[line][col], fill='green')

    def nextmatricestate(self):
        newmatrice = []
        coord = [0, 0]
        for line in self.matrice:
            coord[1] = 0
            newmatrice.append([])
            for cell in line:
                newmatrice[coord[0]].append(self.nextcellstate(coord))
                if newmatrice[coord[0]][coord[1]] == 0:
                    self.graphiquematrice.itemconfig(self.cellids[coord[0]][coord[1]], fill='white')
                else:
                    self.graphiquematrice.itemconfig(self.cellids[coord[0]][coord[1]], fill='green')
                coord[1] += 1
            coord[0] += 1
        self.matrice = newmatrice
    """Printing"""
    def printmatrice(self):
        for line in self.matrice:
            text = ""
            for cell in line:
                text += ("X" if cell == 1 else " ") + " "
            print(text)
        i = 1
    """Binding Methodes"""
    def changestateonclick(self, idcell, event):
        color = self.graphiquematrice.itemcget(idcell, 'fill')
        if color == 'white':
            self.graphiquematrice.itemconfig(idcell, fill='green')
        else:
            self.graphiquematrice.itemconfig(idcell, fill='white')

    def zoomwithmousewheel(self, event):
        if event.delta > 0:
            self.scale += 1
        else:
            self.scale -= 1
        for line in range(self.dimention[0]):
            for col in range(self.dimention[1]):
                self.graphiquematrice.coords(self.cellids[line][col], col*self.scale, line*self.scale, (col+1)*self.scale, (line+1)*self.scale)

    def changecolor(self, event):
        print("in change color")
        print(event.state)
        if event.state == 0:
            self.graphiquematrice.itemconfig(self.cellids[self.actcoord[0]][self.actcoord[1]], fill='white')
        else:
            self.graphiquematrice.itemconfig(self.cellids[self.actcoord[0]][self.actcoord[1]], fill='green')
        self.update()

    def showparamwin(self):
        self.controlwin.deiconify()

    def hideparamwin(self):
        self.controlwin.iconify()


if __name__ == '__main__':
    root = MainFrame()
    root.mainloop()
