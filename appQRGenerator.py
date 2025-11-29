import customtkinter as ctk
import qrcode
from PIL import Image, ImageTk
from tkinter import filedialog
import io
import os
import sys
import shutil
import tempfile
import webbrowser

def extraer_icono_a_temp(nombre_archivo="qr.ico"):
    """Copia el ícono a la carpeta TEMP del sistema"""
    temp_dir = tempfile.gettempdir()
    destino = os.path.join(temp_dir, nombre_archivo)

    try:
        shutil.copyfile(resource_path(nombre_archivo), destino)
    except Exception as e:
        print(f"Error al extraer ícono a TEMP: {e}")
        return None

    return destino


# Función para compatibilidad con PyInstaller
def resource_path(relative_path):
    """Devuelve la ruta absoluta, incluso si estás usando PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Extraer ícono al iniciar
ico_path = extraer_icono_a_temp()

# Crear ventana
app = ctk.CTk()
if ico_path:
    try:
        app.iconbitmap(ico_path)
    except Exception as e:
        print(f"No se pudo asignar ícono: {e}")

app.title("Generador de Código QR 0.2")
app.geometry("400x600")
app.resizable(False, False)

img = 0
generado = False

# Función para generar QR
def generar_qr():
    global img, generado
    texto = entrada.get()
    if texto.strip() == "":
        estado.configure(text="⚠️ Ingrese un texto o enlace", text_color="red")
        return

    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=4,
    )
    qr.add_data(texto)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    img_tk = Image.open(buffer)
    img_tk = img_tk.resize((200, 200))
    tk_img = ImageTk.PhotoImage(img_tk)

    etiqueta_imagen.configure(image=tk_img)
    etiqueta_imagen.image = tk_img
    estado.configure(text="✅ Código QR generado", text_color="green")
    generado = True
    boton2.pack(pady=10)

def guardar():
    if generado:
        ruta_guardado = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
            title="Guardar código QR como..."
        )
        if ruta_guardado:
            img.save(ruta_guardado)
            estado.configure(text=f"✅ Guardado en: {ruta_guardado}", text_color="green")
        else:
            estado.configure(text="❌ No se guardó el archivo", text_color="orange")

def mostrar_acerca():
    ventana_acerca = ctk.CTkToplevel(app)
    ventana_acerca.title("Acerca de")
    ventana_acerca.geometry("300x180")
    ventana_acerca.resizable(False, False)

    ventana_acerca.transient(app)
    ventana_acerca.grab_set()

    if ico_path:
        try:
            ventana_acerca.iconbitmap(ico_path)
            ventana_acerca.icono_ref = ico_path 
        except Exception as e:
            print(f"Error al asignar ícono a ventana 'Acerca de': {e}")

    texto = (
        "Generador de Código QR\n"
        "Versión 0.1\n\n"
        "Desarrollado por Arizael GC\n"
        "© 2025\n"
        "Contacto: arizogurdian@gmail.com"
    )

    etiqueta = ctk.CTkLabel(ventana_acerca, text=texto, justify="left", font=("Arial", 12))
    etiqueta.pack(padx=20, pady=20)

    cerrar = ctk.CTkButton(ventana_acerca, text="Cerrar", command=ventana_acerca.destroy)
    cerrar.pack(pady=(0, 10))

def eliminar_icono_temp():
    try:
        if os.path.exists(ico_path):
            os.remove(ico_path)
    except:
        pass

def abrir_paypal():
    paypal_email = "arizogurdian@gmail.com" 
    amount = "5.00"
    currency = "USD"
    item_name = "Buy me a coffee"
    
    url = f"https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business={paypal_email}&currency_code={currency}&amount={amount}&item_name={item_name}"
    webbrowser.open(url)



# Widgets
titulo = ctk.CTkLabel(app, text="Generador de Código QR", font=("Arial", 20))
titulo.pack(pady=20)

entrada = ctk.CTkEntry(app, placeholder_text="Introduce un enlace o texto...")
entrada.pack(padx=20, pady=10, fill="x")

boton = ctk.CTkButton(app, text="Generar Código QR", command=generar_qr)
boton.pack(pady=10)

boton2 = ctk.CTkButton(app, text="Guardar en..", command=guardar)

etiqueta_imagen = ctk.CTkLabel(app, text="")
etiqueta_imagen.pack(pady=20)

estado = ctk.CTkLabel(app, text="")
estado.pack()

# Botón "Acerca de"
boton_acerca = ctk.CTkButton(app, text="Acerca de", command=mostrar_acerca)
boton_acerca.pack(pady=10)

# Botón PayPal
boton_paypal = ctk.CTkButton(app, text="Buy me a coffee ☕", command=abrir_paypal, fg_color="#FFD700", text_color="black", hover_color="#F0C300")
boton_paypal.pack(pady=10)
app.protocol("WM_DELETE_WINDOW", lambda: (eliminar_icono_temp(), app.destroy()))
# Ejecutar la app
app.mainloop()


