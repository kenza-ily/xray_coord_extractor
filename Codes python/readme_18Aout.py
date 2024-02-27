####### IMPORTATIONS
from tkinter import * ; import tkinter as tk
from PIL import ImageTk as itk; from PIL import Image
import subprocess; import os ; 
import cv2
import numpy as np
import pandas as pd;from pandastable import Table,TableModel;
from math import log10  
from PIL import Image
import io
import pathlib


######## OPTIONS
TITLE_FONT = ("Arial", 25, "bold")
violet_bg='#ccb6e4'
white_bg='#FFFFFF' 
V=['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7','T1','T2','T3','T4','T5','T6','T7','T8','T9','T10','T11','T12','L1','L2','L3','L4','L5']
Titre_Application="X-Rays Measurements Tracking Platform"

global radio_var ; radio_var=0


#Directories --> A MODIFIER !!!!
icone='/Users/KenzaBenkirane/Desktop/Skairos/Skairos_logo.ico' 
logo='/Users/KenzaBenkirane/Desktop/Skairos/Skairos_logo.png' 
radios_directory='/Users/KenzaBenkirane/Desktop/Skairos/Radios'



class Application(object):
    # Stores current drawing tool used, current one is "line"
    global drawing_tool

    
    
    def __init__ (self):
        """Construteur de la fenêtre principale"""
        
        #Paramètres de la fenêtre
        self.fen=Tk()
        global frame; frame=self.fen
        self.fen.configure(background='white')
        self.fen.title(Titre_Application)
        self.fen.iconbitmap(icone)
        self.fen.minsize(1000,400)
        
        #Initialisation des frames
        global f; f = tk.Frame(self.fen,bg=white_bg) #frame pour la base de données 
        global f2;f2 = tk.Frame(self.fen,bg=white_bg) #frame pour les boutons
        f.pack(fill='y',expand=0,side='right')
        f2.pack(fill='y',expand=0,side='left')
        
        tk.Label(frame, text="\n Plateforme de suivi d'imageries cliniques", font=("Arial", 20, "bold"),bg=white_bg).pack(fill='x') 
        global Description_bttn; Description_bttn=tk.Label(frame, text="Description \n", font=("Arial", 12, "italic"),bg=white_bg); Description_bttn.pack(expand='yes') 
        
        tk.Label(frame, text="Skairos", font=("Arial", 11, "italic"),bg=white_bg).pack(side='bottom') #foreground = "Red"
        # canvas = Canvas(frame, width = 30, height = 30)      
        # canvas.pack(side='bottom')      
        # img = PhotoImage(file=logo)      
        # canvas.create_image(20,20, anchor=NW, image=img) 


        
        
        self.drawing_tool = "line" #initalisation du drawing_tool : paramètre par défaut : ligne
    
        
        global Start_bttn; Start_bttn= tk.Button(frame,text="Commencer",command=lambda:start(self), bg=white_bg)
        Start_bttn.pack(expand='yes')        
            
        

    global start
    def start(self):
        """Permet de nommer la page de l'application"""
        
        Description_bttn.pack_forget() ; Start_bttn.pack_forget()
        global etapes; 
        etapes=Label(self.fen, text="\n Etape 1 : Parcourir les fichiers pour choisir la radiographie \n Etape 2 : Mettre les points sur la radio \n Etape 3 : Vérifier et valider \n Etape 4 : Enregistrer dans la base de donnée \n", font=("Arial", 12, "bold"),bg=white_bg);etapes.pack(side='top') 
        
        global Parcourir; Parcourir= Button(self.fen,text="Parcourir",command=lambda:openradio(self), bg=white_bg)
        Parcourir.pack()
        
        if radio_var==0:
            Label(self.fen, text=" ", font=("Arial", 12, "bold"),bg=white_bg).pack(side='top');
            global Choisir_Label; Choisir_Label=Label(self.fen, text="Merci de choisir une radiographie afin d'accéder aux étapes suivantes", font=("Arial", 10, "italic"),bg=white_bg)
            Choisir_Label.pack(side='top');Label(self.fen, text=" ", font=("Arial", 12, "bold"),bg=white_bg).pack(side='top');
    
    
    
    global openradio     
    def openradio(self):
        """S'execute lorsque l'on appuie sur le bouton "Parcourir" : affiche l'image, créer les boutons pour choisir les formes à créer et la base de données à afficher """
        
        #Visuel de la page modifié
        Choisir_Label.pack_forget(); etapes.pack_forget(); #On supprime l'explication des étapes
        Parcourir['text'] = 'Changer de radiographie' # "Parcourir" devient "Changer de radiographie" mais conserve la même fonction
        
        
        global Database_bttn
        Database_bttn=Button(frame,text='Afficher le tableau des données \n',bg=white_bg,command=lambda: database(self))
        Database_bttn.pack(); basededonnee=1; 
        
        ##### Ouvrir la radio et l'afficher
        radio_filename = tk.filedialog.askopenfilename(initialdir=radios_directory, title="Select A File", filetypes=(("jpg files", "*.jpg"),("all files", "*.*")))
        radio_img=cv2.imread(radio_filename)
        # b,g,r = cv2.split(radio_img) #Rearrang the color channel
        # radio_img= cv2.merge((r,g,b))
        radio_img_tk= Image.fromarray(radio_img) # Convert the Image object into a TkPhoto object
        radio = itk.PhotoImage(image=radio_img_tk) 
        
        global drawing_area
        drawing_area = tk.Canvas(frame, width=radio.width(), height=radio.height(),bg='black') #à améliorer
        global Image_to_canva;
        Image_to_canva=drawing_area.create_image(0, 0,image=radio,anchor="nw") #Associate the image to the canva
        drawing_area.bind("<Motion>", self.motion)
        drawing_area.bind("<ButtonPress-1>", self.left_but_down)
        drawing_area.bind("<ButtonRelease-1>", self.left_but_up)
        drawing_area.pack(side='top',fill="y")
        
        #Ajout des boutons de contrôle pour choisir la forme à déssiner
        DTool=tk.Label(f2, text="Drawing Tool is : "+self.drawing_tool, font=("Arial", 18),bg=white_bg)
        DTool.pack(side="top")
        Button(f2, text="Lignes",bg=white_bg,command=lambda: setline(self)).pack()
        Button(f2, text="Arc",bg=white_bg,command=lambda: setarc(self)).pack()
        Button(f2, text="Oval",bg=white_bg,command=lambda: setoval(self)).pack()
        Button(f2, text="Rectangle",bg=white_bg,command=lambda: setrectangle(self)).pack()
        Button(f2, text="Point",bg=white_bg,command=lambda: setpoint(self)).pack()
        Label(f2, text="",bg=white_bg).pack()
        Button(f2, text="Crayon",bg=white_bg,command=lambda: setpencil(self)).pack()
        Button(f2, text="Legender les vertèbres",bg=white_bg,command=lambda: settext(self)).pack()

        
        #On initalise les base de données
        global coordo_pointeur; coordo_pointeur=[] #Coordonnées des points
        global coordo_ligne; coordo_ligne=[] #Coordonnées des lignes 
        global coordo_oval; coordo_oval=[] #Coordonnées des cercles : centre du cercle pour l'instant
        global coordo_rectangle; coordo_rectangle=[] #Coordonnées des rectangles
        global coordo_arc; coordo_arc=[] #Coordonnées des arc
        text_indent=0;
        
        Parcourir['command']=changeradio(self)
              
            
    global changeradio  
    def changeradio(self):
        
                
        #On supprime les tracé précédents
        global lines1_bind ; global lines2_bind ; global points ;
        drawing_area.delete(Tk.ALL)
        # drawing_area.delete(lines1_bind)
        # drawing_area .delete(lines2_bind)
        # drawing_area.delete(points)
        # drawing_area.delete(Image_to_canva) #supprime l'image précédente
        
        # #Ajoute la nouvelle image et l'afllcheà la place de l'ancienne
        # radio_filename = tk.filedialog.askopenfilename(initialdir=radios_directory, title="Select A File", filetypes=(("jpg files", "*.jpg"),("all files", "*.*")))
        # radio_img=cv2.imread(radio_filename)
        # b,g,r = cv2.split(radio_img) #Rearrang the color channel
        # radio_img= cv2.merge((r,g,b))
        # radio_img_tk= Image.fromarray(radio_img) # Convert the Image object into a TkPhoto object
        # radio = itk.PhotoImage(image=radio_img_tk) 
        # drawing_area.pack()
        # Image_to_canva=drawing_area.create_image(0, 0,image=radio,anchor="nw") #Associate the image to the canva

        
        # #On réinitalise les tableaux de données
        # coordo_pointeur=[];
            
        
        
 
        # drawing_area.config(width=radio.width(), height=radio.height)


    global df
    
    global setline
    def setline(self):
        self.drawing_tool = "line"
        # self.df=self.df_lines
    
    global setarc
    def setarc(self):
        self.drawing_tool = "arc"
        
    global setoval
    def setoval(self):
        self.drawing_tool = "oval"
     
    global setrectangle
    def setrectangle(self):
        self.drawing_tool = "rectangle"
        # self.df=self.df_rectangle
      
    global settext
    def settext(self):
        self.drawing_tool = "text"
        
    global setpoint
    def setpoint(self):
        self.drawing_tool="point"
        # self.df=self.df_points
        
    global setpencil
    def setpencil(self):
        self.drawing_tool="pencil"
        
        
    # tk.Button(self,)
    # Stores current drawing tool used

 
    # Tracks whether left mouse is down
    left_but = "up"
 
    # x and y positions for drawing with pencil
    x_pos, y_pos = None, None
 
    # Tracks x & y when the mouse is clicked and released
    x1_line_pt, y1_line_pt, x2_line_pt, y2_line_pt = None, None, None, None
 
    # ---------- CATCH MOUSE UP ----------

    def left_but_down(self, event=None):
    #Methode s'executant lorsque l'on appuie sur la souris, qui permet de prendre les premières coordonnées de la ligne/ d'autres formes.
        
        self.left_but = "down"
 
        # Set x & y when mouse is clicked
        self.x1_line_pt = event.x
        self.y1_line_pt = event.y
 
    # ---------- CATCH MOUSE UP ----------

    def left_but_up(self, event=None):
    #Méthode s'executant lorsque l'on lache la souris, qui permet de prendre les coordonnées du point où on lache la souris. 
    
        self.left_but = "up"
 
        # Reset the line
        self.x_pos = None
        self.y_pos = None
 
        # Set x & y when mouse is released
        self.x2_line_pt = event.x
        self.y2_line_pt = event.y
 
        # If mouse is released and line tool is selected
        # draw the line
        if self.drawing_tool == "line":
            self.line_draw(event)
        elif self.drawing_tool == "arc":
            self.arc_draw(event)
        elif self.drawing_tool == "oval":
            self.oval_draw(event)
        elif self.drawing_tool == "rectangle":
            self.rectangle_draw(event)
        elif self.drawing_tool == "text":
            self.text_draw(event)
        elif self.drawing_tool=="point":
            self.pointeur(event)
 
    # ---------- CATCH MOUSE MOVEMENT ----------

    def motion(self, event=None):
 
        if self.drawing_tool == "pencil":
            self.pencil_draw(event)
 
    # ---------- DRAW PENCIL ----------
    
    def pencil_draw(self, event=None):
        if self.left_but == "down":
 
            # Make sure x and y have a value
            if self.x_pos is not None and self.y_pos is not None:
                event.widget.create_line(self.x_pos, self.y_pos,  event.x, event.y, smooth=TRUE,fill="white")
 
            self.x_pos = event.x
            self.y_pos = event.y
 
    # ---------- DRAW LINE ----------

    def line_draw(self, event=None):
 
        # Shortcut way to check if none of these values contain None
        if None not in (self.x1_line_pt, self.y1_line_pt, self.x2_line_pt, self.y2_line_pt):
            event.widget.create_line(self.x1_line_pt, self.y1_line_pt, self.x2_line_pt, self.y2_line_pt, smooth=TRUE, fill="red")
            
            #Database Lignes
            coordo_ligne.append([self.x1_line_pt,self.y1_line_pt, self.x2_line_pt, self.y2_line_pt])
            self.df_lines=pd.DataFrame(coordo_ligne,columns=['x1','y1','x2','y2'])
            self.df=self.df_lines
            
            
    # ---------- DRAW ARC ----------

    def arc_draw(self, event=None):
 
        # Shortcut way to check if none of these values contain None
        if None not in (self.x1_line_pt, self.y1_line_pt, self.x2_line_pt,self.y2_line_pt):
 
            coords = self.x1_line_pt, self.y1_line_pt, self.x2_line_pt,self.y2_line_pt
 
            # start : starting angle for the slice in degrees
            # extent : width of the slice in degrees
            # fill : fill color if needed
            # style : can be ARC, PIESLICE, or CHORD
            event.widget.create_arc(coords, start=0, extent=150,outline='white',
                                    style=ARC)
            
            #Database Arc
            coordo_arc.append([self.x1_line_pt, self.y1_line_pt,self.x2_line_pt, self.y2_line_pt])
            self.df_arc=pd.DataFrame(coordo_arc,columns=['x1','y1','x2','y2'])
            self.df=self.df_arc
 
    # ---------- DRAW OVAL ----------

    def oval_draw(self, event=None):
        if None not in (self.x1_line_pt, self.y1_line_pt, self.x2_line_pt, self.y2_line_pt):
 
            # fill : Color option names are here http://wiki.tcl.tk/37701
            # outline : border color
            # width : width of border in pixels
 
            event.widget.create_oval(self.x1_line_pt, self.y1_line_pt,                                              self.x2_line_pt, self.y2_line_pt,
                                        fill="blue",
                                        outline="white",
                                        width=2)
            
            #Database Cercle
            coordo_oval.append([self.x1_line_pt, self.y1_line_pt])
            self.df_oval=pd.DataFrame(coordo_oval,columns=['x','y'])
            self.df=self.df_oval
 
    # ---------- DRAW RECTANGLE ----------

    def rectangle_draw(self, event=None):
        if None not in (self.x1_line_pt, self.y1_line_pt, self.x2_line_pt,self.y2_line_pt):
 
            # fill : Color option names are here http://wiki.tcl.tk/37701
            # outline : border color
            # width : width of border in pixels
 
            event.widget.create_rectangle(self.x1_line_pt, self.y1_line_pt, self.x2_line_pt, self.y2_line_pt,
                outline="white",
                width=2)
            
            #Database Rectangle
            coordo_rectangle.append([self.x1_line_pt, self.y1_line_pt,self.x2_line_pt, self.y2_line_pt])
            self.df_rectangle=pd.DataFrame(coordo_rectangle,columns=['x1','y1','x2','y2'])
            self.df=self.df_rectangle
 
    # ---------- DRAW TEXT ----------

    def text_draw(self, event=None):
        k=0
        if None not in (self.x1_line_pt, self.y1_line_pt):
                
                event.widget.create_text(self.x1_line_pt, self.y1_line_pt,
                                          fill="white",
                                          font=("Arial", 10),
                                          text=V[k])
                k+=1



    

    # ---------- DRAW POINTS ----------
    
    def pointeur(self,event=None):

        event.widget.create_oval(self.x1_line_pt, self.y1_line_pt,                                              self.x2_line_pt, self.y2_line_pt,
                                        fill="white",
                                        outline="white",
                                        width=1)
        
        #Database Pointeur
        coordo_pointeur.append([self.x1_line_pt, self.y1_line_pt]) #ajoute les coordonnées des points à la liste 
        self.df_points=pd.DataFrame(coordo_pointeur,columns=['x','y'])
        self.df=self.df_points
        

    global database
    def database(self):
        Database_bttn['text'] = 'Mettre les données à jour'

        # if self.drawing_tool=='line':
        #     self.df=self.df_lines
        # if self.drawing_tool=='rectangle':
        #     self.df=self.df_rectangle
        # if self.drawing_tool=='arc':
        #     self.df=self.df_arc
        # if self.drawing_tool=='oval':
        #     self.df=self.df_oval
        # if self.drawing_tool=='points':
        #     self.df=self.df_points
        
        print(self.drawing_tool)
        print(self.df)
        # tk.Label(f, text="Table of the"+self.drawing_tool, font=("Arial", 11),bg=white_bg).pack() 
        self.table = pt = Table(f, dataframe=self.df,
                                showtoolbar=True, showstatusbar=True)
        pt.show()
               
                                  
 #######################################                
appli = Application()
appli.fen.mainloop()
appli.fen.destroy()

# if __name__ == "__main__":
#     appli = Application()
# #    appli.config(background=white_bg) #We can change the background color
#     appli.title(Titre_Application)
#     appli.geometry("400x600")
#     appli.minsize(1000,400)
#     appli.maxsize(2000,1000)
#     appli.iconbitmap(icone)
#     appli.fen.mainloop()
#     appli.fen.destroy()