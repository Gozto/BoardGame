from plocha import *
from PIL import Image, ImageTk


class Kresli:

    canvas = None

    def __init__(self, canvas, subor="nova_hra.txt"):
        
        self.plocha = Plocha(subor)
        self.canvas = canvas
        self.moz_tahu_on_off = 0 #toto tu mam na to aby som nemohol viackrat vykreslit moznosti tahu
        self.zisti_kam_on_off = 0 #toto tu mam na to aby mi to nespadlo ked viackrat kliknem zisti kam ist
        self.faza_tahu = self.plocha.faza_tahu
        self.canvas.bind("<Button-1>", self.moznosti_tahu)
        self.canvas.bind("<Button-3>", self.zisti_kam_ist)
        self.vybrana_figurka = 0
        self.pohyb = ""
               
    def kresli_plochu(self, zoznam_plocha):

        self.canvas.delete("all")
        self.pohyb = ""
        self.zoz = zoznam_plocha
        x = 50
        y = 50

        poc = 1
        for riadok in self.zoz:
            for prvok in riadok:
                if poc % 2 == 0:
                    self.canvas.create_rectangle(x, y, x+50, y+50, fill="saddlebrown")
                elif poc % 2 != 0:
                    self.canvas.create_rectangle(x, y, x+50, y+50, fill="darkgoldenrod")
                if prvok == "1":
                    self.canvas.create_oval(x,y,x+50,y+50, fill="red")
                    self.canvas.create_text(x+25,y+25,text="1", font="Arial 20")
                elif prvok == "2":
                    self.canvas.create_oval(x,y,x+50,y+50, fill="blue")
                    self.canvas.create_text(x+25,y+25,text="2", font="Arial 20")
                x+=50
                poc += 1
            y+=50
            x=50
            poc += 1
        
        #vykreslenie pismen a cisel vedla sachovnice
        pismena = "ABCDEFGH"
        cisla = "12345678"
        x = 25
        y = 75
        for i in range(8):
            self.canvas.create_text(x, y, text = cisla[i], font = "15")
            y+=50
        y = 25
        x = 75
        for i in range(8):
            self.canvas.create_text(x, y, text = pismena[i], font = "15")
            x+=50
        
        #vykreslenie tlacidla koniec
        self.canvas.create_rectangle(0,0,50,50, outline="", fill="yellow")
        self.canvas.create_text(25, 25, text = "Ukonči hru", font = "Arial 7")

    def je_na_sachovnici(self, nove_policko):

        return 0 <= nove_policko[0] <= 7 and 0 <= nove_policko[1] <= 7

    def je_volne(self, policko):

        assert self.je_na_sachovnici(policko)
        return self.zoz[policko[0]][policko[1]] == "x"
          
    def get_clicked(self, x, y):

        self.x = x
        self.y = y

        if self.x >= 50 and self.y >= 50 and self.x <= 450 and self.y <= 450:

            self.stlpec = (self.x // 50) - 1
            self.riadok = (self.y // 50) - 1

            self.poz = (self.riadok, self.stlpec)

            return self.poz

        elif 0 <= self.x < 50  and 0 <= self.y < 50:
            pass

        else:
            raise IndexError("Klikol si mimo plochy")     

    def moznosti_tahu(self, event):
        
        if self.moz_tahu_on_off == 0:

            #ked kliknes tlacidlo koniec
            if 0 <= event.x < 50 and 0 <= event.y < 50:
                poc1 = self.plocha.spocitaj_1()
                poc2 = self.plocha.spocitaj_2()
                self.canvas.unbind("<Button-1>")
                self.canvas.unbind("<Button-3>")

                self.canvas.delete("all")
                if poc1 > poc2:
                    self.canvas.after(1000)
                    self.canvas.delete("all")
                    self.canvas.create_rectangle(0, 0, 510, 510, outline="", fill="light blue")
                    self.canvas.create_text(250,150, text="Hráč 1 vyhral!", font = "Arial 20")
                    self.animacia2()
                    self.canvas.update()
                elif poc1 < poc2:
                    self.canvas.after(1000)
                    self.canvas.delete("all")
                    self.canvas.create_rectangle(0, 0, 510, 510, outline="", fill="light blue")
                    self.canvas.create_text(250,150, text="Hráč 2 vyhral!", font = "Arial 20")
                    self.animacia2()
                    self.canvas.update()
                elif poc1 == poc2:
                    self.canvas.after(1000)
                    self.canvas.delete("all")
                    self.canvas.create_rectangle(0, 0, 510, 510, outline="", fill="light blue")
                    self.canvas.create_text(250,150, text="Hra skončila remízou", font = "Arial 20")
                    self.animacia3()
                    self.canvas.update()
            #koniec tlacidla

            else:
                self.poz = self.get_clicked(event.x,event.y)
                riadok = self.poz[0]
                stlpec = self.poz[1]
                poz_x = (stlpec+1)*50
                poz_y = (riadok+1)*50
                self.vybrana_figurka = (riadok,stlpec)
                self.smery = [(1,1),(1,-1)] #vlavo, vpravo
                self.tahy=[None, None]


                if self.faza_tahu == "1":
                    self.smery = [(1,1),(1,-1)]
                else:
                    self.smery = [(-1,1),(-1,-1)]
                    assert self.faza_tahu == "2"

                #pridavanie policiek na ktore sa mozem posunut do self.tahy
                if self.zoz[riadok][stlpec] == self.faza_tahu:

                    for i in range(2):
                        
                        nove_policko = [riadok+self.smery[i][0], stlpec+self.smery[i][1]]
                        if self.je_na_sachovnici(nove_policko):

                            if self.je_volne(nove_policko):
                                self.tahy[i] = nove_policko
                        
                            elif self.zoz[nove_policko[0]][nove_policko[1]] not in [self.faza_tahu, "x"]: #kontrolujem ci tam je superova figurka
                                nove_policko = [riadok + 2*self.smery[i][0], stlpec + 2*self.smery[i][1]] #ked idem o 2 policka viac
                                if self.je_na_sachovnici(nove_policko) and self.je_volne(nove_policko):
                                    self.tahy[i] = nove_policko
                    

                    #vykreslenie moznosti tahu
                    if self.faza_tahu == "1":

                        if self.tahy[0] != None:

                            poz_y_pol = (self.tahy[0][0])*50
                            poz_x_pol = (self.tahy[0][1])*50
                            self.canvas.create_rectangle(poz_x_pol+50, poz_y_pol+50, poz_x_pol+100, poz_y_pol+100, fill="red", outline="red")
                            self.moz_tahu_on_off = 1
                            self.zisti_kam_on_off = 0

                        if self.tahy[1] != None:

                            poz_y_pol = (self.tahy[1][0])*50
                            poz_x_pol = (self.tahy[1][1])*50
                            self.canvas.create_rectangle(poz_x_pol+50, poz_y_pol+50, poz_x_pol+100, poz_y_pol+100, fill="red", outline="red")
                            self.moz_tahu_on_off = 1
                            self.zisti_kam_on_off = 0

                    if self.faza_tahu == "2":

                        if self.tahy[0] != None:

                            poz_y_pol = (self.tahy[0][0])*50
                            poz_x_pol = (self.tahy[0][1])*50
                            self.canvas.create_rectangle(poz_x_pol+50, poz_y_pol+50, poz_x_pol+100, poz_y_pol+100, fill="red", outline="red")
                            self.moz_tahu_on_off = 1
                            self.zisti_kam_on_off = 0

                        if self.tahy[1] != None:
                            poz_y_pol = (self.tahy[1][0])*50
                            poz_x_pol = (self.tahy[1][1])*50
                            self.canvas.create_rectangle(poz_x_pol+50, poz_y_pol+50, poz_x_pol+100, poz_y_pol+100, fill="red", outline="red")
                            self.moz_tahu_on_off = 1
                            self.zisti_kam_on_off = 0
            #koniec vykreslovania moznosti tahu 

    def zisti_kam_ist(self, event):

        self.poz = self.get_clicked(event.x,event.y)
        riadok = self.poz[0]
        stlpec = self.poz[1]
        
        #normalne tahy bez preskocania
        if self.zisti_kam_on_off == 0 and self.faza_tahu == "1" and riadok-1 == self.vybrana_figurka[0] and \
             stlpec-1 == self.vybrana_figurka[1] and self.moz_tahu_on_off == 1 and riadok == self.tahy[0][0] and \
                stlpec == self.tahy[0][1]:
                 
            self.moz_tahu_on_off = 0
            self.faza_tahu = "2"
            self.vybrana_figurka = 0
            self.zisti_kam_on_off = 1
            self.pohyb = "tl1"
            
             
        elif self.zisti_kam_on_off == 0 and self.faza_tahu == "1" and riadok-1 == self.vybrana_figurka[0] and \
             stlpec+1 == self.vybrana_figurka[1] and self.moz_tahu_on_off == 1 and riadok == self.tahy[1][0] and \
                stlpec == self.tahy[1][1]:
            
            self.moz_tahu_on_off = 0
            self.faza_tahu = "2"
            self.vybrana_figurka = 0
            self.zisti_kam_on_off = 1
            self.pohyb = "tp1"
            
        
        elif self.zisti_kam_on_off == 0 and self.faza_tahu == "2" and riadok+1 == self.vybrana_figurka[0] and \
             stlpec+1 == self.vybrana_figurka[1] and self.moz_tahu_on_off == 1 and riadok == self.tahy[1][0] and \
                stlpec == self.tahy[1][1]:
             
            self.moz_tahu_on_off = 0
            self.faza_tahu = "1"
            self.vybrana_figurka = 0
            self.zisti_kam_on_off = 1
            self.pohyb = "tl2"
            
        
        elif self.zisti_kam_on_off == 0 and self.faza_tahu == "2" and riadok+1 == self.vybrana_figurka[0] and \
             stlpec-1 == self.vybrana_figurka[1] and self.moz_tahu_on_off == 1 and riadok == self.tahy[0][0] and \
                stlpec == self.tahy[0][1]:
                
            self.moz_tahu_on_off=0
            self.faza_tahu = "1"
            self.vybrana_figurka = 0
            self.zisti_kam_on_off = 1
            self.pohyb = "tp2"
        #koniec normalnych tahov


        elif self.zisti_kam_on_off == 0 and self.faza_tahu == "1" and riadok-2 == self.vybrana_figurka[0] and \
             stlpec-2 == self.vybrana_figurka[1] and self.moz_tahu_on_off == 1 and riadok == self.tahy[0][0] and \
                stlpec == self.tahy[0][1]:

            self.moz_tahu_on_off = 0
            self.faza_tahu = "2"
            self.vybrana_figurka = 0
            self.zisti_kam_on_off = 1
            self.pohyb = "tl1p" #tah dolava, hrac 1, preskocenie
            

        elif self.zisti_kam_on_off == 0 and self.faza_tahu == "1" and riadok-2 == self.vybrana_figurka[0] and \
                stlpec+2 == self.vybrana_figurka[1] and self.moz_tahu_on_off == 1 and riadok == self.tahy[1][0] and \
                    stlpec == self.tahy[1][1]:

            self.moz_tahu_on_off = 0
            self.faza_tahu = "2"
            self.vybrana_figurka = 0
            self.zisti_kam_on_off = 1
            self.pohyb = "tp1p" #tah doprava, hrac 1, preskocenie
            

        elif self.zisti_kam_on_off == 0 and self.faza_tahu == "2" and riadok+2 == self.vybrana_figurka[0] and \
            stlpec+2 == self.vybrana_figurka[1] and self.moz_tahu_on_off == 1 and riadok == self.tahy[1][0] and \
                stlpec == self.tahy[1][1]:

            self.moz_tahu_on_off = 0
            self.faza_tahu = "1"
            self.vybrana_figurka = 0
            self.zisti_kam_on_off = 1
            self.pohyb = "tl2p" #tah dolava, hrac 2, preskocenie


        elif self.zisti_kam_on_off == 0 and self.faza_tahu == "2" and riadok+2 == self.vybrana_figurka[0] and \
            stlpec-2 == self.vybrana_figurka[1] and self.moz_tahu_on_off == 1 and riadok == self.tahy[0][0] and \
                stlpec == self.tahy[0][1]:

            self.moz_tahu_on_off = 0
            self.faza_tahu = "1"
            self.vybrana_figurka = 0
            self.zisti_kam_on_off = 1
            self.pohyb = "tp2p" #tah doprava, hrac 2, preskocenie
        #koniec tahov preskocenia        
        
    

        #posun figurky
        if self.pohyb == "tp1":
                
            self.plocha.tah_doprava(riadok-1,stlpec+1)
            self.kresli_plochu(self.plocha.plocha_zoz)
            self.pesiak_na_konci()
            if self.plocha.kontroluj_koniec_hry() == "h1_vyhral" or self.plocha.kontroluj_koniec_hry() == "h2_vyhral":
                print("koniec hry")
                self.canvas.unbind("<Button-1>")
                self.canvas.unbind("<Button-3>")
                self.canvas.after(1000)
                self.canvas.delete("all")
                self.canvas.create_rectangle(0, 0, 510, 510, outline="", fill="light blue")
                self.canvas.create_text(250,150, text="Hráč 1 vyhral!", font = "Arial 20")
                self.animacia2()
                self.canvas.update()
                 
        elif self.pohyb == "tl1":
               
            self.plocha.tah_dolava(riadok-1,stlpec-1)
            self.kresli_plochu(self.plocha.plocha_zoz)
            self.pesiak_na_konci()
            if self.plocha.kontroluj_koniec_hry() == "h1_vyhral" or self.plocha.kontroluj_koniec_hry() == "h2_vyhral":
                print("koniec hry")
                self.canvas.unbind("<Button-1>")
                self.canvas.unbind("<Button-3>")
                self.canvas.after(1000)
                self.canvas.delete("all")
                self.canvas.create_rectangle(0, 0, 510, 510, outline="", fill="light blue")
                self.canvas.create_text(250,150, text="Hráč 1 vyhral!", font = "Arial 20")
                self.animacia2()
                self.canvas.update()

        elif self.pohyb == "tl2":
              
            self.plocha.tah_dolava(riadok+1,stlpec+1)
            self.kresli_plochu(self.plocha.plocha_zoz)
            self.pesiak_na_konci()
            if self.plocha.kontroluj_koniec_hry() == "h1_vyhral" or self.plocha.kontroluj_koniec_hry() == "h2_vyhral":
                print("koniec hry")
                self.canvas.unbind("<Button-1>")
                self.canvas.unbind("<Button-3>")
                self.canvas.after(1000)
                self.canvas.delete("all")
                self.canvas.create_rectangle(0, 0, 510, 510, outline="", fill="light blue")
                self.canvas.create_text(250,150, text="Hráč 2 vyhral!", font = "Arial 20")
                self.animacia2()
                self.canvas.update()

        elif self.pohyb == "tp2":
               
            self.plocha.tah_doprava(riadok+1,stlpec-1)
            self.kresli_plochu(self.plocha.plocha_zoz)
            self.pesiak_na_konci()
            if self.plocha.kontroluj_koniec_hry() == "h1_vyhral" or self.plocha.kontroluj_koniec_hry() == "h2_vyhral":
                print("koniec hry")
                self.canvas.unbind("<Button-1>")
                self.canvas.unbind("<Button-3>")
                self.canvas.after(1000)
                self.canvas.delete("all")
                self.canvas.create_rectangle(0, 0, 510, 510, outline="", fill="light blue")
                self.canvas.create_text(250,150, text="Hráč 2 vyhral!", font = "Arial 20")
                self.animacia2()
                self.canvas.update()
        
        elif self.pohyb == "tl1p":
               
            self.plocha.tah_dolava(riadok-2,stlpec-2)
            self.kresli_plochu(self.plocha.plocha_zoz)
            self.pesiak_na_konci()
            if self.plocha.kontroluj_koniec_hry() == "h1_vyhral" or self.plocha.kontroluj_koniec_hry() == "h2_vyhral":
                print("koniec hry")
                self.canvas.unbind("<Button-1>")
                self.canvas.unbind("<Button-3>")
                self.canvas.after(1000)
                self.canvas.delete("all")
                self.canvas.create_rectangle(0, 0, 510, 510, outline="", fill="light blue")
                self.canvas.create_text(250,150, text="Hráč 1 vyhral!", font = "Arial 20")
                self.animacia2()
                self.canvas.update()
            else:
                self.animacia()

        elif self.pohyb == "tp1p":
               
            self.plocha.tah_doprava(riadok-2,stlpec+2)
            self.kresli_plochu(self.plocha.plocha_zoz)
            self.pesiak_na_konci()
            if self.plocha.kontroluj_koniec_hry() == "h1_vyhral" or self.plocha.kontroluj_koniec_hry() == "h2_vyhral":
                print("koniec hry")
                self.canvas.unbind("<Button-1>")
                self.canvas.unbind("<Button-3>")
                self.canvas.after(1000)
                self.canvas.delete("all")
                self.canvas.create_rectangle(0, 0, 510, 510, outline="", fill="light blue")
                self.canvas.create_text(250,150, text="Hráč 1 vyhral!", font = "Arial 20")
                self.animacia2()
                self.canvas.update()
            else:
                self.animacia()
            
        elif self.pohyb == "tp2p":
               
            self.plocha.tah_doprava(riadok+2,stlpec-2)
            self.kresli_plochu(self.plocha.plocha_zoz)
            self.pesiak_na_konci()
            if self.plocha.kontroluj_koniec_hry() == "h1_vyhral" or self.plocha.kontroluj_koniec_hry() == "h2_vyhral":
                print("koniec hry")
                self.canvas.unbind("<Button-1>")
                self.canvas.unbind("<Button-3>")
                self.canvas.after(1000)
                self.canvas.delete("all")
                self.canvas.create_rectangle(0, 0, 510, 510, outline="", fill="light blue")
                self.canvas.create_text(250,150, text="Hráč 2 vyhral!", font = "Arial 20")
                self.animacia2()
                self.canvas.update()
            else:
                self.animacia()

        elif self.pohyb == "tl2p":
               
            self.plocha.tah_dolava(riadok+2,stlpec+2)
            self.kresli_plochu(self.plocha.plocha_zoz)
            self.pesiak_na_konci()
            if self.plocha.kontroluj_koniec_hry() == "h1_vyhral" or self.plocha.kontroluj_koniec_hry() == "h2_vyhral":
                print("koniec hry")
                self.canvas.unbind("<Button-1>")
                self.canvas.unbind("<Button-3>")
                self.canvas.after(1000)
                self.canvas.delete("all")
                self.canvas.create_rectangle(0, 0, 510, 510, outline="", fill="light blue")
                self.canvas.create_text(250,150, text="Hráč 2 vyhral!", font = "Arial 20")
                self.animacia2()
                self.canvas.update()
            else:
                self.animacia()
            
    def pesiak_na_konci(self):

        hrac1 = "nie"
        hrac2 = "nie"

        #zisti ci prisiel nejaky hrac na koniec
        for i in range(8):

            if self.zoz[7][i] == "1":
                hrac1 = "ano"
                self.zoz[7][i] = "x"
                self.kresli_plochu(self.plocha.plocha_zoz)
                break
            if self.zoz[0][i] == "2":
                hrac2 = "ano"
                self.zoz[0][i] = "x"
                self.kresli_plochu(self.plocha.plocha_zoz)
                break
        

        #pridaj 2 figurky ak niekto prisiel na koniec
        poc = 0
        ind = 7 #index pre forcyklus pre hraca 2 kedze to musim vzdy o riadok zmensit
        
        if hrac1 == "ano":

            for i in range(8):
                for j in range(8):
                    if i % 2 == 0:
                        if j % 2 != 0 and self.zoz[i][j] == "x" and poc < 2:
                            self.zoz[i][j] = "1"
                            self.kresli_plochu(self.plocha.plocha_zoz)
                            poc += 1
                    elif i % 2 != 0:
                        if j % 2 == 0 and self.zoz[i][j] == "x" and poc < 2:
                            self.zoz[i][j] = "1"
                            self.kresli_plochu(self.plocha.plocha_zoz)
                            poc += 1
            poc = 0
            hrac1 = "nie"

        if hrac2 == "ano":

            for i in range(8):
                for j in range(8):
                    if i % 2 == 0:
                        if j % 2 == 0 and self.zoz[ind][j] == "x" and poc < 2:
                            self.zoz[ind][j] = "2"
                            self.kresli_plochu(self.plocha.plocha_zoz)
                            poc += 1
                    elif i % 2 != 0:
                        if j % 2 != 0 and self.zoz[ind][j] == "x" and poc < 2:
                            self.zoz[ind][j] = "2"
                            self.kresli_plochu(self.plocha.plocha_zoz)
                            poc += 1
                ind -= 1

            poc = 0
            hrac2 = "nie"
            
    def animacia(self):
        zoz = []
        for i in range(1, 11):
            obr = Image.open(str(i) + ".png")
            obr1 = obr.resize((250,200))
            zoz.append(ImageTk.PhotoImage(obr1))
    
        tk_id = self.canvas.create_image(250, 250)
        faza = 0
        for i in range(10):
            self.canvas.itemconfig(tk_id, image=zoz[faza])
            faza = (faza + 1) % len(zoz)
            self.canvas.update()
            self.canvas.after(100)

    def animacia2(self):
        zoz = []
        for i in range(1, 16):
            obr = Image.open("w" + str(i) + ".png")
            obr1 = obr.resize((350,300))
            zoz.append(ImageTk.PhotoImage(obr1))
    
        tk_id = self.canvas.create_image(250, 320)
        faza = 0
        for i in range(1000):
            self.canvas.itemconfig(tk_id, image=zoz[faza])
            faza = (faza + 1) % len(zoz)
            self.canvas.update()
            self.canvas.after(100)
    
    def animacia3(self):
        zoz = []
        for i in range(1, 11):
            obr = Image.open("r" + str(i) + ".png")
            obr1 = obr.resize((350,300))
            zoz.append(ImageTk.PhotoImage(obr1))
    
        tk_id = self.canvas.create_image(250, 320)
        faza = 0
        for i in range(1000):
            self.canvas.itemconfig(tk_id, image=zoz[faza])
            faza = (faza + 1) % len(zoz)
            self.canvas.update()
            self.canvas.after(100)






    






