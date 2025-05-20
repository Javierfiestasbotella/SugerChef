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




# Ruta base
BASE_DIR = Path(__file__).resolve().parent
ESP_FILE = BASE_DIR / 'esp.docx'
ENG_FILE = BASE_DIR / 'eng.docx'
LISTADO_FILE = BASE_DIR / 'listado.docx'
LOGO_PATH = BASE_DIR / 'logo.jpeg'
ICONO_PATH = BASE_DIR / 'logo.ico'
sugerencias={
    1: [12.95, "Espárragos gratinados con holandesa y jamón", "Gratinated asparagus with hollandaise and ham"],
    2: [14.95, "Salteado de setas variadas con piñones caramelizados, queso curado y brotes de ajo", "Sautéed mixed mushrooms with caramelized pine nuts, aged cheese and garlic sprouts"],
    3: [11.95, "Rollito vietnamita con langostinos panko, aguacate, mango y mezclum", "Vietnamese roll with panko prawns, avocado, mango and mixed greens"],
    4: [13.95, "Solomillo de cerdo con salsa de arándanos y puré de patata", "Pork tenderloin with cranberry sauce and mashed potatoes"],
    5: [13.95, "Secreto con salsa de queso manchego y puré de patatas", "Secreto pork with Manchego cheese sauce and mashed potatoes"],
    6: [12.95, "Cous cous especiado, acompañado de pinchitos de cordero", "Spiced couscous with lamb skewers"],
    7: [18.95, "Pata de pulpo en tempura con puré de patata y aceite de pimentón", "Octopus leg in tempura with mashed potatoes and paprika oil"],
    8: [13.95, "Brioche de carrillera al vino tinto con salsa de queso de cabra y cebolla caramelizada", "Brioche with red wine pork cheek, goat cheese sauce and caramelized onion"],
    9: [14.95, "Flamenquín de serrano y parmesano", "Flamenquín of serrano ham and parmesan"],
    10: [17.95, "Bacalao con pisto", "Cod with Spanish ratatouille (pisto)"],
    11: [14.95, "Pan bao de pato, pimiento encurtido, lombarda, mayonesa, garrapiñados y brote de ajo", "Duck bao bun with pickled pepper, red cabbage, mayo, candied nuts and garlic sprouts"],
    12: [13.95, "Pan bao de rejo, rúcula y alioli", "Octopus bao bun with arugula and aioli"],
    13: [13.95, "Langostinos al curry con fideos de arroz", "Curry prawns with rice noodles"],
    14: [17.95, "Salmón con shiitake y espárragos salteados", "Salmon with shiitake mushrooms and sautéed asparagus"],
    15: [12.95, "Brochetas de pavo especiado con tabulé de verduras", "Spiced turkey skewers with vegetable tabbouleh"],
    16: [11.95, "Bocata de presa marinada en cítricos y salsa kimchi", "Sandwich of citrus-marinated pork shoulder with kimchi sauce"],
    17: [17.95, "Steak tartar de vaca madurada con salsa chipotle y encurtidos", "Matured beef steak tartare with chipotle sauce and pickles"],
    18: [17.95, "Secreto ibérico con miso y puré Robuchon", "Iberian pork with miso and Robuchon-style purée"],
    19: [15.95, "Flamenquín relleno de duxelle de setas y viruta de parmesano", "Flamenquín stuffed with mushroom duxelles and parmesan shavings"],
    20: [7.95, "Gazpacho de cereza con peta zeta de lima", "Cherry gazpacho with lime popping candy"],
    21: [14.95, "Porra con huevo y jamón", "Thick gazpacho (porra) with egg and ham"],
    22: [14.95, "Buñuelos de alga wakame y gamba cristal", "Wakame seaweed and tiny shrimp fritters"],
    23: [14.95, "Tartar de salchichón de Málaga en brioche", "Málaga-style salchichón tartare in brioche"],
    24: [17.95, "Poke de atún, wakame, aguacate, arroz y mango", "Tuna poke with wakame, avocado, rice and mango"],
    25: [6.95, "Taco de merluza con aguacate, cebolla y mango", "Hake taco with avocado, onion and mango"],
    26: [14.95, "Buñuelos de alga wakame y gamba cristal", "Wakame seaweed and tiny shrimp fritters"],
    27: [16.95, "Tosta de hojaldre caramelizado con tartar de atún, aliñado con Kimchi puro, lima y cebolleta china.", "Caramelized puff pastry toast with tuna tartare, pure kimchi, lime and spring onion"],
    28: [13.95, "Empanadas de carne acompañadas de salsa criolla y chimichurri.", "Meat empanadas with criolla sauce and chimichurri"],
    29: [17.95, "Salmón con piel de almendra sobre tagliatelle con salsa parmesana.", "Almond-crusted salmon on tagliatelle with parmesan sauce"],
    30: [18.95, "Merluza en salsa verde con guisantes y gambones crujientes", "Hake in green sauce with peas and crispy prawns"]


}

# Traducción
# me gustaria en una 3 o 4 versión poder ponerle en vez de google translate utilizar la api de Deepl

def traducir_a_ingles(texto_es):
    try:
        return GoogleTranslator(source='auto', target='en').translate(texto_es)
    except:
        return texto_es + " (no traducido)"

# Crear nueva sugerencia
# queda pendiente crear los icon de cada ventana nueva al crear sugerencia
def crear_sugerencia():
    ventana = Toplevel()
    ventana.title("Nueva sugerencia")
    if ICONO_PATH.exists(): ventana.iconbitmap(ICONO_PATH)

    tk.Label(ventana, text="Precio (€):").pack(pady=5)
    entry_precio = tk.Entry(ventana)
    entry_precio.pack(pady=5)

    tk.Label(ventana, text="Descripción en español:").pack(pady=5)
    text_desc = tk.Text(ventana, height=4, width=50)
    text_desc.pack(pady=5)

    def guardar():
        try:
            precio = float(entry_precio.get())
            desc_es = text_desc.get("1.0", tk.END).strip()
            desc_en = traducir_a_ingles(desc_es)
            nueva_clave = max(sugerencias.keys(), default=0) + 1
            sugerencias[nueva_clave] = [precio, desc_es, desc_en]
            messagebox.showinfo("Éxito", f"Sugerencia {nueva_clave} añadida", parent=ventana)
            ventana.destroy()
        except:
            messagebox.showerror("Error", "Datos inválidos", parent=ventana)

    tk.Button(ventana, text="Guardar sugerencia", command=guardar).pack(pady=10)

# Crear menú Word
# añadir el icon tambien en la ventana de precios
def crear_menu():
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

# Modificar sugerencia

def modificar_sugerencia():
    ventana = Toplevel()
    ventana.title("Modificar sugerencia")
    if ICONO_PATH.exists(): ventana.iconbitmap(ICONO_PATH)

    clave = simpledialog.askinteger("Modificar", "Número de sugerencia a modificar:", parent=ventana)
    if clave not in sugerencias:
        messagebox.showerror("Error", "No existe esa sugerencia", parent=ventana)
        return
    opcion = simpledialog.askinteger("Modificar", "1. Precio\n2. Descripción en español", parent=ventana)
    if opcion == 1:
        nuevo_precio = float(simpledialog.askstring("Nuevo precio", "Introduce el nuevo precio (€):", parent=ventana))
        sugerencias[clave][0] = nuevo_precio
    elif opcion == 2:
        ventana_desc = Toplevel(ventana)
        ventana_desc.title("Modificar descripción")
        if ICONO_PATH.exists(): ventana_desc.iconbitmap(ICONO_PATH)

        tk.Label(ventana_desc, text="Nueva descripción en español:").pack(pady=5)
        text_mod = tk.Text(ventana_desc, height=4, width=50)
        text_mod.insert("1.0", sugerencias[clave][1])
        text_mod.pack(pady=5)

        def guardar_mod():
            nueva_desc = text_mod.get("1.0", tk.END).strip()
            sugerencias[clave][1] = nueva_desc
            sugerencias[clave][2] = traducir_a_ingles(nueva_desc)
            ventana_desc.destroy()
            messagebox.showinfo("Modificado", "Descripción actualizada")

        tk.Button(ventana_desc, text="Guardar cambios", command=guardar_mod).pack(pady=10)
    else:
        messagebox.showerror("Error", "Opción no válida", parent=ventana)

# Imprimir listado
# imprime el listado de las sugerencias o pisa el que ya está creado, incluso debemos crear bbdd a base de pdf para tener un registro
def imprimir_listado():
    doc = Document()
    doc.add_heading("Listado de Sugerencias", 0)
    for clave, (precio, desc_es, desc_en) in sugerencias.items():
        p = doc.add_paragraph(f"{clave}. {desc_es} - {precio}€\n{desc_en}")
        p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    doc.save(LISTADO_FILE)
    messagebox.showinfo("Listado guardado", "Archivo listado.docx guardado correctamente")

# Ventana principal

root = tk.Tk()
root.title("SugerChef - La Chancla")
root.geometry("500x600")
root.configure(bg="#E6F2FA")
if ICONO_PATH.exists():
    root.iconbitmap(ICONO_PATH)

# Logo
if LOGO_PATH.exists():
    from PIL import Image, ImageTk
    logo_img = Image.open(LOGO_PATH)
    logo_img = logo_img.resize((160, 100))
    logo_tk = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(root, image=logo_tk, bg="#E6F2FA")
    logo_label.pack(pady=10)

# Título
tk.Label(root, text="Sistema de Sugerencias del Chef", font=("Georgia", 16, "bold"), bg="#E6F2FA", fg="#005B96").pack(pady=5)

# Botones
boton_frame = tk.Frame(root, bg="#E6F2FA")
boton_frame.pack(pady=20)

estilo_boton = {"font": ("Georgia", 12), "bg": "#B3DAF1", "fg": "#003E6B", "width": 30, "relief": "raised"}


def abrir_video():
    webbrowser.open("https://www.youtube.com/watch?v=E2mLzJxLz8s")

def mostrar_info():
    respuesta = messagebox.askyesno(
        "Información",
        "Esta aplicación está diseñada para gestionar de forma profesional las sugerencias gastronómicas del restaurante.\n\n"
        "• Puedes crear nuevas sugerencias introduciendo el precio y la descripción en español, que se traduce automáticamente al inglés.\n"
        "• Puedes generar menús profesionales en formato Word (ESP/ENG) a partir de sugerencias seleccionadas.\n"
        "• También puedes modificar cualquier sugerencia existente o imprimir un listado completo actualizado.\n\n"
        "¿Deseas ver el video explicativo?"
    )
    if respuesta:
        abrir_video()



botones = [
    ("Crear sugerencia nueva", crear_sugerencia),
    ("Crear menú en Word", crear_menu),
    ("Modificar sugerencia", modificar_sugerencia),
    ("Imprimir listado completo", imprimir_listado),
    ("Información / Incidencias", mostrar_info)
]
for texto, comando in botones:
    tk.Button(boton_frame, text=texto, command=comando, **estilo_boton).pack(pady=6)

root.mainloop()
