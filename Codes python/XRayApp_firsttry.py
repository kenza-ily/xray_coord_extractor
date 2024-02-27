####### IMPORTATIONS
from pandastable import Table #,TableModel
from tkinter import *
import tkinter as tk
from PIL import ImageTk as itk
#from matplotlib import style
import subprocess
from PIL import Image
import os
import cv2
import numpy as np


################ OPTIONS
TITLE_FONT = ("Arial", 25, "bold")
violet_bg='#ccb6e4'
white_bg='#FFFFFF' 
icone='/Users/KenzaBenkirane/Desktop/Skairos/Skairos_logo.ico' #à modifier  !!!!!
logo='/Users/KenzaBenkirane/Desktop/Skairos/Skairos_logo.jpg' # à modifier!!!!
radios_directory='/Users/KenzaBenkirane/Desktop/Skairos/Radios'
global radio
radio=None
cross_color=(255,255,255)
V=['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7','T1','T2','T3','T4','T5','T6','T7','T8','T9''T10','T11','T12','L1','L2','L3','L4','L5']
Titre_Application="X-Rays Measurements Tracking Platform"
from numpy import *


import pandas as pd;from pandastable import Table,TableModel;
import pandas as pd



#####################################################################################################################
#                       APP CREATING
###############################################################################################################################################################

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        Pages_List=[StartPage, SaisiInfo,DataBase] #à modifier si besoin
        self.frames = {}
        for F in Pages_List: #dont forget to add the different pages
            frame = F(container, self)
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(SaisiInfo)

    def show_frame(self, c):
        frame = self.frames[c]
        frame.tkraise()

#####################################################################################################################
#                       PAGE D'ACCUEIL
###############################################################################################################################################################

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg=white_bg)
        StartPage_frame=tk.Frame(self,bg=white_bg)
        
        

        # logo_image=itk.PhotoImage(file=logo)
        # canvasStart = tk.Canvas(StartPage_frame, width=logo_image.width(), height=logo_image.height()) #à améliorer
        # canvasStart.pack()
        # canvasStart.create_image(0, 0,image=radio,anchor="nw")
   
        
        label = tk.Label(StartPage_frame, text="Plateforme de suivi d'imageries cliniques", font=("Arial", 30, "bold"),bg=white_bg) #foreground = "Red"
        label.pack(side="top")
        tk.Label(StartPage_frame,bg=white_bg, text="Welcome to the 2020 Software enabling you to track X-Rays measurements",font=("Arial", 15)).pack()
        tk.Button(StartPage_frame, text="Evaluer une radiographie",bg=white_bg,command=lambda: controller.show_frame(SaisiInfo)).pack(side="top")
        tk.Button(StartPage_frame, text="Accéder à la base de données",bg=white_bg,command=lambda: controller.show_frame(DataBase)).pack(side="top")
        StartPage_frame.pack(expand=True)

        
#####################################################################################################################
#                       PAGE DE TRAITEMENT DE RADIOS
###############################################################################################################################################################

class SaisiInfo(tk.Frame): #Login page

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg=white_bg)
        self.controller=controller
        global SaisiInfo_frame 
        SaisiInfo_frame=tk.Frame(self,bg=white_bg)
        
        
        
        
############ BASES DE LA PAGE
        
    #################### Scrollbar
        canvas=tk.Canvas(SaisiInfo_frame,bg=white_bg)
        canvas.config(scrollregion=canvas.bbox('all'))
        yscrollbar = tk.Scrollbar(self,orient='vertical')
        xscrollbar = tk.Scrollbar(self,orient='horizontal')
        yscrollbar.config(command=canvas.yview)
        xscrollbar.config(command=canvas.xview)
        
        SaisiInfo_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=SaisiInfo_frame, anchor="nw")
        
        canvas.configure(xscrollcommand=xscrollbar.set,yscrollcommand=yscrollbar.set)
        # canvas.pack(side="left", fill="both", expand=True)
        yscrollbar.pack( side = 'right', fill = 'y')
        xscrollbar.pack( side = 'bottom', fill = 'x')
        


    ################### Titres
        space=tk.Label(SaisiInfo_frame, text=" ", font=("Arial", 12, "bold"),bg=white_bg)
        tk.Label(SaisiInfo_frame, text=" ", font=("Arial", 25, "bold"),bg=white_bg).pack(side="top");tk.Label(SaisiInfo_frame, text="Plateforme de suivi d'imageries cliniques", font=("Arial", 25, "bold"),bg=white_bg).pack(side="top");tk.Label(SaisiInfo_frame, text=" ", font=("Arial", 25, "bold"),bg=white_bg).pack(side="top")
        global Enregistrer
        Enregistrer= tk.Button(SaisiInfo_frame,text="Enregistrer les données",bg=white_bg)
        

        
    ################### Fonction naming : nomme les differentes étapes
        global naming 
        def naming(self):
            global label1; global label2 ; global label3 ;global Etape1
            space.pack();
            label1=tk.Label(SaisiInfo_frame, text="Etape 2 : Mettre les points sur la radio", font=("Arial", 12, "bold"),bg=white_bg);label1.pack(side='top');space.pack(side='top')
            label2=tk.Label(SaisiInfo_frame, text="Etape 3 : Vérifier et valider ", font=("Arial", 12, "bold"),bg=white_bg);label2.pack(side='top');space.pack(side='top')
            label3=tk.Label(SaisiInfo_frame, text="Etape 4 : Enregistrer dans la base de données", font=("Arial", 12, "bold"),bg=white_bg);label3.pack(side='top');space.pack(side='top')
            if radio==None:
                tk.Label(SaisiInfo_frame, text=" ", font=("Arial", 12, "bold"),bg=white_bg).pack(side='top');Etape1=tk.Label(SaisiInfo_frame, text="Merci de choisir une radiographie afin d'accéder aux étapes suivantes", font=("Arial", 10, "italic"),bg=white_bg)
                Etape1.pack(side='top');tk.Label(SaisiInfo_frame, text=" ", font=("Arial", 12, "bold"),bg=white_bg).pack(side='top');
            else: #cas où une radio a été selectionnée
                Enregistrer.pack()
                
                
                
                
                
                
                
                
########## ETAPE 2 : TRAITEMENT D'IMAGE 
        #L'étape 2 doit être processed avant l'étape 1 car il faut definir les fonctions qui font être appliquées sur l'image avant de définir l'image. La numérotation des étapes est temporelle,  mais l'ordre du code est selon l'ordre de definition des objets.
        
        
    ################### Légende au fur et à mesure que l'on ajoute les données        
        
        # for i in range(len(V)):
        #     text_draw(self,event,V[i])
            
        
        # def text_draw(self, event=None,vertebrate):
        # if None not in (self.x1_line_pt, self.y1_line_pt):
        #     # Show all fonts available
        #     print(tkinter.font.families())
 
        #     text_font = tkinter.font.Font(family='Helvetica',
        #     size=20, weight='bold', slant='italic')
 
        #     event.widget.create_text(self.x1_line_pt, self.y1_line_pt,
        #                               fill="green",
        #                               font=text_font,
        #                               text=vertebrate)
        
        
        
        
        
        
        
        
        
        
        
    ##################### Pointeur 
        coordo_pointeur=[]
        def paint(event):
                 color='red'

                 
                 #Option Pointage
                 x1_p,y1_p=(event.x-1),(event.y-1)
                 coordo_pointeur.append([x1_p,y1_p]) #ajoute les coordonnées des points à la liste 
                 x2_p,y2_p=(event.x+1),(event.y+1)
                 canvas_radio.create_oval(x1_p,y1_p,x2_p,y2_p,fill=color,outline=color)
                 
                 #Option Ligne : pointer les coins des vertèbres dans l'ordre suivant : supérieur gauche, supérieur droite, inférieur gauche, inferieur droite
                 
        
                 #Creer une base de données (dataframe df) à partir de la liste. 
                 #df_points=pd.DataFrame(coordo_pointeur,columns=['Vertèbres','Supérieure gauche','Supérieure droite','Inférieure Gauche','Inférieure droite'],index =['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7','T1','T2','T3','T4','T5','T6','T7','T8','T9''T10','T11','T12','L1','L2','L3','L4','L5'])

                 
                 


    ##################### Traceur de Lignes 
        
        self.drawing_tool = "pencil"
        self.left_but = "up"
        coordo_lignes=[]
        # x and y positions for drawing with pencil
        self.x_pos, self.y_pos = None, None
        # Tracks x & y when the mouse is clicked and released
        self.x1_line_pt, self.y1_line_pt, self.x2_line_pt, self.y2_line_pt = None, None, None, None
        
        
        # ---------- CATCH MOUSE DOWN ----------
        
        def left_but_down(self, event=None):
            self.left_but = "down"
     
            # Set x & y when mouse is clicked
            self.x1_line_pt = event.x
            self.y1_line_pt = event.y
 
        # ---------- CATCH MOUSE UP ----------
 
        def left_but_up(self, event=None):
            self.left_but = "up"
     
            # Reset the line
            self.x_pos = None
            self.y_pos = None
     
            # Set x & y when mouse is released
            self.x2_line_pt = event.x
            self.y2_line_pt = event.y

            
            
            if self.drawing_tool=='line':
                line_draw(event)
 
        
        def motion(self, event=None):
 
             if self.drawing_tool=="pencil":
                 self.pencil_draw(event)
 
        # ---------- DRAW PENCIL ----------
 
        def pencil_draw(self, event=None):
            if self.left_but == "down":
     
                # Make sure x and y have a value
                if self.x_pos is not None and self.y_pos is not None:
                    event.widget.create_line(self.x_pos, self.y_pos,  event.x, event.y, smooth='true')
     
                self.x_pos = event.x
                self.y_pos = event.y
           
            
        def line_draw(self, event=None):
 
        # Shortcut way to check if none of these values contain None
            if None not in (self.x1_line_pt, self.y1_line_pt, self.x2_line_pt, self.y2_line_pt):
                event.widget.create_line(self.x1_line_pt, self.y1_line_pt, self.x2_line_pt, self.y2_line_pt, smooth='true', fill="green")
                
                coordo_lignes.append([self.x1_line_pt,self.y1_line_pt]) #ajout à la df
                coordo_lignes.append([self.x2_line_pt,self.y2_line_pt]) #ajout à la df
        
        
        
        #df_points=pd.DataFrame(coordo_pointeur,columns=['Vertèbres','Supérieure gauche','Supérieure droite','Inférieure Gauche','Inférieure droite'],index =['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7','T1','T2','T3','T4','T5','T6','T7','T8','T9''T10','T11','T12','L1','L2','L3','L4','L5'])

 
    
 
################## ETAPE 1 
        #L'étape 2 doit être processed avant l'étape 1 car il faut definir les fonctions qui font être appliquées sur l'image avant de définir l'image. La numérotation des étapes est temporelle,  mais l'ordre du code est selon l'ordre de definition des objets.
        
        
        tk.Label(SaisiInfo_frame, text="Etape 1 : Parcourir les fichiers pour choisir la radiographie", font=("Arial", 12, "bold"),bg=white_bg).pack(side='top') 
        Parcourir= tk.Button(SaisiInfo_frame,text="Parcourir",command=lambda:openradio(self), bg=white_bg)
        Parcourir.pack()
        naming(self)
        
        ################# OpenRadio : Fonction d'ouverture de fichier --> Associée au bouton Parcourir
        global openradio
        def openradio(self):
            global radio #permet à l'image "radio" d'être reconnu aussi en dehors de la fonction
            radio_filename = tk.filedialog.askopenfilename(initialdir=radios_directory, title="Select A File", filetypes=(("jpg files", "*.jpg"),("all files", "*.*")))
            radio_img=cv2.imread(radio_filename)
            #Rearrang the color channel
            b,g,r = cv2.split(radio_img)
            radio_img= cv2.merge((r,g,b))
            
            
            
            # Convert the Image object into a TkPhoto object
            radio_img_tk= Image.fromarray(radio_img)
            radio = itk.PhotoImage(image=radio_img_tk) 
            
            ##### CREATE A CANVA TO HOST THE IMAGE
            global canvas_radio
            canvas_radio = tk.Canvas(SaisiInfo_frame, width=radio.width(), height=radio.height(),bg='black') #à améliorer
            canvas_radio.pack(expand='yes',fill='both')
            
            
            
            #Associate the image to the canva
            canvas_radio.create_image(0, 0,image=radio,anchor="nw") 
            
            
            ##### LINK THE PAINTING FUNCTIONS 
            
            #Pointage 
            #canvas_radio.bind('<B1-Motion>',paint)
            
            
            #Lignes
            canvas_radio.bind("<B1-Motion>", motion)
            canvas_radio.bind("<ButtonPress-1>", self.left_but_down)
            canvas_radio.bind("<ButtonRelease-1>", self.left_but_up)
            
            
            
            
            
                        
            Parcourir['text'] = 'Changer de radiographie'
            Etape1.pack_forget()
            space.pack_forget()
            label1.pack_forget();label2.pack_forget();label3.pack_forget();
            
        
            
         
            
         
            
         
        
###############Etape 3 : Vérifier et valider 
        
        
###############Etape 4 : Enregistrer dans la base de données
        
        
        
      
        
        SaisiInfo_frame.pack();
        tk.Button(self, text="Go to the Welcome Page",bg=white_bg,command=lambda: controller.show_frame(StartPage)).pack(side="bottom")

        
#####################################################################################################################
#                       BASES DE DONNÉES
###############################################################################################################################################################

class DataBase(tk.Frame): 

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg=white_bg)
        
        global DataBase_frame
        DataBase_frame=tk.Frame(self,bg=white_bg)
    
        
        tk.Label(SaisiInfo_frame, text="",bg=white_bg,font=('Arial',11)) .pack();
   
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