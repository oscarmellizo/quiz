import tkinter as tk
from tkinter import messagebox
import random
from notion_client import Client

# Conecta con la API de Notion
notion = Client(auth="secret_aAgPKQ7tbH0fga5g0vdetysFNidsjtiA6exKR2Mhk6v")  # Reemplaza con tu token

# ID de la base de datos de Notion donde están las preguntas
database_id = '1110878281c680dbaaeadffafd0215eb'

def obtener_preguntas_desde_notion():
    preguntas = []
    results = notion.databases.query(database_id=database_id).get('results', [])
    
    for result in results:
        # Obtener el texto completo de la pregunta
        titulo_pregunta = result['properties']['Pregunta']['title']
        if titulo_pregunta:
            pregunta = ''.join([t['text']['content'] for t in titulo_pregunta])
        else:
            pregunta = "Sin pregunta"
        
        # Obtener el texto completo de la respuesta correcta
        rich_text_correcta = result['properties']['Correcta']['rich_text']
        if rich_text_correcta:
            respuesta_correcta = ''.join([t['text']['content'] for t in rich_text_correcta])
        else:
            respuesta_correcta = "Sin respuesta correcta"
        
        # Obtener el texto completo de las respuestas incorrectas
        rich_text_incorrecta1 = result['properties']['Incorrecta 1']['rich_text']
        if rich_text_incorrecta1:
            respuesta_incorrecta1 = ''.join([t['text']['content'] for t in rich_text_incorrecta1])
        else:
            respuesta_incorrecta1 = "Sin respuesta incorrecta 1"
        
        rich_text_incorrecta2 = result['properties']['Incorrecta 2']['rich_text']
        if rich_text_incorrecta2:
            respuesta_incorrecta2 = ''.join([t['text']['content'] for t in rich_text_incorrecta2])
        else:
            respuesta_incorrecta2 = "Sin respuesta incorrecta 2"
        
        rich_text_incorrecta3 = result['properties']['Incorrecta 3']['rich_text']
        if rich_text_incorrecta3:
            respuesta_incorrecta3 = ''.join([t['text']['content'] for t in rich_text_incorrecta3])
        else:
            respuesta_incorrecta3 = "Sin respuesta incorrecta 3"
        
        # Agregar la pregunta y las respuestas a la lista
        preguntas.append((pregunta, respuesta_correcta, respuesta_incorrecta1, respuesta_incorrecta2, respuesta_incorrecta3))
    
    return preguntas


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación de Quiz")
        
        # Hacer que la ventana sea redimensionable
        self.root.geometry("800x400")
        self.root.minsize(600, 400)
        self.root.config(bg="#f0f4f8")

        # Configurar el grid para que los widgets se expandan
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Variables del quiz
        self.preguntas = self.obtener_preguntas()
        self.pregunta_actual = 0
        self.correctas = 0
        self.total_preguntas = len(self.preguntas)
        
        # Estilos de fuente
        self.fuente_pregunta = ("Helvetica", 14, "bold")
        self.fuente_respuesta = ("Helvetica", 12)
        self.fuente_estado = ("Helvetica", 10, "italic")

        # Etiqueta de progreso
        self.lbl_progreso = tk.Label(self.root, text="", font=self.fuente_estado, bg="#f0f4f8")
        self.lbl_progreso.grid(row=0, column=0, pady=10, sticky="ew")

        # Widget Message para la pregunta
        self.lbl_pregunta = tk.Message(self.root, text="", font=self.fuente_pregunta, bg="#f0f4f8", anchor="nw", justify="left", width=700)
        self.lbl_pregunta.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")
        self.root.grid_rowconfigure(1, weight=1)

        # Frame para las opciones
        self.frame_opciones = tk.Frame(self.root, bg="#f0f4f8")
        self.frame_opciones.grid(row=2, column=0, padx=20, sticky="nsew")
        self.root.grid_rowconfigure(2, weight=1)

        # Configurar expansión del frame de opciones
        for i in range(4):
            self.frame_opciones.grid_rowconfigure(i, weight=1)
        self.frame_opciones.grid_columnconfigure(0, weight=1)

        self.opciones = []
        self.respuesta = tk.StringVar()

        # Crear botones de opciones
        for i in range(4):
            r = tk.Radiobutton(self.frame_opciones, text="", variable=self.respuesta, value="", font=self.fuente_respuesta, bg="#e9eff4", 
                               activebackground="#cde4f7", anchor="w", relief="ridge", padx=10, pady=5, justify="left")
            r.grid(row=i, column=0, padx=5, pady=5, sticky="nsew")
            self.opciones.append(r)

        # Botón Siguiente
        self.btn_siguiente = tk.Button(self.root, text="Siguiente", command=self.verificar_respuesta, font=("Helvetica", 12, "bold"), 
                                       bg="#4CAF50", fg="white", relief="raised", padx=20, pady=5)
        self.btn_siguiente.grid(row=3, column=0, pady=20, sticky="ew")

        # Ajustar el ancho del widget Message al redimensionar la ventana
        self.root.bind("<Configure>", self.adjust_width)

        self.mostrar_pregunta()

    def obtener_preguntas(self):
        return obtener_preguntas_desde_notion()
    
    def actualizar_progreso(self):
        # Actualiza el texto del progreso
        self.lbl_progreso.config(
            text=f"Pregunta {self.pregunta_actual + 1} de {self.total_preguntas}. Faltan {self.total_preguntas - self.pregunta_actual - 1} preguntas."
        )
    
    def mostrar_pregunta(self):
        if self.pregunta_actual < len(self.preguntas):
            self.actualizar_progreso()
            
            pregunta = self.preguntas[self.pregunta_actual]
            self.lbl_pregunta.config(text=pregunta[0])
            
            opciones = [pregunta[1], pregunta[2], pregunta[3], pregunta[4]]
            random.shuffle(opciones)
            
            for i, r in enumerate(self.opciones):
                r.config(text=opciones[i], value=opciones[i])
                self.respuesta.set(None)  # Desmarcar respuesta
        else:
            messagebox.showinfo("Resultado", f"Quiz terminado.\nRespuestas correctas: {self.correctas}/{len(self.preguntas)}")
            self.root.quit()
    
    def adjust_width(self, event=None):
        # Ajustar el ancho del widget Message según el ancho de la ventana
        new_width = self.root.winfo_width() - 60  # 60 píxeles de margen total
        self.lbl_pregunta.config(width=new_width)
        # Ajustar el wraplength de las opciones también
        for r in self.opciones:
            r.config(wraplength=new_width - 40)  # Ajustar el wraplength de las opciones

    def verificar_respuesta(self):
        respuesta_seleccionada = self.respuesta.get()
        pregunta = self.preguntas[self.pregunta_actual]
        
        if respuesta_seleccionada == pregunta[1]:
            self.correctas += 1
            messagebox.showinfo("Correcto", "¡Respuesta correcta!")
        else:
            messagebox.showinfo("Incorrecto", f"Respuesta incorrecta. La respuesta correcta era: {pregunta[1]}")
        
        self.pregunta_actual += 1
        self.mostrar_pregunta()

# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
