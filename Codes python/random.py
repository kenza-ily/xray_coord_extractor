

#Saisi d'informations 

label = tk.Label(SaisiInfo_frame, text="Personal Informations", font=TITLE_FONT,bg=white_bg)
        label.pack(side="top", fill="x", pady=10)
        global optionv
        self.optionv = tk.StringVar()
        t1 = tk.Label(SaisiInfo_frame, text="Account: ",font=('Arial',11,'bold'),bg=white_bg)
        self.v = tk.StringVar()
        self.v.set("")
        global entry1
        entry1 = tk.Entry(SaisiInfo_frame, textvariable=self.v)
        t2 = tk.Label(SaisiInfo_frame,text="\nPassword: ",font=('Arial',11,'bold'),bg=white_bg)
        self.pwd = tk.StringVar()
        self.pwd.set("")
        global entry2
        entry2 = tk.Entry(SaisiInfo_frame, textvariable=self.pwd)
        entry2.config(show="*")
        
        t1.pack();entry1.pack();
        t2.pack();entry2.pack();
        tk.Label(SaisiInfo_frame, text="",bg=white_bg,font=('Arial',11)) .pack();