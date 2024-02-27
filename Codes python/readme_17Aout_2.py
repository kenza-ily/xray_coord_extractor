####### IMPORTATIONS
from tkinter import * ; import tkinter as tk
from PIL import ImageTk as itk; from PIL import Image
import subprocess; import os ; 
import cv2
import numpy as np
import pandas as pd;from pandastable import Table,TableModel;


######## OPTIONS
TITLE_FONT = ("Arial", 25, "bold")
violet_bg='#ccb6e4'
white_bg='#FFFFFF' 
V=['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7','T1','T2','T3','T4','T5','T6','T7','T8','T9''T10','T11','T12','L1','L2','L3','L4','L5']
Titre_Application="X-Rays Measurements Tracking Platform"
global radio ; radio=None



#Directories --> A MODIFIER !!!!
icone='/Users/KenzaBenkirane/Desktop/Skairos/Skairos_logo.ico' 
logo='/Users/KenzaBenkirane/Desktop/Skairos/Skairos_logo.jpg' 
radios_directory='/Users/KenzaBenkirane/Desktop/Skairos/Radios'



#####################################################################################################################
#                       APP CREATING
###############################################################################################################################################################

class SampleApp(tk.Tk):
    def __init__(self):
        # self.fen=Tk()
        tk.Tk.__init__(self)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        Pages_List=[StartPage, SaisiInfo,DataBase] #à modifier si besoin
        self.frames = {}
        for F in Pages_List: #dont forget to add the different pages
            frame = F(container, self)
            self.frames[F] = frame;

            frame.grid(row=0, column=0, sticky="nsew")

        #self.show_frame(StartPage)
        self.show_frame(SaisiInfo)

    def show_frame(self, c):
        frame = self.frames[c]
        frame.tkraise()

#####################################################################################################################
#                       PAGE D'ACCUEIL
###############################################################################################################################################################

class StartPage(tk.Frame):
#Page d'accueil 
    
    def __init__(self, parent, controller):
    #Construction de la page d'accueil, avec le logo, et les deux boutons permettant d'acceder au traitement des radios et à la base de données
        
        tk.Frame.__init__(self, parent,bg=white_bg)
        StartPage_frame=tk.Frame(self,bg=white_bg)
        
        
        ####### AFFICHAGE DU LOGO EN PAGE D'ACCUEIL
        # logo_img=cv2.imread(logo) ; b,g,r = cv2.split(logo_img)
        # logo_img= cv2.merge((r,g,b)) # Convert the Image object into a TkPhoto object
        # logo_img_tk= Image.fromarray(logo_img); logo_photoimage = itk.PhotoImage(image=logo_img_tk) 
        # global canvas_logo
        # canvas_logo = tk.Canvas(self, width=logo_photoimage.width(), height=logo_photoimage.height(),bg='black') #à améliorer
        # canvas_logo.pack(expand='yes')
        # Image_to_canva=canvas_logo.create_image(0, 0,image=logo_photoimage,anchor="nw") 
        #########
        
        label = tk.Label(StartPage_frame, text="Plateforme de suivi d'imageries cliniques", font=("Arial", 30, "bold"),bg=white_bg) #foreground = "Red"
        label.pack(side="top")
        tk.Label(StartPage_frame,bg=white_bg, text="Welcome to the 2020 Software enabling you to track X-Rays measurements",font=("Arial", 15)).pack()
        tk.Button(StartPage_frame, text="Evaluer une radiographie",bg=white_bg,command=lambda: controller.show_frame(SaisiInfo)).pack(side="top")
        tk.Button(StartPage_frame, text="Accéder à la base de données",bg=white_bg,command=lambda: controller.show_frame(DataBase)).pack(side="top")
        StartPage_frame.pack(expand=True)

        
#####################################################################################################################
#                       PAGE DE TRAITEMENT DE RADIOS
###############################################################################################################################################################

class SaisiInfo(tk.Frame): 
 #Page d'entrée des informations sur les radios 

    def __init__(self, parent, controller):
        """Constructeur de la fenêtre Saisiinfo"""
        tk.Frame.__init__(self, parent,bg=white_bg)
        self.controller=controller
        
        space=tk.Label(self, text=" ", font=("Arial", 12, "bold"),bg=white_bg)
        tk.Label(self, text="Plateforme de suivi d'imageries cliniques", font=("Arial", 20, "bold"),bg=white_bg).pack(side="top");
        
        
############ BASES DE LA PAGE
        


    
        

        
    ################### Fonction naming : nomme les differentes étapes
    
    global naming 
    def naming(self):
        global etape1; global etape2; global etape3 ; global etape4 ;global Etape1
        space.pack();
        etape1=tk.Label(self, text="Etape 1 : Parcourir les fichiers pour choisir la radiographie", font=("Arial", 12, "bold"),bg=white_bg);etape1.pack(side='top') 
        etape2=tk.Label(self, text="Etape 2 : Mettre les points sur la radio", font=("Arial", 12, "bold"),bg=white_bg);etape2.pack(side='top');space.pack(side='top')
        etape3=tk.Label(self, text="Etape 3 : Vérifier et valider ", font=("Arial", 12, "bold"),bg=white_bg);etape3.pack(side='top');space.pack(side='top')
        etape4=tk.Label(self, text="Etape 4 : Enregistrer dans la base de données", font=("Arial", 12, "bold"),bg=white_bg);etape4.pack(side='top');space.pack(side='top')
        if radio==None:
            tk.Label(self, text=" ", font=("Arial", 12, "bold"),bg=white_bg).pack(side='top');
            Etape1=tk.Label(self, text="Merci de choisir une radiographie afin d'accéder aux étapes suivantes", font=("Arial", 10, "italic"),bg=white_bg)
            Etape1.pack(side='top');tk.Label(self, text=" ", font=("Arial", 12, "bold"),bg=white_bg).pack(side='top');

                
                
                
                
                
                
                
########## ETAPE 2 : TRAITEMENT D'IMAGE 
        #L'étape 2 doit être processed avant l'étape 1 car il faut definir les fonctions qui font être appliquées sur l'image avant de définir l'image. La numérotation des étapes est temporelle,  mais l'ordre du code est selon l'ordre de definition des objets.
        
        

        
        
        
        
    ##################### Pointeur 
        global coordo_pointeur #Initialise la liste où l'on mettera les coordonnées des points
        coordo_pointeur=[]
        global df_points
        
        
        
        def pointeur(event):
                 color_points='blue'

                 
                 #Option Pointage
                 x1_p,y1_p=(event.x-1),(event.y-1)
                 coordo_pointeur.append([x1_p,y1_p]) #ajoute les coordonnées des points à la liste 
                 x2_p,y2_p=(event.x+1),(event.y+1)
                 canvas_radio.create_oval(x1_p,y1_p,x2_p,y2_p,fill=color_points,outline=color_points)
                 
                 
                 df_points=pd.DataFrame(coordo_pointeur,columns=['x','y'])
                 
                 # df_points=pd.DataFrame(coordo_pointeur,columns=['Vertèbres','Supérieure gauche','Supérieure droite','Inférieure Gauche','Inférieure droite'],index =['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7','T1','T2','T3','T4','T5','T6','T7','T8','T9''T10','T11','T12','L1','L2','L3','L4','L5'])
        
        
                 


    
 
################## ETAPE 1 
        #L'étape 2 doit être processed avant l'étape 1 car il faut definir les fonctions qui font être appliquées sur l'image avant de définir l'image. La numérotation des étapes est temporelle,  mais l'ordre du code est selon l'ordre de definition des objets.
        
        
        Parcourir= tk.Button(self,text="Parcourir",command=lambda:openradio(self), bg=white_bg)
        Parcourir.pack()
        naming(self)
        
        ################# OpenRadio : Fonction d'ouverture de fichier --> Associée au bouton Parcourir
        global openradio
        def openradio(self):
            
            
            # if radio != None : 
            #     radio_filename2 = tk.filedialog.askopenfilename(initialdir=radios_directory, title="Select A File", filetypes=(("jpg files", "*.jpg"),("all files", "*.*")))
            #     can_image.itemconfigure(img, image=radio_filename2)
            # else:
                
                
            #Visuel de la page modifié
            Etape1.pack_forget()
            space.pack_forget()
            etape1.pack_forget(); etape2.pack_forget();etape3.pack_forget();etape4.pack_forget();
            
            #Ajout des boutons de contrôle 
            DTool.pack(side="top")
            tk.Button(self, text="Set line",bg=white_bg,command=lambda: setline(self)).pack(side='left')
            tk.Button(self, text="Set arc",bg=white_bg,command=lambda: setarc(self)).pack(side='left')
            tk.Button(self, text="Set oval",bg=white_bg,command=lambda: setoval(self)).pack(side='left')
            tk.Button(self, text="Set rectangle",bg=white_bg,command=lambda: setrectangle(self)).pack(side='left')
            tk.Button(self, text="Set text",bg=white_bg,command=lambda: settext(self)).pack(side='left')

            
            # #Cas où on ouvre une radio pour la première fois : supprime les points, ligne et image pour faire la place pour la nouvelle
            # if radio!=None:
            #     global lines1_bind ; global lines2_bind ; global points ; global Image_to_canva;
            #     canvas.delete(lines1_bind)
            #     canvas.delete(lines2_bind)
            #     canvas.delete(points)
            #     canvas.delete(Image_to_canva)
            
            ##### Ouvrir la radio et l'afficher
            # global radio
            radio_filename = tk.filedialog.askopenfilename(initialdir=radios_directory, title="Select A File", filetypes=(("jpg files", "*.jpg"),("all files", "*.*")))
            radio_img=cv2.imread(radio_filename)
            #Rearrang the color channel
            b,g,r = cv2.split(radio_img)
            radio_img= cv2.merge((r,g,b))
            # Convert the Image object into a TkPhoto object
            radio_img_tk= Image.fromarray(radio_img)
            radio = itk.PhotoImage(image=radio_img_tk) 
            #Creating the canva hosting the image
            global canvas_radio
            canvas_radio = tk.Canvas(self, width=radio.width(), height=radio.height(),bg='black') #à améliorer
            canvas_radio.pack()
            #Associate the image to the canva
            Image_to_canva=canvas_radio.create_image(0, 0,image=radio,anchor="nw") 



                    
                
            
            
            
            
            ####### LINK THE FUNCTIONS
            
            #Pointage 
            points = canvas_radio.bind('<B1-Motion>',pointeur)

            #Initialisation avec un objet
            # a=SaisiInfo(12,controller)

            #Detection des mouvements de la souris
            canvas_radio.bind("<Motion>", self.motion)
            lines1_bind =canvas_radio.bind("<ButtonPress-1>", self.left_but_down)
            lines2_bind=canvas_radio.bind("<ButtonRelease-1>", self.left_but_up)
            
            
            
            ####### DESIGN
            #Changements visuels et initialisation de la base de données
            Parcourir['text'] = 'Changer de radiographie'
            #initilise les coordonnées du pointeur

            
            
            
         
                
                
                
            
        
            
         
            
         
            
         
        
###############Etape 3 : Vérifier et valider 
        
        
###############Etape 4 : Enregistrer dans la base de données
        global basededonnee; basededonnee=0;
        
        def database(self):
            
            Database_Button.pack(side='top'); basededonnee=1;
            df_points=pd.DataFrame(coordo_pointeur,columns=['x','y'])
            Database_Button['text'] = 'Mettre les données à jour'
            
            global df
            df=df_points
            f = Frame(self)
            f.pack(fill='both',expand=1)
            self.table = pt = Table(f, dataframe=df,
                                    showtoolbar=True, showstatusbar=True)
            pt.show()
            pt.redraw()
            
           
        global Database_Button
        Database_Button=tk.Button(self,text='Afficher les données',bg=white_bg,command=lambda: database(self))
        Database_Button.pack(side='top')
        self.pack();
        tk.Button(self, text="Go to the Welcome Page",bg=white_bg,command=lambda: controller.show_frame(StartPage)).pack(side="bottom")
    
    # Stores current drawing tool used, current one is "line"
    global drawing_tool
    drawing_tool = "line" #valeur par défaut
    
    global DTool
    DTool=tk.Label(container, text="Drawing Tool is : "+drawing_tool, font=("Arial", 18),bg=white_bg)
       
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
 
    # ---------- CATCH MOUSE MOVEMENT ----------
 
    def motion(self, event=None):
 
        if self.drawing_tool == "pencil":
            self.pencil_draw(event)
 
    # ---------- DRAW PENCIL ----------
 
    def pencil_draw(self, event=None):
        if self.left_but == "down":
 
            # Make sure x and y have a value
            if self.x_pos is not None and self.y_pos is not None:
                event.widget.create_line(self.x_pos, self.y_pos,                        event.x, event.y, smooth=TRUE)
 
            self.x_pos = event.x
            self.y_pos = event.y
 
    # ---------- DRAW LINE ----------
 
    def line_draw(self, event=None):
 
        # Shortcut way to check if none of these values contain None
        if None not in (self.x1_line_pt, self.y1_line_pt, self.x2_line_pt, self.y2_line_pt):
            event.widget.create_line(self.x1_line_pt, self.y1_line_pt, self.x2_line_pt, self.y2_line_pt, smooth=TRUE, fill="green")
 
    # ---------- DRAW ARC ----------
 
    def arc_draw(self, event=None):
 
        # Shortcut way to check if none of these values contain None
        if None not in (self.x1_line_pt, self.y1_line_pt, self.x2_line_pt,                              self.y2_line_pt):
 
            coords = self.x1_line_pt, self.y1_line_pt, self.x2_line_pt,                                  self.y2_line_pt
 
            # start : starting angle for the slice in degrees
            # extent : width of the slice in degrees
            # fill : fill color if needed
            # style : can be ARC, PIESLICE, or CHORD
            event.widget.create_arc(coords, start=0, extent=150,
                                    style=ARC)
 
    # ---------- DRAW OVAL ----------
 
    def oval_draw(self, event=None):
        if None not in (self.x1_line_pt, self.y1_line_pt, self.x2_line_pt,self.y2_line_pt):
 
            # fill : Color option names are here http://wiki.tcl.tk/37701
            # outline : border color
            # width : width of border in pixels
 
            event.widget.create_oval(self.x1_line_pt, self.y1_line_pt, fill="midnight blue",
                                        outline="yellow",
                                        width=2)
 
    # ---------- DRAW RECTANGLE ----------
 
    def rectangle_draw(self, event=None):
        if None not in (self.x1_line_pt, self.y1_line_pt, self.x2_line_pt,self.y2_line_pt):
 
            # fill : Color option names are here http://wiki.tcl.tk/37701
            # outline : border color
            # width : width of border in pixels
 
            event.widget.create_rectangle(self.x1_line_pt, self.y1_line_pt, self.x2_line_pt, self.y2_line_pt,
                fill="midnight blue",
                outline="yellow",
                width=2)
 
    # ---------- DRAW TEXT ----------
 
    def text_draw(self, event=None):
        if None not in (self.x1_line_pt, self.y1_line_pt):
            # Show all fonts available
            print(tkinter.font.families())
 
            text_font = tkinter.font.Font(family='Helvetica',
            size=20, weight='bold', slant='italic')
 
            event.widget.create_text(self.x1_line_pt, self.y1_line_pt,
                                      fill="green",
                                      font=text_font,
                                      text="WOW")
        
#####################################################################################################################
#                       BASES DE DONNÉES
###############################################################################################################################################################

class DataBase(tk.Frame): 

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg=white_bg)
        
        global DataBase_frame
        DataBase_frame=tk.Frame(self,bg=white_bg)
    
        
        tk.Label(self, text="",bg=white_bg,font=('Arial',11)) .pack();
   
        DataBase_frame.pack(expand=True);
        tk.Button(self, text="Go to the Welcome Page",bg=white_bg,command=lambda: controller.show_frame(StartPage)).pack(side="bottom")



        


########################################################################################################################################################## 
##############################################################################################################################################################
##############################################################################################################################################################
##############################################################################################################################################################
if __name__ == "__main__":
    app = SampleApp()
#    app.config(background=white_bg) #We can change the background color
    app.title(Titre_Application)
    app.geometry("400x600")
    app.minsize(1000,400)
    app.maxsize(2000,1000)
    app.iconbitmap(icone)
    app.mainloop()