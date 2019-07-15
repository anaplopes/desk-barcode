import os
import csv
from barcode import generate
from barcode.writer import ImageWriter


def check_file(diretorio):
    path = '/home/alopes/Documentos/EAN13/'
    full_path = path + diretorio
    if not os.path.exists(full_path):
        return False
    return True


def create_code():
    with open('/home/alopes/Documentos/EAN13/kits.csv', 'r') as kit:
        file = csv.reader(kit, delimiter=';', quotechar=';')
        next(file)
        for row in file:
            dir_exist = check_file(row[1])
            if not dir_exist:
                os.mkdir(f'/home/alopes/Documentos/EAN13/{row[1]}')
            barCodeImage = generate('EAN13', row[0], writer=ImageWriter(), output=f'/home/alopes/Documentos/EAN13/{row[1]}/{row[0]}')
        kit.close()


if __name__ == '__main__':
    create_code()
