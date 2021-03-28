# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 08:08:14 2021

@author: Martin
"""

from tkinter import * 
from random import choice


##_______________Classe Forme pour le dessin du pendu___________##
class Forme:
    def __init__(self, canevas, x, y):
        self.__canevas = canevas
        self._item = None
        self.x = x
        self.y = y
    
    def effacer(self):
        self.__canevas.delete(self._item)
    
    def deplacement(self, dx, dy):
        self.__canevas.move(self._item, dx, dy)
        self.x += dx
        self.y += dy
        
    def setState(self, s):
        self.__canevas.itemconfig(self._item, state=s)

class Rectangle(Forme):
    def __init__(self, canevas, x, y, l, h, couleur):
        Forme.__init__(self, canevas, x, y)
        self._item = canevas.create_rectangle(x, y, x+l, y+h, fill=couleur)
        self.__l = l
        self.__h = h
    
    def __str__(self):
        return f"Rectangle d'origine {self.x},{self.y} et de dimensions {self.__l}x{self.__h}"

    def get_dim(self):
        return self.__l, self.__h

    def set_dim(self, l, h):
        self.__l = l
        self.__h = h

    def contient_point(self, x, y):
        return self.x <= x <= self.x + self.__l and \
               self.y <= y <= self.y + self.__h

    def redimension_par_points(self, x0, y0, x1, y1):
        self.x = min(x0, x1)
        self.y = min(y0, y1)
        self.__l = abs(x0 - x1)
        self.__h = abs(y0 - y1)
        
    

class Ellipse(Forme):
    def __init__(self, canevas, x, y, rx, ry, couleur):
        Forme.__init__(self, canevas, x, y)
        self._item = canevas.create_oval(x-rx, y-ry, x+rx, y+ry, fill=couleur)
        self.__rx = rx
        self.__ry = ry

    def __str__(self):
        return f"Ellipse de centre {self.x},{self.y} et de rayons {self.__rx}x{self.__ry}"

    def get_dim(self):
        return self.__rx, self.__ry

    def set_dim(self, rx, ry):
        self.__rx = rx
        self.__ry = ry

    def contient_point(self, x, y):
        return ((x - self.x) / self.__rx) ** 2 + ((y - self.y) / self.__ry) ** 2 <= 1

    def redimension_par_points(self, x0, y0, x1, y1):
        self.x = (x0 + x1) // 2
        self.y = (y0 + y1) // 2
        self.__rx = abs(x0 - x1) / 2
        self.__ry = abs(y0 - y1) / 2

   
#_______________________________________________________________________________#




class ZoneAffichage(Canvas):
    def __init__(self, parent, largeur, hauteur):
        Canvas.__init__(self, parent, width=largeur, height=hauteur)
        self.ListeForme=[]       
        self.ListeForme.append(Rectangle(self, 0,  237, 270,  15, "lemon chiffon"))
        self.ListeForme.append(Rectangle(self, 87,   55,  15, 200, "sienna4"))
        self.ListeForme.append(Rectangle(self, 87,   40, 150,  15, "sienna4"))
        self.ListeForme.append(Rectangle(self, 183,  37,  5,  40, "black"))
        self.ListeForme.append(Ellipse(self, 188, 90,  15,  15, "peach puff"))
        self.ListeForme.append(Rectangle(self, 175, 107,  26,  60, "white"))
        self.ListeForme.append(Rectangle(self, 133, 120,  40,  10, "peach puff"))
        self.ListeForme.append(Rectangle(self, 203, 120,  40,  10, "peach puff"))
        self.ListeForme.append(Rectangle(self, 175, 167,  10,  40, "cornflower blue"))
        self.ListeForme.append(Rectangle(self, 191, 167,  10,  40, "cornflower blue"))
        

class FenetrePrincipale(Tk): 
    
    
    
    def chargeMots(self):# Charge la liste de mots du fichier mots.txt
        f = open('mots.txt', 'r')
        s = f.read()
        self.__mots = s.split('\n')
        f.close()
    
        
    def NouvellePartie(self):
        self.__motHazard = choice(self.__mots) # Choix au hasard du mot caché
        self.Motcaché=[]
        for i in range(len(self.__motHazard)):#On remplace les lettres du mot par des étoiles
                       self.Motcaché.append('*')
        
        #Initialisation de tous les artefacts
        self.__Label.config(text = self.Motcaché)#Initialistion des label avec le mot en *
        self.__AfficheScore.config(text = 'Score = 1000',fg='black')#Initialisation du Score à 1000
        self.__Saisie.config(state=NORMAL)
        for b in self.__boutons:#On affiche les boutons
            b.config(state=NORMAL)
        for b in self.DessinPendu.ListeForme:#On cache l'image du pendu 
            b.setState("hidden") 

        self.__triche=False#Initialisation de la triche
        self.__count=0#initialisation du nombre de tentatives
        self.__count2=len(self.__motHazard)#Initialisation du nombre de lettres à trouver
        self.__score=1000
    
    def traitement(self,lettre):#Grise les lettres cliquées        
        LettreCliquée = self.__boutons[ord(lettre)-65]
        LettreCliquée.config(state = DISABLED)
        
        a=False
        for i in range(len(self.__motHazard)) :#Révélation des lettre du mot
            if self.__motHazard[i]==lettre:
                self.Motcaché[i] = self.__motHazard[i]
                self.__Label.config(text = self.Motcaché)
                a=True
                self.__count2-=1
        if a==False and self.__count<10:#Dessin du pendu si mauvaise lettre et diminution du score
            self.DessinPendu.ListeForme[self.__count].setState("normal")#dessin du pendu 
            self.__count+=1#augmentation du nombre de tentatives
            if self.__count>9  and self.__triche==True:
                self.__count=9
            if self.__triche==False:
                self.__score-=100 #le score diminue de 100 à chaque mauvaise lettre sans triche
            self.__AfficheScore.config(text = f'Score: {self.__score}')#diminution du score
            print(self.__count,self.__score)
        
        if self.__count==10 and self.__triche==False :#Défaite au delà de 10 tentatives et sans triche          
           self.__Label.config(text = f'Mot cherché : {self.__motHazard}') 
           self.__AfficheScore.config(text='Score: 0 PERDU')
           for b in self.__boutons:#On affiche les boutons
                b.config(state=DISABLED)   
           
           
           
        if self.__count2==0:#Victoire si mot trouvé
            L=[self.__motHazard,'VICTOIRE ']
            self.__Label.config(text = L) 
            self.__AfficheScore.config(text=f'Score: {self.__score} Saisissez votre Pseudo et appuyez sur Enter')
            self.__Saisie.config(bg='grey',bd=2)
            self.bind('<Down>', self.getPseudo)
    
    
    def getPseudo(self,event): 
        self.__Pseudo = self.__Saisie.get()
        print(self.__Pseudo)
        
    def triche(self,event):#Mode triche, qui permet en appyant sur le bouton down de revenir en arrière         
        if self.__count>0 : self.__count-=1 #Le count ne dois pas devenir négatif
        self.DessinPendu.ListeForme[self.__count].setState("hidden")
        
        self.__score+=100
        if self.__score>1000 : self.__score=1000#le score ne peut pas exéder 1000

    def SaisieTriche(self,event):
   
        #Vérification du code triche puis activation du mode triche 
        self.__entree = self.__Saisie.get()
        if self.__entree=='TRICHE':
            self.__triche=True
            self.bind('<Down>', self.triche)
            
            #Activation de l'interface "TRICHE"
            self.configure(bg='black')
            self.f1.configure(bg='black')
            self.f2.configure(bg='black')
            self.f3.configure(bg='black')
            self.__Saisie=Entry(self.f2,bg='black',fg='red')
            self.__AfficheScore.config(text = f'TRICHE ACTIVEE >:)   Score: {self.__score}',fg='red',bg='black')
            print('Youpi')

    def creerMenuBar(self):
        menuBar=Menu(self)
        menuColors = Menu(menuBar, tearoff=0)
        couleur=Couleur(self,"lightblue","#E6BBAD") #couleurs complémentaires
        menuColors.add_command(label="Bleu ciel et Saumon", command=couleur.clique)
        couleur=Couleur(self,"#FFD700","#ff5700") # couleurs analogues
        menuColors.add_command(label="Or et Rouge", command=couleur.clique)
        couleur=Couleur(self,"#FF6347","#47E3FF") #couleurs complémentaires
        menuColors.add_command(label="Rouge et Bleu", command=couleur.clique)
        couleur=Couleur(self,"#98fb98","#cafb98") # couleurs analogues
        menuColors.add_command(label="Vert", command=couleur.clique)
        self.config(menu=menuColors)

    def change_couleur(self,couleur1,couleur2):
        self.configure(bg=couleur1)
        self.f2.configure(bg=couleur1)
        self.f1.configure(bg=couleur1)
        
        self.DessinPendu.config(bg=couleur2)
        



    def __init__(self):
        Tk.__init__(self)
        self.title('Jeu du pendu')
        self.creerMenuBar()
        self.configure(bg='lightblue') #frame principale
        self.chargeMots()
        self.__triche=False
        self.bind('<Down>', self.SaisieTriche)
        
        
        
        #________ INTERFACE __________#
        
        
        #frame secondaire n°1
        self.f1=Frame(self)
        self.f1.configure(bg ='lightblue')
        self.f1.pack(side = TOP, pady=5)
        
        BoutonNewPartie = Button(self.f1,text="Nouvelle Partie")
        BoutonNewPartie.pack(side=LEFT,padx=5, pady=2)
        BoutonNewPartie.config(command=self.NouvellePartie)
        
        BoutonQuitter = Button(self.f1, text = "Quitter")
        BoutonQuitter.pack(side=LEFT, padx=5, pady=2)
        BoutonQuitter.config(command=self.destroy)
        
        
        #Creation du canevas
        self.DessinPendu = ZoneAffichage(self, 250, 250)
        self.DessinPendu.pack(side=TOP, padx=15, pady=5)
        self.DessinPendu.configure(bg="#E6BBAD")

       # Frame secondaire n° 2, Entrée de la triche, affichage score et mot
        self.f2 = Frame(self) 
        self.f2.configure(bg="lightblue")
        self.f2.pack(side = TOP)
        #la frame contenant les lettres du clavier
        #et le label du mot cherché et le score
        self.__AfficheScore = Label(self.f2, text = 'Jeu du pendu')
        self.__AfficheScore.pack(side=TOP,padx=15,pady=2)  
        
        #label du mot cherché
        self.__Label = Label(self.f2,text = 'Cliquez sur Nouvelle Partie pour jouer' )
        self.__Label.pack(side=TOP,padx=15,pady=10)   
        
        #Entrée pour le code triche et le pseudo en fin de partie 
        self.__Saisie=Entry(self.f2,bg='lightblue',bd=0,state=DISABLED)
        self.__Saisie.pack(side=BOTTOM)
        
        
        #Frame 3, clavier
        self.f3 = Frame(self)
        self.f3.configure(bg="lightblue")
        self.f3.pack(side = TOP)

        count=0 #Mise en place d'un compteur pour pouvoir utiliser l'aide de l'énoncé
        self.__boutons = []
        for i in range(3):#Clavier à travers une grille
            for j in range(7):
                boutonLettre = MonBoutonLettre(self.f3, self,chr(ord('A')+count))
                boutonLettre.config(state=DISABLED)
                count+=1
                self.__boutons.append(boutonLettre)
                boutonLettre.grid(row=i,column=j,padx=2, pady=2)
        for a in range(1,6):
            boutonLettre = MonBoutonLettre(self.f3,self, chr(ord('U')+ a))
            boutonLettre.config(state=DISABLED)
            self.__boutons.append(boutonLettre)
            boutonLettre.grid(row=4,column=a)
            
        
        

        
class MonBoutonLettre(Button):#création d'une classe 
    def __init__(self,parent,fenetre,lettre):
        Button.__init__(self,parent,text=lettre)
        self.__fenetre=fenetre
        self.__lettre=lettre
        self.config(command= self.clic)
        
    def clic(self):
        print(ord(self.__lettre))
        return self.__fenetre.traitement(self.__lettre)


class Couleur: #Création de la classe couleur
    def __init__(self,fenetre,couleur1,couleur2):
        self.__fenetre=fenetre
        self.__couleur1=couleur1
        self.__couleur2=couleur2
    def clique(self):
        self.__fenetre.change_couleur(self.__couleur1,self.__couleur2)
        
#____________________ BDD des Joueurs_________________#
class Joueurs: 
    def __init__(self):
        self.__conn = sqlite3.connect('Joueurs.db')#Le init ouvre l'accès à la base. 
        self.__curseur = self.__conn.cursor()                

    def __del__(self):
        self.__conn.close()
        
    def AjouteJoueur(self):
        nom = getnom()
        #ID = int(nom[i]*10**i for i in range(4)) #L'ID du joueur correspond aux quatres premières lettres de son Pseudo
        pass
        self.__curseur.execute(f"INSERT INTO Joueurs (PSEUDO,Id_Joueurs) VALUES({nom},{ID}")
        self.__conn.commit()
    
    def getnom(self):
        return fen.__Pseudo
        
    def getinfo(self):
        return fen.__score, fen.__motHazard

if __name__ == '__main__':
	fen = FenetrePrincipale()  
fen.geometry('300x550')
fen.mainloop()            

    
    

