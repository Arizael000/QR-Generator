import customtkinter as ctk
import qrcode
from PIL import Image, ImageTk
from tkinter import filedialog
import io
import os
import sys
import webbrowser

try:
    from pyzbar.pyzbar import decode
    PYZBAR_INSTALLED = True
except ImportError:
    decode = None
    PYZBAR_INSTALLED = False

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

ACCENT = "#0A84FF"
ACCENT_HOVER = "#0066CC"
BG = "#0B0F19"
CARD = "#151A28"
BORDER = "#1F2738"
TEXT = "#E6EDF7"
MUTED = "#8A94A6"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("QR Generator")
app.geometry("480x760")
app.resizable(True, True)
app.minsize(460, 720)
app.configure(fg_color=BG)

icon_path = resource_path("qr.ico")
if os.path.exists(icon_path):
    try:
        app.iconbitmap(icon_path)
    except Exception:
        pass

img = None
generado = False
imagen_cargada = None
ruta_imagen = None

def generar_qr():
    global img, generado
    texto = entrada.get()
    if texto.strip() == "":
        estado.configure(text="Ingrese un texto o enlace", text_color="#FF6B6B")
        return
    qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=20, border=4)
    qr.add_data(texto)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    img_tk = Image.open(buffer).resize((220, 220))
    tk_img = ImageTk.PhotoImage(img_tk)
    etiqueta_imagen.configure(image=tk_img, text="")
    etiqueta_imagen.image = tk_img
    estado.configure(text="Codigo QR generado", text_color="#4ADE80")
    generado = True
    boton2.pack(pady=(8, 0))

def guardar():
    if generado:
        ruta_guardado = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")], title="Guardar codigo QR como...")
        if ruta_guardado:
            img.save(ruta_guardado)
            estado.configure(text=f"Guardado en: {ruta_guardado}", text_color="#4ADE80")
        else:
            estado.configure(text="No se guardo el archivo", text_color="#FBBF24")

def cargar_imagen_qr():
    global imagen_cargada, ruta_imagen
    ruta = filedialog.askopenfilename(title="Seleccionar imagen con codigo QR", filetypes=[("Imagen", "*.png *.jpg *.jpeg *.bmp *.gif")])
    if not ruta:
        return
    try:
        imagen_cargada = Image.open(ruta).convert("RGB")
        ruta_imagen = ruta
        preview = imagen_cargada.copy()
        preview.thumbnail((240, 240), Image.LANCZOS)
        tk_preview = ImageTk.PhotoImage(preview)
        etiqueta_previa.configure(image=tk_preview, text="")
        etiqueta_previa.image = tk_preview
        boton_leer_qr.configure(state="normal" if PYZBAR_INSTALLED else "disabled")
        estado_lectura.configure(text="Imagen cargada", text_color="#4ADE80")
        texto_resultado.delete("0.0", "end")
    except Exception as e:
        estado_lectura.configure(text=f"Error cargando imagen: {e}", text_color="#FF6B6B")

def leer_qr():
    if not PYZBAR_INSTALLED:
        estado_lectura.configure(text="Instale pyzbar para leer codigos QR", text_color="#FF6B6B")
        return
    if imagen_cargada is None:
        estado_lectura.configure(text="Cargue primero una imagen", text_color="#FF6B6B")
        return
    try:
        resultados = decode(imagen_cargada)
        if not resultados:
            estado_lectura.configure(text="No se encontro un codigo QR", text_color="#FBBF24")
            texto_resultado.delete("0.0", "end")
            return
        texto = "\n\n".join([r.data.decode("utf-8", errors="replace") for r in resultados])
        texto_resultado.delete("0.0", "end")
        texto_resultado.insert("0.0", texto)
        estado_lectura.configure(text="Codigo QR leido", text_color="#4ADE80")
    except Exception as e:
        estado_lectura.configure(text=f"Error al leer QR: {e}", text_color="#FF6B6B")

def mostrar_acerca():
    v = ctk.CTkToplevel(app)
    v.title("Acerca de")
    v.geometry("320x200")
    v.resizable(False, False)
    v.transient(app)
    v.grab_set()
    v.configure(fg_color=BG)
    ctk.CTkLabel(v, text="Generador de Codigo QR\nVersion 0.85", font=("Segoe UI", 16, "bold"), text_color=TEXT).pack(pady=(24, 8))
    ctk.CTkLabel(v, text="Desarrollado por Arizael GC\n(c) 2025\narizogurdian@gmail.com", font=("Segoe UI", 12), text_color=MUTED).pack(pady=8)
    ctk.CTkButton(v, text="Cerrar", command=v.destroy, fg_color=ACCENT, hover_color=ACCENT_HOVER).pack(pady=(8, 16))

def abrir_paypal():
    url = "https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=arizogurdian@gmail.com&currency_code=USD&amount=5.00&item_name=Buy+me+a+coffee"
    webbrowser.open(url)

# Header
header = ctk.CTkFrame(app, fg_color="transparent")
header.pack(fill="x", padx=24, pady=(20, 8))
ctk.CTkLabel(header, text="QR Generator", font=("Segoe UI", 22, "bold"), text_color=TEXT).pack(anchor="w")
ctk.CTkLabel(header, text="Crea y lee codigos QR", font=("Segoe UI", 12), text_color=MUTED).pack(anchor="w")

tabs = ctk.CTkTabview(app, width=412, height=560, fg_color=CARD, segmented_button_fg_color=CARD, segmented_button_selected_color=ACCENT, segmented_button_selected_hover_color=ACCENT_HOVER, segmented_button_unselected_color=CARD, segmented_button_unselected_hover_color=BORDER)
tabs.pack(padx=24, pady=8, fill="both", expand=True)
tabs.add("Crear QR")
tabs.add("Leer QR")

# Crear
panel_crear = tabs.tab("Crear QR")
ctk.CTkLabel(panel_crear, text="Contenido", font=("Segoe UI", 13, "bold"), text_color=TEXT).pack(anchor="w", padx=4, pady=(8, 4))
entrada = ctk.CTkEntry(panel_crear, placeholder_text="Introduce un enlace o texto...", height=40, border_color=BORDER, fg_color=BG)
entrada.pack(padx=4, pady=(0, 12), fill="x")

btn_row = ctk.CTkFrame(panel_crear, fg_color="transparent")
btn_row.pack(fill="x", padx=4)
boton = ctk.CTkButton(btn_row, text="Generar", command=generar_qr, fg_color=ACCENT, hover_color=ACCENT_HOVER, height=40, corner_radius=10)
boton.pack(side="left", fill="x", expand=True, padx=(0, 6))
boton2 = ctk.CTkButton(btn_row, text="Guardar", command=guardar, fg_color=BORDER, hover_color="#2A3448", height=40, corner_radius=10)

etiqueta_imagen = ctk.CTkLabel(panel_crear, text="Vista previa del QR", width=220, height=220, fg_color=BG, corner_radius=12, text_color=MUTED)
etiqueta_imagen.pack(pady=20)
estado = ctk.CTkLabel(panel_crear, text="", font=("Segoe UI", 12), text_color=MUTED)
estado.pack()

# Leer
panel_leer = tabs.tab("Leer QR")
boton_cargar = ctk.CTkButton(panel_leer, text="Cargar imagen", command=cargar_imagen_qr, fg_color=ACCENT, hover_color=ACCENT_HOVER, height=40, corner_radius=10)
boton_cargar.pack(pady=(8, 12), fill="x", padx=4)
etiqueta_previa = ctk.CTkLabel(panel_leer, text="Vista previa de la imagen", width=200, height=200, fg_color=BG, corner_radius=12, text_color=MUTED)
etiqueta_previa.pack(pady=8)
boton_leer_qr = ctk.CTkButton(panel_leer, text="Leer codigo QR", command=leer_qr, state="disabled", fg_color=BORDER, hover_color="#2A3448", height=40, corner_radius=10)
boton_leer_qr.pack(pady=8, fill="x", padx=4)
texto_resultado = ctk.CTkTextbox(panel_leer, width=380, height=90, fg_color=BG, border_color=BORDER, border_width=1, corner_radius=10)
texto_resultado.pack(pady=8, fill="x", padx=4)
texto_resultado.insert("0.0", "El resultado de la lectura aparecera aqui...")
estado_lectura = ctk.CTkLabel(panel_leer, text="", font=("Segoe UI", 12), text_color=MUTED)
estado_lectura.pack()

# Footer
footer = ctk.CTkFrame(app, fg_color="transparent")
footer.pack(fill="x", padx=24, pady=(8, 20))
ctk.CTkButton(footer, text="Acerca de", command=mostrar_acerca, fg_color=BORDER, hover_color="#2A3448", height=36, corner_radius=10).pack(side="left", fill="x", expand=True, padx=(0, 6))
ctk.CTkButton(footer, text="Buy me a coffee", command=abrir_paypal, fg_color="#FFD700", text_color="#000", hover_color="#F0C300", height=36, corner_radius=10).pack(side="left", fill="x", expand=True, padx=(6, 0))

if not PYZBAR_INSTALLED:
    estado_lectura.configure(text="pyzbar no instalado. Instale pyzbar para leer QR.", text_color="#FBBF24")

app.protocol("WM_DELETE_WINDOW", app.destroy)
app.mainloop()
