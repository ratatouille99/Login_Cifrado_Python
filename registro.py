import customtkinter as ctk
from PIL import Image, ImageTk, ImageFont
import os
import tkinter as tk
from conexion import Registro_usuarios
import hashlib
import secrets

carpeta_principal = os.path.dirname(__file__)
carpeta_imagenes = os.path.join(carpeta_principal, "imagenes")
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

Aulas = {
    "Aula 1": 1,
    "Aula 2": 2
}

def cifrar_sha256(password, salt):
    password_salt = password + salt
    hash_object = hashlib.sha256(password_salt.encode())
    hashed_password = hash_object.hexdigest()

    return hashed_password

def cifrar_md5(password, salt):

    password_salt = password + salt
    hash_object = hashlib.md5(password_salt.encode())
    hashed_password = hash_object.hexdigest()

    return hashed_password

class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def option_registro(self):
        self.title("Error!!")
        self.geometry("220x80")

        self.label = ctk.CTkLabel(self, text="El usuario ya existe",font=("Comic Sans MS", 16) )
        self.label.pack(padx=20, pady=20)
    def option_inicio(self):
        self.title("Error!!")
        self.geometry("220x100")

        self.label = ctk.CTkLabel(self, text="El usuario o contraseña\n son incorrectos",font=("Comic Sans MS", 16) )
        self.label.pack(padx=20, pady=20)

def open_toplevel(self, option):
    self.toplevel_window = ToplevelWindow(self)
    if option == 2: 
        self.toplevel_window.option_registro()
    elif option == 1:
        self.toplevel_window.option_inicio()

def toggle_password(txt):
    if txt.cget('show') == '':
        txt.configure(show='*')
    else:
        txt.configure(show='')

def iniciar_sesion(fondo, boton, boton2, app):
    fondo.destroy()
    boton.destroy()
    boton2.destroy()
    
    fondo_sesion = ctk.CTkImage(light_image=Image.open(os.path.join(carpeta_imagenes,"2.png")), size=(400,650))
    et_fondo = ctk.CTkLabel(app, image=fondo_sesion, text=" ")
    et_fondo.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
    
    boton_enviar = Image.open(os.path.join(carpeta_imagenes, "2_1.png"))
    boton_enviar = boton_enviar.resize((250, 80))
    boton_sel = ImageTk.PhotoImage(boton_enviar)

    boton = tk.Button(app, image=boton_sel, command= lambda : sesion_iniciada(et_fondo, boton, boton2, app, entry_pass.get(), entry_usuario.get(),None, optionrol.get(),1), highlightthickness=0, bd=0)
    boton.image = boton_sel
    boton.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
    
    entry_usuario = ctk.CTkEntry(app, placeholder_text="Nombre de usuario", width=300)
    entry_usuario.place(relx=0.1, rely=0.57)
    
    entry_pass = ctk.CTkEntry(app, placeholder_text="Contraseña", width=300)
    entry_pass.place(relx=0.1, rely=0.70)
    
    optionrol = ctk.CTkOptionMenu(app, values=["Estudiante", "Maestro"], command=optionmenu_callback)
    optionrol.place(relx=0.3, rely=0.77)
    
    toggle_password(entry_pass)
    
def registro(fondo, boton, boton2, app):
    fondo.destroy()
    boton.destroy()
    boton2.destroy()

    fondo_sesion = ctk.CTkImage(light_image=Image.open(os.path.join(carpeta_imagenes, "3.png")), size=(400, 650))
    et_fondo = ctk.CTkLabel(app, image=fondo_sesion, text=" ")
    et_fondo.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    boton_enviar = Image.open(os.path.join(carpeta_imagenes, "3_1.png"))
    boton_enviar = boton_enviar.resize((250, 80))
    boton_sel = ImageTk.PhotoImage(boton_enviar)

    # Crear una variable de control para el estado del botón
    estado_boton = tk.BooleanVar()
    estado_boton.set(False)

    def envio_datos():
        sesion_iniciada(et_fondo, boton, boton2, app, entry_pass.get(), entry_usuario.get(), optionmenu.get(), optionrol.get(), 2)

    boton = tk.Button(app, image=boton_sel, command=envio_datos, highlightthickness=0, bd=0, state="disabled")
    boton.image = boton_sel
    boton.place(relx=0.5, rely=0.93, anchor=tk.CENTER)

    entry_usuario = ctk.CTkEntry(app, placeholder_text="Nombre de usuario", width=300)
    entry_usuario.place(relx=0.1, rely=0.55)

    entry_pass = ctk.CTkEntry(app, placeholder_text="Contraseña", width=300)
    entry_pass.place(relx=0.1, rely=0.66)

    optionmenu = ctk.CTkOptionMenu(app, values=["Aula 1", "Aula 2"], command=optionmenu_callback)
    optionmenu.place(relx=0.4, rely=0.73)
    
    optionrol = ctk.CTkOptionMenu(app, values=["Estudiante", "Maestro"], command=optionmenu_callback)
    optionrol.place(relx=0.4, rely=0.81)

    # Vincular la habilitación del botón al estado de los campos de entrada
    entry_usuario.bind("<KeyRelease>", lambda event: check_campos())
    entry_pass.bind("<KeyRelease>", lambda event: check_campos())

    def check_campos():
        estado_boton.set(bool(entry_usuario.get() and entry_pass.get()) and (optionmenu.get() != ' '))
        if estado_boton.get():
            boton.config(state="normal")
        else:
            boton.config(state="disabled")
            
    toggle_password(entry_pass)
    
def sesion_iniciada(fondo, boton, boton2, app, entry_pass, entry_usuario, optionmenu,optionrol, option):
    conex = Registro_usuarios()
    tipo = None
    aula = optionmenu
    rol = optionrol
    salt = None
    
    if optionrol == "Estudiante" and option == 2:
        salt = secrets.token_hex(16)
        tipo  = conex.estudiante(entry_usuario, cifrar_md5(entry_pass,salt), Aulas[optionmenu], salt)
    
    elif optionrol == "Maestro" and option == 2:
        salt = secrets.token_hex(16)
        tipo  = conex.maestro(entry_usuario, cifrar_sha256(entry_pass,salt), Aulas[optionmenu], salt)
    
    elif option == 1 and optionrol == "Maestro":
        salt = conex.obtener_salt_ma(entry_usuario)
        
        if salt != None:
            tipo, aula, rol = conex.sesion_ma(entry_usuario, cifrar_sha256(entry_pass,salt))
        else:
            tipo = False
    
    elif option == 1 and optionrol == "Estudiante":
        salt = conex.obtener_salt_est(entry_usuario)
        
        if salt != None:
            tipo, aula, rol = conex.sesion_est(entry_usuario, cifrar_md5(entry_pass,salt))
        else:
            tipo = False

    if not tipo:
        open_toplevel(app,option)
    
    else:
        fondo.destroy()
        boton.destroy()
        boton2.destroy()
        
        fondo_sesion = ctk.CTkImage(light_image=Image.open(os.path.join(carpeta_imagenes,"4.png")), size=(400,650))
        et_fondo = ctk.CTkLabel(app, image=fondo_sesion, text=" ")
        et_fondo.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        
        nombre_usuario = ctk.CTkLabel(app,text=entry_usuario, font=("Comic Sans MS", 26))
        nombre_usuario.place(relx = 0.4, rely = 0.63)
        
        nombre_aula = ctk.CTkLabel(app,text=str(aula), font=("Comic Sans MS", 26))
        nombre_aula.place(relx = 0.35, rely = 0.83)
        
        tipo_rol = ctk.CTkLabel(app,text=rol, font=("Comic Sans MS", 26))
        tipo_rol.place(relx = 0.35, rely = 0.73)
    
def optionmenu_callback(choice):
    return str(choice)
