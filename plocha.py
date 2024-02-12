import random

class Plocha:

    def __init__(self, subor="nova_hra.txt"):

        self.subor = subor
        self.faza_tahu = random.choice(["1","2"])
       
        if self.subor == "nova_hra.txt":
            self.plocha_zoz = []

            for i in range(8):
                pom = []
                for j in range(8):
                    if i == 0 or i == 1 or i == 2:
                        pom.append("1")
                    elif i == 7 or i == 6 or i == 5:
                        pom.append("2")
                    else:
                        pom.append("x")
                self.plocha_zoz.append(pom)
            
            deli = 0
            for i in range(3):
                for j in range(8):
                    if deli == 0:
                        if j % 2 == 0:
                            self.plocha_zoz[i][j] = "x"
                    elif deli == 1:
                        if j % 2 != 0:
                            self.plocha_zoz[i][j] = "x"
                    elif deli == 2:
                        if j % 2 == 0:
                            self.plocha_zoz[i][j] = "x"
                deli += 1
            
            deli = 0
            for i in range(5,8):
                for j in range(8):
                    if deli == 0:
                        if j % 2 != 0:
                            self.plocha_zoz[i][j] = "x"
                    elif deli == 1:
                        if j % 2 == 0:
                            self.plocha_zoz[i][j] = "x"
                    elif deli == 2:
                        if j % 2 != 0:
                            self.plocha_zoz[i][j] = "x"
                deli += 1
            
            file = open(subor, "w")

            for riadok in self.plocha_zoz:
                for prvok in riadok:
                    file.write(str(prvok))
                file.write("\n")

            file.close()

        elif self.subor != "nova_hra.txt" and self.subor[-4:] == ".txt":
            
            self.plocha_zoz = []

            file = open(subor, "r")
            for riadok in file.readlines():
                pom = []
                for prvok in riadok:
                    if prvok != "\n":
                        pom.append(prvok)
                self.plocha_zoz.append(pom)

            file.close()
            
    def __str__(self):

        print(self.faza_tahu)
        self.str_plocha = "Na rade je: "+str(self.faza_tahu)+"\n"

        for riadok in self.plocha_zoz:
            for prvok in riadok:
                self.str_plocha += prvok
            self.str_plocha += "\n"
        
        return self.str_plocha[:-1]
        
    def tah_dolava(self, riadok, stlpec):

        if str(riadok) in "01234567" and str(stlpec) in "01234567":

            if self.faza_tahu == "1" and riadok < 6 and stlpec < 6 and self.plocha_zoz[riadok+1][stlpec+1] == "2" and \
                 self.plocha_zoz[riadok+2][stlpec+2] == "x": #hrac 1 vyhodi hraca 2

                self.plocha_zoz[riadok][stlpec] = "x"
                self.plocha_zoz[riadok+1][stlpec+1] = "x"
                self.plocha_zoz[riadok+2][stlpec+2] = "1"
                self.faza_tahu = "2"

            elif self.faza_tahu == "2" and riadok > 1 and stlpec > 1 and self.plocha_zoz[riadok-1][stlpec-1] == "1" and \
                 self.plocha_zoz[riadok-2][stlpec-2] == "x": #hrac 2 vyhodi hraca 1

                self.plocha_zoz[riadok][stlpec] = "x"
                self.plocha_zoz[riadok-1][stlpec-1] = "x"
                self.plocha_zoz[riadok-2][stlpec-2] = "2"
                self.faza_tahu = "1"

            elif self.faza_tahu == "2" and riadok > 0 and stlpec > 0 and self.plocha_zoz[riadok-1][stlpec-1] == "x":
                self.plocha_zoz[riadok][stlpec] = "x"
                self.plocha_zoz[riadok-1][stlpec-1] = "2"
                self.faza_tahu = "1"
            
            elif self.faza_tahu == "1" and riadok < 7 and stlpec < 7 and self.plocha_zoz[riadok+1][stlpec+1] == "x":
                self.plocha_zoz[riadok][stlpec] = "x"
                self.plocha_zoz[riadok+1][stlpec+1] = "1"
                self.faza_tahu = "2"

                         
            else:
                print("Na tomto políčku sa nenachádza tvoja figúrka alebo sa týmto smerom nedokáže posunúť")
        
        else:
            print("Chyba v zadanom príkaze")
        
        self.prepis_subor()

    def tah_doprava(self, riadok, stlpec):

        if str(riadok) in "01234567" and str(stlpec) in "01234567":

            if self.faza_tahu == "1" and riadok < 6 and stlpec > 1 and self.plocha_zoz[riadok+1][stlpec-1] == "2" and \
                 self.plocha_zoz[riadok+2][stlpec-2] == "x": #hrac 1 vyhodi hraca 2

                self.plocha_zoz[riadok][stlpec] = "x"
                self.plocha_zoz[riadok+1][stlpec-1] = "x"
                self.plocha_zoz[riadok+2][stlpec-2] = "1"
                self.faza_tahu = "2"

            elif self.faza_tahu == "2" and riadok > 1 and stlpec < 6 and self.plocha_zoz[riadok-1][stlpec+1] == "1" and \
                 self.plocha_zoz[riadok-2][stlpec+2] == "x": #hrac 2 vyhodi hraca 1

                self.plocha_zoz[riadok][stlpec] = "x"
                self.plocha_zoz[riadok-1][stlpec+1] = "x"
                self.plocha_zoz[riadok-2][stlpec+2] = "2"
                self.faza_tahu = "1"
            
            elif self.faza_tahu == "2" and riadok > 0 and stlpec < 7 and self.plocha_zoz[riadok-1][stlpec+1] == "x":
                self.plocha_zoz[riadok][stlpec] = "x"
                self.plocha_zoz[riadok-1][stlpec+1] = "2"
                self.faza_tahu = "1"
            
            elif self.faza_tahu == "1" and riadok < 7 and stlpec > 0 and self.plocha_zoz[riadok+1][stlpec-1] == "x":
                self.plocha_zoz[riadok][stlpec] = "x"
                self.plocha_zoz[riadok+1][stlpec-1] = "1"
                self.faza_tahu = "2"

            else:
                print("Na tomto políčku sa nenachádza tvoja figúrka alebo sa týmto smerom nedokáže posunúť")

        else:
            print("Chyba v zadanom príkaze")
        
        self.prepis_subor()
        
    def kontroluj_koniec_hry(self):

        poc_h1 = 0
        poc_h2 = 0
        for riadok in self.plocha_zoz:
            for prvok in riadok:
                if prvok == "1":
                    poc_h1 += 1
                elif prvok == "2":
                    poc_h2 += 1
        
        if poc_h1 == 0:
            return "h2_vyhral"

        elif poc_h2 == 0:
            return "h1_vyhral"

    def prepis_subor(self):

        subor = open(self.subor, "w")
        subor.close()

        subor = open(self.subor, "w")
        for riadok in self.plocha_zoz:
            for prvok in riadok:
                subor.write(prvok)
            subor.write("\n")
        
        subor.close()

    def spocitaj_1(self):
        poc = 0
        for riadok in self.plocha_zoz:
            for prvok in riadok:
                if prvok == "1":
                    poc += 1
        return poc 

    def spocitaj_2(self):
        poc = 0
        for riadok in self.plocha_zoz:
            for prvok in riadok:
                if prvok == "2":
                    poc += 1
        return poc 



    



