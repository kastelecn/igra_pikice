from tkinter import *
from tkinter.colorchooser import *
import math

vodoravno = []
for i in range(7):
    vrsta = []
    vodoravno.append(vrsta)
    for j in range(6):
                vrsta.append(False)
navpicno = []
for i in range(6):
    vrsta1 = []
    navpicno.append(vrsta1)
    for j in range(7):
        vrsta1.append(False)
            
NEVTRALNO = False

class Pikice():
    def __init__(self, master):
        self.stanje = NEVTRALNO
        self.vodoravno = vodoravno
        self.navpicno = navpicno
        self.koordinata_x0 = 0
        self.koordinata_x1 = 0
        self.koordinata_y0 = 0
        self.koordinata_y1 = 0
        self.igralec1 = 0
        self.igralec2 = 0
        self.zmagovalec = ""
        
        
       
        #platno
        self.canvas = Canvas(master, width=300, height=300)
        self.canvas.grid(row=0, column=0, columnspan=5, rowspan=3)
        
        #pikice na platnu
        for x in range(1,8):
            for y in range(1,8):
                self.canvas.coords = (x,y)
                self.canvas.create_oval(40*x-3, 40*y-3, 40*x+3, 40*y+3)
           
        
        #menu
        menu = Menu(master)
        master.config(menu=menu)

        #podmenu
        file_menu = Menu(menu)
        menu.add_cascade(label = "File", menu = file_menu)

        #izbire v file_menu
        #
        #file_menu.add_command(label = "Odpri", command = self.odpri)
        file_menu.add_command(label = "Poglej zgodovino", command = self.poglej_zgodovino)
        file_menu.add_command(label = "Nova igra",command=self.nova_igra)
        #file_menu.add_command(label = "Izhod", command = self.izhod)
        file_menu.add_command(label="Izhod", command=master.destroy)
        file_menu.add_command(label="Shrani", command=self.pisi_zgodovino)

        self.canvas.bind("<Button-1>", self.narisi_crto)

        self.napis_spodaj = StringVar(value="igralec1 je na potezi")
        napis = Label(master, textvariable=self.napis_spodaj)
        napis.grid(row=3, column=2 )

        self.sprotni_rezultat1 = StringVar(value = "0")
        napis = Label(master, textvariable=self.sprotni_rezultat1)
        napis.grid(row=3, column=0)

        self.sprotni_rezultat2 = StringVar(value = "0")
        napis = Label(master, textvariable=self.sprotni_rezultat2)
        napis.grid(row=3, column=4)
  
  
    def poglej_zgodovino(self):
        ime = filedialog.askopenfilename()
        if ime == "":  # Pritisnili smo Cancel
            return
        with open(ime, encoding="utf8") as f:
            for v in f:
                print (v)
        #print ("zgodovina")
                         
    def nova_igra(self):
        self.canvas.delete(ALL)
        self.igralec1 = 0
        self.igralec2 = 0
        self.stanje = NEVTRALNO
        for x in range(1,8): #pikice na platnu
            for y in range(1,8):
                self.canvas.coords = (x,y)
                self.canvas.create_oval(40*x-3, 40*y-3, 40*x+3, 40*y+3)
        self.sprotni_rezultat1.set("0")
        self.sprotni_rezultat2.set("0")
        self.napis_spodaj.set("igralec1 je na potezi")
        for i in self.navpicno:
            for j in i:
                j = False
        for i in self.vodoravno:
            for j in i:
                j = False
        

   

    def najdi_točki(self, x, y):
        x0 = x // 40 * 40
        y0 = y // 40 * 40
        zgoraj_levo = (x-x0)+(y-y0) < 40
        zgoraj_desno = (x - x0) > (y - y0)
        if zgoraj_levo:
            if zgoraj_desno:
                return (x0, y0, x0 + 40, y0)
            else:
                return (x0, y0, x0, y0 + 40)
        else:
            if zgoraj_desno:
                return (x0 + 40, y0, x0 + 40, y0 + 40)
            else:
                return (x0, y0 + 40, x0 + 40, y0 + 40)
      
          
        
    def narisi_crto(self, event):
        print(event.x, event.y)
        (x0, y0, x1, y1) = self.najdi_točki(event.x, event.y)
        if x0 >= 40 and y0 >= 40 and x1 <= 280 and y1 <= 280 :
            
        
            if x0 == x1:
                i = y0 // 40 - 1 #vrstica v seznamu navpično 
                j = x0 // 40 - 1 # stolpec v seznamu navpično
                k = y0 // 40 - 1 #vrstica v seznamu vodoravno 
                l = x0 // 40 - 1 # stolpec v seznamu vodoravno
                print(i, j, k, l )

                if not self.navpicno[i][j]:
                    self.canvas.create_line(x0, y0, x1, y1)
                    self.stanje = not self.stanje
                    if self.stanje:
                        self.napis_spodaj.set("igralec 2 je na potezi")
                    else:
                        self.napis_spodaj.set("igralec 1 je na potezi")
                    self.navpicno[i][j] = True
                    if i <7 and j <7 and k <6 and l <7:
                        if self.navpicno[i][j-1] and self.vodoravno[k][l-1] and self.vodoravno[k+1][l-1]:
                            print("levo")
                            self.koordinata_x0 = x0 -40
                            self.koordinata_x1 = x0
                            self.koordinata_y0 = y0
                            self.koordinata_y1 = y0 +40
                            self.narisi_krog()
                            
                            
                    if i <7 and j <6 and k <6 and l <7:
                        if self.navpicno[i][j+1] and self.vodoravno[k][l] and self.vodoravno[k+1][l]:
                            self.koordinata_x0 = x0 
                            self.koordinata_x1 = x0 + 40
                            self.koordinata_y0 = y0
                            self.koordinata_y1 = y0 +40
                            self.narisi_krog()
                            print("desno")
                else:
                    print ("je ze")
                    
            elif y0 == y1:
                i = y0 // 40 - 1 #vrstica v seznamu navpično 
                j = x0 // 40 - 1 # stolpec v seznamu navpično
                k = y0 // 40 - 1 #vrstica v seznamu vodoravno 
                l = x0 // 40 - 1 # stolpec v seznamu vodoravno
                print(i, j, k, l )
                if not self.vodoravno[k][l]:
                    
                    self.canvas.create_line(x0, y0, x1, y1)
                    self.stanje = not self.stanje
                    if self.stanje:
                        self.napis_spodaj.set("igralec 2 je na potezi")
                    else:
                        self.napis_spodaj.set("igralec 1 je na potezi")
                    self.vodoravno[k][l] = True
                    if i <7 and j <6 and k <7 and l <7:
                        if self.vodoravno[k-1][l] and self.navpicno[i-1][j] and self.navpicno[i-1][j+1]:
                            self.koordinata_x0 = x0 
                            self.koordinata_x1 = x0 + 40
                            self.koordinata_y0 = y0 -40
                            self.koordinata_y1 = y0 
                            self.narisi_krog()
                            print("gor")
                    if i <7 and j <6 and k <6 and l <7:
                        if self.vodoravno[k+1][l] and self.navpicno[i][j] and self.navpicno[i][j+1]:
                            self.koordinata_x0 = x0 
                            self.koordinata_x1 = x0 + 40
                            self.koordinata_y0 = y0 
                            self.koordinata_y1 = y0 + 40
                            self.narisi_krog()
                            print("dol")
                else:
                    print ("je ze")
            
            #print(self.vodoravno,"         ", self.navpicno)
        else:
            print("ne znam")
        print(self.najdi_točki(event.x, event.y))
        self.zamenjaj_sprotni_rezultat()
        self.konec_igre()
        

        print(self.igralec1, self.igralec2)

        
    def konec_igre(self): #,igralec1, igralec2
        igralec1 = self.igralec1
        igralec2 = self.igralec2
        if igralec1 + igralec2 == 36:
            if igralec1 > igralec2:
                self.zmagovalec = "igralec 1"
                self.napis_spodaj.set("Igre je konec! Zmagal je {0}.".format(self.zmagovalec))
            elif igralec1 < igralec2:
                self.zmagovalec = "igralec 2"
                self.napis_spodaj.set("Igre je konec! Zmagal je {0}.".format(self.zmagovalec))
            else:
                self.zmagovalec = "izenačeno"
                self.napis_spodaj.set("Igre je konec! Izenačen izid.")
            self.pisi_zgodovino()
            return True
            print ("konec igre", self.zmagovalec)

            
    def narisi_krog(self):
        print("krogec pobarvan",self.koordinata_x0,self.koordinata_y0,self.koordinata_x1,self.koordinata_y1
              )
        if self.koordinata_x0 < 241 and self.koordinata_x0 > 39 and self.koordinata_y0 < 241 and self.koordinata_y0 > 39 :
            if self.stanje:
                self.canvas.create_oval(self.koordinata_x0,self.koordinata_y0,self.koordinata_x1,self.koordinata_y1, fill='green')
                self.igralec1 += 1  
            else:
                self.canvas.create_oval(self.koordinata_x0,self.koordinata_y0,self.koordinata_x1,self.koordinata_y1, fill='red')
                self.igralec2 += 1



    def pisi_zgodovino(self):

        ime = filedialog.asksaveasfilename()
        with open(ime, "wt", encoding="utf8") as f:
            if self.zmagovalec != "izenačeno":
                f.write('zmagovalec je {0}, rezultat: {1}:{2}'.format(self.zmagovalec, self.igralec1, self.igralec2))
            else:
                f.write('Izenačeno')
            
       

    def zamenjaj_sprotni_rezultat(self):
        self.sprotni_rezultat1.set("{0}".format(self.igralec1))
        self.sprotni_rezultat2.set("{0}".format(self.igralec2))

        


    





root = Tk()
aplikacija = Pikice(root)

