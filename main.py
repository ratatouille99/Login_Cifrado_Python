import customtkinter as ctk
from PIL import Image, ImageTk, ImageFont
import os
import tkinter as tk
from registro import *


carpeta_principal = os.path.dirname(__file__)
carpeta_imagenes = os.path.join(carpeta_principal, "imagenes")
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x650")
app.title("Ingreso de usuario")

# Utiliza CTkImage directamente con la ruta de la imagen
fondo = ctk.CTkImage(light_image=Image.open(os.path.join(carpeta_imagenes,"1.png")), size=(400,650))
et_fondo = ctk.CTkLabel(app, image=fondo, text=" ")
et_fondo.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

boton_sesion = Image.open(os.path.join(carpeta_imagenes, "1_1.png"))
boton_sesion = boton_sesion.resize((300, 100))
boton_sel = ImageTk.PhotoImage(boton_sesion)

boton = tk.Button(app, image=boton_sel, command= lambda : iniciar_sesion(et_fondo, boton, boton2,app), highlightthickness=0, bd=0)
boton.image = boton_sel
boton.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

boton_registro = Image.open(os.path.join(carpeta_imagenes, "1_2.png"))
boton_registro = boton_registro.resize((300, 100))
boton_sel = ImageTk.PhotoImage(boton_registro)

boton2 = tk.Button(app, image=boton_sel, command= lambda : registro(et_fondo, boton, boton2,app), highlightthickness=0, bd=0)
boton2.image = boton_sel
boton2.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

app.mainloop()
