import os
import csv
import treepoem
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter.filedialog import askopenfilename, askdirectory


class Application:
    
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "12")
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 20
        self.primeiroContainer.pack()
  
        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()
  
        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()
  
        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()

        self.quintoContainer = Frame(master)
        self.quintoContainer["pady"] = 20
        self.quintoContainer.pack()

        self.sextoContainer = Frame(master)
        self.sextoContainer["pady"] = 20
        self.sextoContainer.pack()
  
        self.titulo = Label(self.primeiroContainer, text="Gerador de código")
        self.titulo["font"] = ("Arial", "14", "bold")
        self.titulo.pack()

        self.barcode_type = Label(self.segundoContainer, text="Tipo barcode", font=self.fontePadrao)
        self.barcode_type.pack(side=LEFT)
        self.barcode_type = Entry(self.segundoContainer)
        self.barcode_type["width"] = 10
        self.barcode_type["font"] = ("Calibri", "12")
        self.barcode_type.pack(side=RIGHT)
  
        self.pathfileLabel = Label(self.terceiroContainer, text="Local (*csv)", font=self.fontePadrao)
        self.pathfileLabel.pack(side=LEFT)
        self.pathfile = Entry(self.terceiroContainer)
        self.pathfile["width"] = 50
        self.pathfile["font"] = ("Calibri", "12")
        self.pathfile.pack(side=LEFT)

        self.search_path_file = Button(self.terceiroContainer)
        self.search_path_file["text"] = "Localiza Arquivo"
        self.search_path_file["width"] = 15
        self.search_path_file["command"] = self.open_explore_file
        self.search_path_file["fg"] = "black"
        self.search_path_file.pack(side=RIGHT, padx=10, pady=10)
  
        self.pathsaveLabel = Label(self.quartoContainer, text="Local salvar", font=self.fontePadrao)
        self.pathsaveLabel.pack(side=LEFT)
        self.pathsave = Entry(self.quartoContainer)
        self.pathsave["width"] = 50
        self.pathsave["font"] = ("Calibri", "12")
        self.pathsave.pack(side=LEFT)

        self.search_path_dir = Button(self.quartoContainer)
        self.search_path_dir["text"] = "Localizar diretorio"
        self.search_path_dir["width"] = 15
        self.search_path_dir["command"] = self.open_explore_dir
        self.search_path_dir.pack(side=RIGHT, padx=10, pady=10)
  
        self.generator = Button(self.quintoContainer)
        self.generator["text"] = "Executar"
        self.generator["font"] = ("Calibri", "12")
        self.generator["fg"] = "white"
        self.generator["width"] = 20
        self.generator["bg"] = "blue"
        self.generator["command"] = self.create_code
        self.generator.pack()
  
        # self.mensagem = Label(self.quartoContainer, text="")
        # self.mensagem["font"] = ("Calibri", "12", "italic")
        # self.mensagem.pack()

        self.progress = Progressbar(self.sextoContainer, orient="horizontal", maximum=100, mode="determinate")

    def open_explore_file(self):
        filename = askopenfilename()
        self.pathfile.delete(0, END)
        self.pathfile.insert(0, filename)

    def open_explore_dir(self):
        directory = askdirectory()
        self.pathsave.delete(0, END)
        self.pathsave.insert(0, directory)

    def progress_bar(self, current_value, count_lines):
        percent = (current_value * 100) / count_lines
        self.progress["value"] = percent
        self.progress.update()

    def count_lines(self, file):
        return sum(1 for row in open(file)) - 1

    def check_file(self, local_save, diretorio):
        full_path = f'{local_save}/{diretorio}'
        if not os.path.exists(full_path):
            return False
        return True

    def create_code(self):
        self.progress.pack(side=TOP, ipadx=100)
        file = self.pathfile.get()
        local_save = self.pathsave.get()
        code = self.barcode_type.get()
        count_lines = self.count_lines(file)
        current_value = 1
        try:
            with open(file, 'r', encoding='utf-8') as kit:
                file = csv.reader(kit, delimiter=';', quotechar=';')
                next(file)
                for row in file:
                    dir_exist = self.check_file(local_save, row[1])
                    if not dir_exist:
                        os.mkdir(f'{local_save}/{row[1]}')
                    image = treepoem.generate_barcode(barcode_type=code, data=row[0], options={"includetext": True})
                    image.convert('1').save(f'{local_save}/{row[1]}/{row[0]}.png')
                    current_value += 1
                    self.progress.after(1000, self.progress_bar(current_value=current_value, count_lines=count_lines))
                kit.close()
                messagebox.showinfo("Sucesso", "Códigos gerados!")
        except Exception as e:
            messagebox.showerror("Alert de Erro", str(e))


if __name__ == '__main__':
    window = Tk()
    window.title("Treepoem")
    Application(window)
    window.mainloop()
