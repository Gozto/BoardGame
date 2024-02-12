from kresli import *
from plocha import *
import tkinter

class Program:

    def __init__(self, subor="nova_hra.txt"):
        self.vykreslene = Kresli(tkinter.Canvas(width=500,height=500, bg="light gray"), subor)   
        self.vykreslene.kresli_plochu(self.vykreslene.plocha.plocha_zoz)
        self.vykreslene.canvas.create_text(250,475, text="Začína hráč č." + str(self.vykreslene.faza_tahu), font="Arial 15")
        print("Na tahu je: " + str(self.vykreslene.faza_tahu))
        
        self.vykreslene.canvas.pack()
        tkinter.mainloop()
        

Program()

