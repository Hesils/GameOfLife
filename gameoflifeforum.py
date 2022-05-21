import tkinter as tk
import threading
import random
import time
from functools import partial


class MainFrame(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        x_coord = int(self.winfo_screenwidth() / 2) - 600
        y_coord = int(self.winfo_screenheight() / 2 - 390)
        self.geometry("{}x{}+{}+{}".format(1200, 750, x_coord, y_coord))
        """Graphique elements"""
        # Labels
        self.labelcountgen = tk.Label(self, text="Generation 0", font=("Arial", 9))
        self.labelcountgen.grid(row=0, column=1)
        # Buttons
        btnlaunch = tk.Button(self, text="Launch", command=self.launchtime)
        btnlaunch.grid(row=0, column=0)
        """Graphique data"""
        self.graphiquematrice = tk.Canvas(self, height=740, width=1000, bg='white')
        self.windimention = [1200, 750]
        self.generation = 100
        """Matrice"""
        self.matrice = []
        self.firstquarter = []
        self.secondquarter = []
        self.thirdquarter = []
        self.fourthquarter = []
        self.newmatrice = []
        self.cellids = []
        self.dimention = [70, 100]
        self.density = 15
        self.scale = 10
        self.initmatrice()

    """Init Methodes"""
    def initmatrice(self):
        """
        initialisation du premier etat de la matrice
        """
        self.dimention = [12, 12]
        self.matrice = []
        self.cellids = []
        self.graphiquematrice.grid(row=1, column=1, rowspan=10)
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
    """Calcul Next generation"""
    def launchtime(self):
        for i in range(self.generation):
            self.labelcountgen.config(text="Generation " + str(i + 1))
            self.evolve() # Lance l''evolution avec multithreading
            self.update()

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
                print("first quarter coord:" + str(line) + " " + str(col))
                #with lock:
                if self.firstquarter[line][col] == 0:
                    self.graphiquematrice.itemconfig(self.cellids[line][col], fill='white')
                else:
                    self.graphiquematrice.itemconfig(self.cellids[line][col], fill='green')

    def nextsecondquarterstate(self, quarter, lock):
        self.secondquarter = []
        start = quarter
        for line in range(quarter):
            self.secondquarter.append([])
            for col in range(self.dimention[1]):
                self.secondquarter[line].append(self.nextcellstate([line + start, col]))
                #with lock:
                print("seconde quarter : " + str(line + start) + " " + str(col))
                if self.secondquarter[line][col] == 0:
                    self.graphiquematrice.itemconfig(self.cellids[line][col], fill='white')
                else:
                    self.graphiquematrice.itemconfig(self.cellids[line][col], fill='green')

    def nextthirdquarterstate(self, quarter, lock):
        self.thirdquarter = []
        start = quarter * 2
        for line in range(quarter):
            self.thirdquarter.append([])
            for col in range(self.dimention[1]):
                self.thirdquarter[line].append(self.nextcellstate([line + start, col]))
                #with lock:
                print("third quarter : " + str(line + start) + " " + str(col))
                if self.thirdquarter[line][col] == 0:
                    self.graphiquematrice.itemconfig(self.cellids[line + start][col], fill='white')
                else:
                    self.graphiquematrice.itemconfig(self.cellids[line + start][col], fill='green')

    def nextfourthquarterstate(self, quarter, lock):
        self.fourthquarter = []
        start = quarter * 3
        for line in range(quarter):
            self.fourthquarter.append([])
            for col in range(self.dimention[1]):
                self.fourthquarter[line].append(self.nextcellstate([start + line, col]))
                #with lock:
                print("fourth quarter : " + str(line + start) + " " + str(col))
                if self.fourthquarter[line][col] == 0:
                    self.graphiquematrice.itemconfig(self.cellids[start + line][col], fill='white')
                else:
                    self.graphiquematrice.itemconfig(self.cellids[start + line][col], fill='green')

    def evolve(self):
        self.newmatrice = []
        threads = []
        lock = threading.Lock()
        quarter = int(self.dimention[0] / 4) # Division de la matrice en 4 pour reduire le temps de calcul
        threads.append(threading.Thread(target=self.nextfirstquarterstate, args=(quarter, lock))) # Premier quart
        threads.append(threading.Thread(target=self.nextsecondquarterstate, args=(quarter, lock))) # Deuxieme quart
        threads.append(threading.Thread(target=self.nextthirdquarterstate, args=(quarter, lock))) # 3eme quart
        threads.append(threading.Thread(target=self.nextfourthquarterstate, args=(quarter, lock))) # 4eme quart
        i = 0
        for t in threads:
            try:
                t.start() # Lancement des 4 threads
            except:
                print("Error: not able to lauch thread " + str(i))
            i += 1
        for t in threads:
            while t.is_alive():
                pass
        #    t.join() # Attente de la fin de tous les calculs
        self.matrice = self.firstquarter + self.secondquarter + self.thirdquarter + self.fourthquarter
    """Binding Methodes"""
    def changestateonclick(self, idcell, event):
        color = self.graphiquematrice.itemcget(idcell, 'fill')
        if color == 'white':
            self.graphiquematrice.itemconfig(idcell, fill='green')
        else:
            self.graphiquematrice.itemconfig(idcell, fill='white')


if __name__ == '__main__':
    root = MainFrame()
    root.mainloop()
