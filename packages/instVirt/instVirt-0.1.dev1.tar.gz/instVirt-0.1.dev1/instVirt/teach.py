#!/usr/bin/env python3
from tkinter import *
import os
class vteach(Tk):
    def __init__(self):
        os.system('echo "asl-lab (Academia do Software Livre)." &')
        super().__init__()
        super().geometry("280x390")
        super().title("Instrutor virtual")
        self.filename = ""
        self.e = StringVar()
        self.d = StringVar()
        self.lTitle = Label(self, text='Etapas do curso')
        self.lDisc = Label(self, text='Disciplinas do curso')
        self.sbtn = Button(self, text=" Ler", command=self.mtext)
        self.bbtn = Button(self, text=" Narrar", command=self.bvindo)
        self.le = Listbox(self, background="white", height=10, listvariable=self.e)
        self.ld = Listbox(self, background="white", height=4, listvariable=self.d)
        etapas = [ "primeira","segunda","terceira","quarta","quinta","sexta","sétima","oitava","nona","décima" ]
        idx = 0
        for etap in etapas:
            self.le.insert(idx, etap)
            idx+= 1
        disc_items = [  "Matemática", "Eletricidade", "Tecnologia-da-Informação", "Sistemas-Operacionais" ]
        idx= 0
        for item in disc_items:
            self.ld.insert(idx, item)
            idx+= 1

        self.lTitle.place(x=52, y=0)
        self.le.place(x=52, y=20)
        self.lDisc.place(x=52, y=205)
        self.ld.place(x=52, y=225)
        self.sbtn.place(x=52, y=305)
        self.bbtn.place(x=52, y=338)
        pass    
    
    def slivre(self):
        self.filename="/home/asl-teach/ASL-SL/software_livre.txt"
        os.system("clear")
        talkStr = "cat " + self.filename + " | tsurya "
        texto = ""
        f = open(self.filename, "r")
        texto += f.read()
        print(texto)
        os.system(talkStr)
        pass
    
    def bvindo(self):
        self.filename="/home/asl-teach/ASL-SL/boas-vindas.txt"
        os.system("clear")
        talkStr = "cat " + self.filename + " | tbastet "
        texto = ""
        f = open(self.filename, "r")
        texto += f.read()
        print(texto)
        os.system(talkStr)
        pass

    def mtext(self):
        d = StringVar()
        e = StringVar()
        disc = self.ld.get(ACTIVE)
        d.set(disc)
        etapa = self.le.get(ACTIVE)
        e.set(etapa)
        strCmd = "nohup xterm -T Instrutor -e less " + d.get() + "/" + e.get() + "> /dev/null 2>&1"
        os.system(strCmd)

if __name__ == "__main__":
    app = vteach()
    app.mainloop()
