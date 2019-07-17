import os
import csv
from tkinter import *
# from barcode import generate
# from barcode.writer import ImageWriter
import treepoem


class Application:
    
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "12")
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 50
        self.primeiroContainer.pack()
  
        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 50
        self.segundoContainer.pack()
  
        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 50
        self.terceiroContainer.pack()
  
        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 50
        self.quartoContainer.pack()
  
        self.titulo = Label(self.primeiroContainer, text="Gerador de código de barra")
        self.titulo["font"] = ("Arial", "14", "bold")
        self.titulo.pack()
  
        self.pathfileLabel = Label(self.segundoContainer,text="Local (*csv)", font=self.fontePadrao)
        self.pathfileLabel.pack(side=LEFT)
        self.pathfile = Entry(self.segundoContainer)
        self.pathfile["width"] = 50
        self.pathfile["font"] = ("Calibri", "12")
        self.pathfile.pack(side=LEFT)
  
        self.pathsaveLabel = Label(self.terceiroContainer, text="Local salvar", font=self.fontePadrao)
        self.pathsaveLabel.pack(side=LEFT)
        self.pathsave = Entry(self.terceiroContainer)
        self.pathsave["width"] = 50
        self.pathsave["font"] = ("Calibri", "12")
        self.pathsave.pack(side=LEFT)
  
        self.generator = Button(self.quartoContainer)
        self.generator["text"] = "Executar"
        self.generator["font"] = ("Calibri", "12")
        self.generator["fg"] = "white"
        self.generator["width"] = 20
        self.generator["bg"] = "blue"
        self.generator["command"] = self.create_code
        self.generator.pack()
  
        self.mensagem = Label(self.quartoContainer, text="")
        self.mensagem["font"] = ("Calibri", "12", "italic")
        self.mensagem.pack()

    def check_file(self, diretorio):
        save = self.pathsave.get()
        full_path = save + diretorio
        if not os.path.exists(full_path):
            return False
        return True

    def create_code(self):
        file = self.pathfile.get()
        save = self.pathsave.get()
        try:
            with open(file, 'r', encoding='utf-8') as kit:
                file = csv.reader(kit, delimiter=',', quotechar=',')
                next(file)
                for row in file:
                    dir_exist = self.check_file(row[1])
                    if not dir_exist:
                        os.mkdir(f'{save}/{row[1]}')
                    # generate('EAN13', row[0], writer=ImageWriter(), output=f'{save}/{row[1]}/{row[0]}')
                    image = treepoem.generate_barcode(
                        barcode_type='ean13',
                        data=row[0],
                        options={
                            "includetext": True,
                            "showborder": True
                        }
                    )
                    image.convert('1').save(f'{save}/{row[1]}/{row[0]}.png')
                kit.close()
                self.mensagem["text"] = "Sucesso: Códigos gerados"
                self.mensagem["fg"] = "green"
        except:
            self.mensagem["text"] = "Erro: Local (*csv) sem nome_do_arquivo e extensão .csv"
            self.mensagem["fg"] = "red"


window = Tk()
window.title("EAN13")
Application(window)
window.mainloop()

if __name__ == '__main__':
    Application()
