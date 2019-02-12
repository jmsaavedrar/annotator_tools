# -*- coding: utf-8 -*-
#!/usr/bin/python3
"""
Created on Wed Jan  9 17:46:19 2019

@author: Core i7
"""
import os, glob
import tkinter as tk
import cv2
from PIL import ImageTk, Image

class App:
    def __init__(self, path_images='', path_output=''):
        self.path_images = path_images
        self.path_output = path_output
        self.faltantes = []
        self.counter = -1
        self.current_filename = ''
        self.current_img = None
    
    def load_files(self):
        """Guarda en una lista las imágenes faltantes"""
        self.path_images = ent_path_images.get().strip()
        self.path_output = ent_path_output.get().strip()
        if self.path_images == '' or self.path_output == '':
            print('Error: Seleccione carpeta de entrada y salida')
            return
        self.faltantes = self.get_faltantes(self.path_images, self.path_output)
        self.counter = -1
        if len(self.faltantes) == 0:
            label_filename.delete(0, tk.END)
            label_filename.insert(0, 'Procesadas todas las imágenes')
        else:
            self.next_img()
    
    def get_faltantes(self, path_images, path_output):
        """Obtiene imagenes faltantes para anotar"""
        faltantes = []
        os.chdir(path_images)
        types = ('*.png', '*.bmp', '*.jpg', '*.tif')
        files_grabbed = []
        for files in types:
            files_grabbed.extend(glob.glob(files))
        img_files = files_grabbed
        with open(path_output, 'r') as file: 
            images_ready = [line.split('\t')[0] for line in file] 
        images_ready = [f.split('.')[0] for f in images_ready]
        for img_file in img_files:
            basename = img_file.split('.')[0]
            if basename not in images_ready:
                faltantes.append(img_file)
        return faltantes
    
    def load_img(self, filename):
        """Carga la imagen"""
        canvas.delete("all")
        if filename != '':
            path_img = os.path.join(self.path_images, filename)
            app.current_img = get_img(path_img)
            canvas.create_image(0, 0, image = self.current_img, anchor = "nw")
            ent_car.delete(0, tk.END)

    def next_img(self):
        """Procesa siguiente imagen"""
        total = len(self.faltantes)
        if total == 0:
            filename = ''
            txt_label = 'Procesadas todas las imágenes'
            ent_car.delete(0, tk.END)
        else:
            self.counter = (self.counter + 1) % total
            filename = app.faltantes[app.counter]
            txt_label = filename
        self.current_filename = filename
        label_filename.delete(0, tk.END)
        label_filename.insert(0, txt_label)
        self.load_img(filename)
        
    def generar_anotacion(self):
        """Genera la anotación (output)"""
        annotation = ent_car.get().strip()
        if annotation == '' or 'Error' in annotation:
            print_msg('Error: Genere la anotación primero')
            return
        elif self.current_filename == '':
            print_msg('Error: Cargue imagen primero')
            return
        with open(self.path_output, 'a') as f: 
            f.write("%s\t%s\n" % (self.current_filename, annotation))
        self.faltantes.pop(app.counter)
        if app.counter >= len(app.faltantes):
            app.counter = 0
        self.next_img()
    
    
def print_msg(msg):
    """Muestra un mensaje en la caja de texto de salida"""
    #print(msg)
    ent_car.delete(0, tk.END)
    ent_car.insert(0, msg)

    
def get_img(path_img):
    """Muestra imagen"""
    image = cv2.imread(path_img, 0)
    width_img = image.shape[1]
    height_img = image.shape[0]
    scale_img = min(WIDTH_CANVAS / width_img, HEIGHT_CANVAS / height_img)
    dim = (int(width_img * scale_img), int(height_img * scale_img))
    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    return image    


WIDTH_APP = 700 # ancho app
HEIGHT_APP = 400 # alto app
WIDTH_CANVAS = 600 # ancho canvas
HEIGHT_CANVAS = 200 # alto canvas

path_images0 = 'C:\\Users\\Core i7\\Desktop\\deep learning\\programas\\codigos\\YOLO-data\\\images'
path_output0 = 'C:\\Users\\Core i7\\Desktop\\deep learning\\programas\\codigos\\YOLO-data\\annotations.txt'

app = App()

root = tk.Tk()
root.title('Generador de Anotaciones')
root.geometry('%dx%d+0+0' % (WIDTH_APP, HEIGHT_APP))

canvas = tk.Canvas(root, width=WIDTH_CANVAS, height=HEIGHT_CANVAS)
canvas.grid(row=3, column=0, columnspan=4, sticky='nsew')

label_path_images = tk.Label(root, text= 'Path de carpeta imagenes:', font = "Calibri 11")
label_path_images.grid(row=0, column=0, sticky='w', padx=10)

ent_path_images = tk.Entry(root, font = "Calibri 11")
ent_path_images.grid(row=0, column=1, columnspan=3, sticky='nsew')
ent_path_images.insert(0, path_images0)

label_path_output = tk.Label(root, text= 'Path de archivo salida:', font = "Calibri 11")
label_path_output.grid(row=1, column=0, sticky='w', padx=10)

ent_path_output = tk.Entry(root, font = "Calibri 11")
ent_path_output.grid(row=1, column=1, columnspan=3, sticky='nsew')
ent_path_output.insert(0, path_output0)

label_filename = tk.Entry(root, text= 'Seleccione carpetas de entrada y salida', bg='gray94', font = "Calibri 12")
label_filename.grid(row=2, column=1, columnspan=3, sticky='nsew', pady=10)

botton_load = tk.Button(root, text='Cargar', fg="black", font = "bold 16", command=app.load_files)
botton_load.grid(row=0, column=5, rowspan=2, columnspan=3, sticky='nsew', padx=10)

label_car = tk.Label(root, text= 'Número:', font = "Calibri 16")
label_car.grid(row=4, column=0, sticky='w', padx=10)

ent_car = tk.Entry(root, font = "Calibri 16")
ent_car.grid(row=4, column=1, columnspan=3, sticky='nsew', padx=10)

botton_next = tk.Button(root, text='Siguiente', font = "bold 16", command=app.next_img)
botton_next.grid(row=5, column=0, columnspan=1, sticky='nsew', pady=10)

botton_save = tk.Button(root, text='Guardar', font = "bold 16", command=app.generar_anotacion)
botton_save.grid(row=5, column=1, columnspan=3, sticky='nsew', pady=10)

root.mainloop()

