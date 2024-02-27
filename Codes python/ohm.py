class Application(object):
    def __init__ (self):
        """Construteur de la fenêtre principale"""
        self.fen=Tk()
        self.fen.title('Code des couleurs')
        self.dessineResistance()
        self.dessineBouton()
        self.codeCouleur = ['black','brown','red','orange','yellow',\
                            'green','blue','purple','grey','white']
    def dessineResistance(self):
        self.can=Canvas(self.fen,bg='ivory',width =500,height=300)
        self.can.grid(row = 1, column = 1, columnspan=3)
        self.can.create_line(10,150,490,150,width = 4)
        self.can.create_rectangle(100,100,400,200,fill='light grey')
        self.ligne=[]
        for i in range(3):
            self.ligne.append(self.can.create_rectangle(130+i*35,\
                                    100,145+i*35,200,fill='black'))
 
    def dessineBouton(self):
        Label(self.fen,text ='Entrez la valeur de la résitance, en ohms :').\
                                            grid(row=2,column=1,columnspan=3)
        #Button(self.fen,text='Montrer',command=self.changeCouleurs).grid(row=3,column=1)
        self.entree=Entry(self.fen,width=14)
        self.entree.grid(row=3,column=2)
        self.entree.bind("<Return>",self.changeCouleurs)
        Button(self.fen,text='Quitter',command=self.fen.quit).\
                                            grid(row=3,column=3)
 
    def changeCouleurs(self,event=None):
        """Mettre event dans la fonction si elle est appelée avec un bind"""
        #test avec enent=None : marche pareil
        self.valEntree=self.entree.get()
        try:
            val=float(self.valEntree)
        except:
            erreur = 1
        else:
            erreur = 0
        if erreur == 1 or val >1e11 or val < 1:
            self.signalErreur()
        else :
            li =[0]*3 # liste des 3 codes à afficher
            if val >= 10:
                logv = int(log10(val)) # partie entière du logarithme
                ordgr = 10**logv # ordre de grandeur
                v_temp = round(val/ordgr*10)
                # extraction du premier chiffre significatif :
                li[0] = int(v_temp/10) # partie entière
                li[1] = v_temp- 10*li[0] # partie décimale
                li[2] = logv -1
            else:
                v_temp=round(val,1)
                li[0]=0
                li[1]=int(v_temp)
                li[2]=int(10*(v_temp-li[1]))
            for i in range(3):
                self.can.itemconfig(self.ligne[i],fill=self.codeCouleur[li[i]])
 
    def signalErreur(self):
        self.entree.config(bg='red')
        self.entree.after(1000,self.videEntree)
 
    def videEntree(self):
        self.entree.config(bg='white')
        self.entree.delete(0,len(self.valEntree))
        for i in range(3):
            self.can.itemconfig(self.ligne[i],fill='black')
 
 
 
 
from tkinter import *   
from math import log10  
appli = Application()
appli.fen.mainloop()
appli.fen.destroy()