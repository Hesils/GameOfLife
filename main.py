import tkinter as tk
import time
import threading
import random
import os


class MainFrame(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        x_coord = int(self.winfo_screenwidth() / 2) - 100
        y_coord = int(self.winfo_screenheight() / 2 - 200)
        self.geometry("{}x{}+{}+{}".format(200, 400, x_coord, y_coord))
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
        labelgeneration = tk.Label(self, text="Nombre de generatoion:", font=("Arial", 9))
        labelgeneration.grid(row=4, column=0)
        self.entrygeneration = tk.Entry(self)
        self.entrygeneration.insert(tk.END, "100")
        self.entrygeneration.grid(row=5, column=0)
        btnreset = tk.Button(self, text="Generer", command=self.reset)
        btnreset.grid(row=6, column=0)
        """Graphique data"""
        self.labels = []
        self.windimention = [950, 630]
        self.generation = 100
        """Matrice"""
        self.matrice = []
        self.dimention = [0, 0]
        self.density = 66
        self.initmatrice()

    """Init Methodes"""
    def initmatrice(self):
        self.dimention = [40, 80]
        self.matrice = []
        self.labels = []
        self.density = int(self.entrydensity.get())
        for line in range(self.dimention[0]):
            self.matrice.append([])
            self.labels.append([])
            for col in range(self.dimention[1]):
                chance = random.randrange(1, 100, 1)
                if chance <= self.density:
                    self.matrice[line].append(1)
                    #self.labels[line].append(tk.Label(self, text="X", font=("Arial", 10), bg='grey'))
                else:
                    self.matrice[line].append(0)
                    #self.labels[line].append(tk.Label(self, text="O", font=("Arial", 10), bg='green'))

    def reset(self):
        """
        for one in self.labels:
            for cell in one:
                cell.delete()
        """
        self.initmatrice()
        os.system('cls')
        self.printmatrice()
    """Calcul Next generation"""
    def launchetime(self):
        self.generation = int(self.entrygeneration.get())
        for i in range(self.generation):
            os.system('cls')
            print("Generation " + str(i))
            self.printmatrice()
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
                """
                if newmatrice[coord[0]][coord[1]] == 0:
                    self.labels[coord[0]][coord[1]].config(text="O", bg='grey')
                else:
                    self.labels[coord[0]][coord[1]].config(text="X", bg='green')
                """
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
        for line in self.labels:
            j = 1
            for cell in line:
                cell.grid(row=i, column=j)
                j += 1
            i += 1

    def hidematrice(self):
        for one in self.labels:
            for cell in one:
                cell.place_forget()


if __name__ == '__main__':
    root = MainFrame()
    root.mainloop()
