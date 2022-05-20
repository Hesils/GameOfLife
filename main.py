import tkinter as tk
import time
import threading
import random
import os
from functools import partial


class MainFrame(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        x_coord = int(self.winfo_screenwidth() / 2) - 600
        y_coord = int(self.winfo_screenheight() / 2 - 390)
        self.geometry("{}x{}+{}+{}".format(1200, 750, x_coord, y_coord))
        """Graphique elements"""
        btnnextgen = tk.Button(self, text="Next Generation", command=self.nextmatricestate)
        btnnextgen.grid(row=0, column=0)
        btnlauch = tk.Button(self, text="Launch", command=self.launchetime)
        btnlauch.grid(row=1, column=0)
        labeldensity = tk.Label(self, text="Densité de départ:", font=("Arial", 9))
        labeldensity.grid(row=2, column=0)
        self.entrydensity = tk.Entry(self)
        self.entrydensity.insert(tk.END, "30")
        self.entrydensity.grid(row=3, column=0)
        labelgeneration = tk.Label(self, text="Nombre de generation:", font=("Arial", 9))
        labelgeneration.grid(row=4, column=0)
        self.labelcountgen = tk.Label(self, text="Generation 0", font=("Arial", 9))
        self.labelcountgen.grid(row=0, column=1)
        self.entrygeneration = tk.Entry(self)
        self.entrygeneration.insert(tk.END, "100")
        self.entrygeneration.grid(row=5, column=0)
        """Graphique data"""
        self.graphiquematrice = tk.Canvas(self, height=740, width=1000, bg='white')
        self.graphiquematrice.bind('<MouseWheel>', self.zoomwithmousewheel)
        self.windimention = [1200, 750]
        self.generation = 100
        """Matrice"""
        self.matrice = []
        self.cellids = []
        self.dimention = [0, 0]
        self.density = 66
        self.scale = 10
        self.initmatrice()

    """Init Methodes"""
    def initmatrice(self):
        self.dimention = [70, 100]
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
        self.initmatrice()
        os.system('cls')
        self.printmatrice()

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
            self.nextmatricestate()
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


if __name__ == '__main__':
    root = MainFrame()
    root.mainloop()
