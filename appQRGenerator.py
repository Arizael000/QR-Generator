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

try:
    from pyzbar.pyzbar import decode
    PYZBAR_INSTALLED = True
except ImportError:
    decode = None
    PYZBAR_INSTALLED = False

# Función para compatibilidad con PyInstaller
def resource_path(relative_path):
    """Devuelve la ruta absoluta, incluso si estás usando PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Crear ventana
app = ctk.CTk()
icon_path = resource_path("qr.ico")
if os.path.exists(icon_path):
    try:
        app.iconbitmap(icon_path)
    except Exception as e:
        print(f"No se pudo asignar ícono: {e}")
else:
    print(f"No se encontró qr.ico en: {icon_path}")

app.title("Generador de Código QR 0.5")
app.geometry("400x600")
app.resizable(False, False)

img = None
generado = False
imagen_cargada = None
ruta_imagen = None

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

    etiqueta_imagen.configure(image=tk_img, text="")
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


def cargar_imagen_qr():
    global imagen_cargada, ruta_imagen
    ruta = filedialog.askopenfilename(
        title="Seleccionar imagen con código QR",
        filetypes=[("Imagen", "*.png *.jpg *.jpeg *.bmp *.gif")]
    )
    if not ruta:
        return

    try:
        imagen_cargada = Image.open(ruta).convert("RGB")
        ruta_imagen = ruta

        preview = imagen_cargada.copy()
        preview.thumbnail((250, 250), Image.LANCZOS)
        tk_preview = ImageTk.PhotoImage(preview)
        etiqueta_previa.configure(image=tk_preview, text="")
        etiqueta_previa.image = tk_preview
        boton_leer_qr.configure(state="normal" if PYZBAR_INSTALLED else "disabled")
        estado_lectura.configure(text="✅ Imagen cargada", text_color="green")
        texto_resultado.delete("0.0", "end")
    except Exception as e:
        estado_lectura.configure(text=f"❌ Error cargando imagen: {e}", text_color="red")


def leer_qr():
    if not PYZBAR_INSTALLED:
        estado_lectura.configure(
            text="❌ Instale pyzbar para leer códigos QR desde imágenes", text_color="red"
        )
        return

    if imagen_cargada is None:
        estado_lectura.configure(text="⚠️ Cargue primero una imagen", text_color="red")
        return

    try:
        resultados = decode(imagen_cargada)
        if not resultados:
            estado_lectura.configure(text="⚠️ No se encontró un código QR", text_color="orange")
            texto_resultado.delete("0.0", "end")
            return

        texto = "\n\n".join(
            [resultado.data.decode("utf-8", errors="replace") for resultado in resultados]
        )
        texto_resultado.delete("0.0", "end")
        texto_resultado.insert("0.0", texto)
        estado_lectura.configure(text="✅ Código QR leído", text_color="green")
    except Exception as e:
        estado_lectura.configure(text=f"❌ Error al leer QR: {e}", text_color="red")


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
        "Versión 0.5\n\n"
        "Desarrollado por Arizael GC\n"
        "© 2025\n"
        "Contacto: arizogurdian@gmail.com"
    )

    etiqueta = ctk.CTkLabel(ventana_acerca, text=texto, justify="left", font=("Arial", 12))
    etiqueta.pack(padx=20, pady=20)

    cerrar = ctk.CTkButton(ventana_acerca, text="Cerrar", command=ventana_acerca.destroy)
    cerrar.pack(pady=(0, 10))


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

pestañas = ctk.CTkTabview(app, width=380, height=520)
pestañas.pack(padx=10, pady=10, fill="both", expand=True)

pestañas.add("Crear QR")
pestañas.add("Leer QR")

# Pestaña Crear QR
panel_crear = pestañas.tab("Crear QR")

titulo_crear = ctk.CTkLabel(panel_crear, text="Crear QR", font=("Arial", 18))
titulo_crear.pack(pady=(0, 10))

entrada = ctk.CTkEntry(panel_crear, placeholder_text="Introduce un enlace o texto...")
entrada.pack(padx=20, pady=(0, 10), fill="x")

boton = ctk.CTkButton(panel_crear, text="Generar Código QR", command=generar_qr)
boton.pack(pady=10)

boton2 = ctk.CTkButton(panel_crear, text="Guardar en..", command=guardar)

etiqueta_imagen = ctk.CTkLabel(panel_crear, text="", width=220, height=220, fg_color="#f0f0f0", corner_radius=10)
etiqueta_imagen.pack(pady=20)

estado = ctk.CTkLabel(panel_crear, text="")
estado.pack()

# Pestaña Leer QR
panel_leer = pestañas.tab("Leer QR")

titulo_leer = ctk.CTkLabel(panel_leer, text="Leer QR desde imagen", font=("Arial", 18))
titulo_leer.pack(pady=(0, 10))

boton_cargar = ctk.CTkButton(panel_leer, text="Cargar imagen", command=cargar_imagen_qr)
boton_cargar.pack(pady=10)

etiqueta_previa = ctk.CTkLabel(panel_leer, text="Vista previa de la imagen", width=250, height=250, fg_color="#f0f0f0", corner_radius=10)
etiqueta_previa.pack(pady=10)

boton_leer_qr = ctk.CTkButton(panel_leer, text="Leer Código QR", command=leer_qr, state="disabled")
boton_leer_qr.pack(pady=10)

texto_resultado = ctk.CTkTextbox(panel_leer, width=340, height=280)
texto_resultado.pack(pady=10)
texto_resultado.insert("0.0", "El resultado de la lectura aparecerá aquí...")

estado_lectura = ctk.CTkLabel(panel_leer, text="")
estado_lectura.pack()

# Botón "Acerca de"
boton_acerca = ctk.CTkButton(app, text="Acerca de", command=mostrar_acerca)
boton_acerca.pack(pady=10)

# Botón PayPal
boton_paypal = ctk.CTkButton(app, text="Buy me a coffee ☕", command=abrir_paypal, fg_color="#FFD700", text_color="black", hover_color="#F0C300")
boton_paypal.pack(pady=10)

if not PYZBAR_INSTALLED:
    estado_lectura.configure(text="⚠️ pyzbar no instalado. Instale pyzbar para leer QR desde imágenes.", text_color="orange")

app.protocol("WM_DELETE_WINDOW", app.destroy)
# Ejecutar la app
app.mainloop()


