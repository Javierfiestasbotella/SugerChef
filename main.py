import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel
from tkinter import ttk
from pathlib import Path
from datetime import date
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from deep_translator import GoogleTranslator
import os
import webbrowser
import ast

# Ruta base
BASE_DIR = Path(__file__).resolve().parent
ESP_FILE = BASE_DIR / 'esp.docx'
ENG_FILE = BASE_DIR / 'eng.docx'
LISTADO_FILE = BASE_DIR / 'listado.docx'
BBDD_FILE = BASE_DIR / 'sugerencias_bbdd.docx'
LOGO_PATH = BASE_DIR / 'logo.jpeg'
ICONO_PATH = BASE_DIR / 'logo.ico'

# Función para cargar sugerencias desde Word
def cargar_sugerencias():
    sugerencias = {}
    if BBDD_FILE.exists():
        doc = Document(BBDD_FILE)
        for p in doc.paragraphs:
            if ':' in p.text:
                try:
                    clave, datos = p.text.split("::", 1) if '::' in p.text else p.text.split(":", 1)
                    clave = int(clave.strip())
                    valores = ast.literal_eval(datos.strip())
                    if isinstance(valores, list) and len(valores) == 3:
                        sugerencias[clave] = valores
                except:
                    continue
    return sugerencias

# Guardar sugerencias en Word
def guardar_bbdd(sugerencias):
    doc = Document()
    for clave, datos in sorted(sugerencias.items()):
        doc.add_paragraph(f"{clave}: {datos}")
    doc.save(BBDD_FILE)

# Traducción
def traducir_a_ingles(texto_es):
    try:
        return GoogleTranslator(source='auto', target='en').translate(texto_es)
    except:
        return texto_es + " (no traducido)"

# Crear sugerencia nueva
def crear_sugerencia():
    sugerencias = cargar_sugerencias()
    ventana = Toplevel()
    ventana.title("Nueva sugerencia")
    if ICONO_PATH.exists(): ventana.iconbitmap(ICONO_PATH)

    frame = tk.Frame(ventana, padx=10, pady=10)
    frame.pack()

    tk.Label(frame, text="Precio (€):").grid(row=0, column=0, sticky="e", pady=5)
    entry_precio = tk.Entry(frame)
    entry_precio.grid(row=0, column=1, pady=5)

    tk.Label(frame, text="Descripción en español:").grid(row=1, column=0, sticky="ne", pady=5)
    text_desc = tk.Text(frame, height=4, width=40)
    text_desc.grid(row=1, column=1, pady=5)

    def guardar():
        try:
            precio = float(entry_precio.get())
            desc_es = text_desc.get("1.0", tk.END).strip()
            desc_en = traducir_a_ingles(desc_es)
            nueva_clave = max(sugerencias.keys(), default=0) + 1
            sugerencias[nueva_clave] = [precio, desc_es, desc_en]
            guardar_bbdd(sugerencias)
            messagebox.showinfo("Éxito", f"Sugerencia {nueva_clave} añadida", parent=ventana)
            ventana.destroy()
        except:
            messagebox.showerror("Error", "Datos inválidos", parent=ventana)

    tk.Button(frame, text="Guardar sugerencia", command=guardar).grid(row=2, columnspan=2, pady=10)

# Modificar sugerencia existente
def modificar_sugerencia():
    sugerencias = cargar_sugerencias()
    clave = simpledialog.askinteger("Modificar sugerencia", "Número de sugerencia a modificar:")
    if not clave or clave not in sugerencias:
        messagebox.showerror("Error", "Número inválido o no existente")
        return

    ventana = Toplevel()
    ventana.title(f"Modificar sugerencia {clave}")
    if ICONO_PATH.exists(): ventana.iconbitmap(ICONO_PATH)

    frame = tk.Frame(ventana, padx=10, pady=10)
    frame.pack()

    tk.Label(frame, text="Precio (€):").grid(row=0, column=0, sticky="e", pady=5)
    entry_precio = tk.Entry(frame)
    entry_precio.insert(0, sugerencias[clave][0])
    entry_precio.grid(row=0, column=1, pady=5)

    tk.Label(frame, text="Descripción en español:").grid(row=1, column=0, sticky="ne", pady=5)
    text_desc = tk.Text(frame, height=4, width=40)
    text_desc.insert("1.0", sugerencias[clave][1])
    text_desc.grid(row=1, column=1, pady=5)

    def guardar():
        try:
            nuevo_precio = float(entry_precio.get())
            nueva_desc_es = text_desc.get("1.0", tk.END).strip()
            nueva_desc_en = traducir_a_ingles(nueva_desc_es)
            sugerencias[clave] = [nuevo_precio, nueva_desc_es, nueva_desc_en]
            guardar_bbdd(sugerencias)
            messagebox.showinfo("Modificado", f"Sugerencia {clave} modificada con éxito")
            ventana.destroy()
        except:
            messagebox.showerror("Error", "Datos inválidos", parent=ventana)

    tk.Button(frame, text="Guardar cambios", command=guardar).grid(row=2, columnspan=2, pady=10)

# Crear menú Word
def crear_menu():
    sugerencias = cargar_sugerencias()
    seleccion = simpledialog.askstring("Menú", "Números de sugerencia (ej: 1,2,3):")
    if not seleccion:
        return

    indices = [int(i.strip()) for i in seleccion.split(",") if i.strip().isdigit() and int(i.strip()) in sugerencias]
    hoy = date.today().isoformat()
    output_dir = BASE_DIR / 'menus'
    output_dir.mkdir(exist_ok=True)

    plantilla_esp = Document(ESP_FILE)
    plantilla_eng = Document(ENG_FILE)

    for idx, num in enumerate(indices):
        precio, desc_es, desc_en = sugerencias[num]
        for doc, texto, precio_str in [
            (plantilla_esp, desc_es, f"{precio}€"),
            (plantilla_eng, desc_en, f"{precio}€")]:

            p = doc.add_paragraph()
            run_texto = p.add_run(f"- {texto} - ")
            run_precio = p.add_run(precio_str)
            for r in [run_texto, run_precio]:
                r.font.name = 'Georgia'
                r._element.rPr.rFonts.set(qn('w:eastAsia'), 'Georgia')
                r.font.size = Pt(12)
            run_precio.bold = True
            color = RGBColor(0, 0, 0) if idx % 2 == 0 else RGBColor(0, 0, 255)
            run_texto.font.color.rgb = color
            run_precio.font.color.rgb = color
            p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            doc.add_paragraph("")

    plantilla_esp.save(output_dir / f"esp_{hoy}.docx")
    plantilla_eng.save(output_dir / f"eng_{hoy}.docx")
    messagebox.showinfo("Menú creado", "Menús Word generados correctamente")

# Imprimir listado completo
def imprimir_listado():
    sugerencias = cargar_sugerencias()
    if not sugerencias:
        messagebox.showwarning("Aviso", "No hay sugerencias guardadas.")
        return

    doc = Document()
    doc.add_heading("Listado completo de sugerencias", 0)
    for clave, (precio, desc_es, desc_en) in sorted(sugerencias.items()):
        p = doc.add_paragraph()
        run = p.add_run(f"{clave}. {desc_es}\n{desc_en} - {precio}€")
        run.font.name = 'Georgia'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Georgia')
        run.font.size = Pt(11)
        p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    doc.save(LISTADO_FILE)
    messagebox.showinfo("Listado generado", "Listado completo guardado correctamente")

# Interfaz principal
def interfaz():
    root = tk.Tk()
    root.title("SugerChef - La Chancla")
    root.geometry("500x620")
    root.configure(bg="#E6F2FA")
    if ICONO_PATH.exists(): root.iconbitmap(ICONO_PATH)

    frame = tk.Frame(root, bg="#E6F2FA")
    frame.pack()

    if LOGO_PATH.exists():
        from PIL import Image, ImageTk
        logo_img = Image.open(LOGO_PATH).resize((160, 100))
        logo = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(frame, image=logo, bg="#E6F2FA")
        logo_label.image = logo
        logo_label.pack(pady=10)

    tk.Label(frame, text="Sistema de Sugerencias del Chef", font=("Georgia", 16, "bold"), bg="#E6F2FA", fg="#005B96").pack(pady=5)

    botones = [
        ("Crear sugerencia nueva", crear_sugerencia),
        ("Modificar sugerencia existente", modificar_sugerencia),
        ("Crear menú en Word", crear_menu),
        ("Imprimir listado completo", imprimir_listado),
        ("Salir", root.quit)
    ]
    for texto, comando in botones:
        tk.Button(frame, text=texto, command=comando, font=("Georgia", 12), bg="#B3DAF1", fg="#003E6B", width=40).pack(pady=6)

    root.mainloop()

if __name__ == "__main__":
    interfaz()
