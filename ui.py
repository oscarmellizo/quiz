import tkinter as tk
from tkinter import messagebox
import random
from notion_client import Client
import database

# Conecta con la API de Notion
notion = Client(auth="secret_aAgPKQ7tbH0fga5g0vdetysFNidsjtiA6exKR2Mhk6v")  # Reemplaza con tu token

# ID de la base de datos de Notion donde están las preguntas
database_id = '1110878281c680dbaaeadffafd0215eb'

def obtener_preguntas_desde_notion():
    """
    Consulta la base de datos de Notion y obtiene las preguntas y respuestas.
    
    Returns:
        list: Lista de preguntas, cada una con la estructura (pregunta, correcta, incorrecta1, incorrecta2, incorrecta3).
    """
    preguntas = []
    
    # Obtener todos los elementos de la base de datos
    results = notion.databases.query(database_id=database_id).get('results', [])
    
    # Procesar los resultados
    for result in results:
        # Verificar si el campo "Pregunta" tiene un título no vacío
        if result['properties']['Pregunta']['title']:
            pregunta = result['properties']['Pregunta']['title'][0]['text']['content']
        else:
            pregunta = "Sin pregunta"  # Puedes ajustar este valor según sea necesario

        # Verificar si las respuestas están disponibles y asignar valores por defecto si están vacías
        respuesta_correcta = (
            result['properties']['Correcta']['rich_text'][0]['text']['content']
            if result['properties']['Correcta']['rich_text']
            else "Sin respuesta correcta"
        )
        
        respuesta_incorrecta1 = (
            result['properties']['Incorrecta 1']['rich_text'][0]['text']['content']
            if result['properties']['Incorrecta 1']['rich_text']
            else "Sin respuesta incorrecta 1"
        )
        
        respuesta_incorrecta2 = (
            result['properties']['Incorrecta 2']['rich_text'][0]['text']['content']
            if result['properties']['Incorrecta 2']['rich_text']
            else "Sin respuesta incorrecta 2"
        )
        
        respuesta_incorrecta3 = (
            result['properties']['Incorrecta 3']['rich_text'][0]['text']['content']
            if result['properties']['Incorrecta 3']['rich_text']
            else "Sin respuesta incorrecta 3"
        )
        
        # Agregar la pregunta y las respuestas a la lista de preguntas
        preguntas.append((pregunta, respuesta_correcta, respuesta_incorrecta1, respuesta_incorrecta2, respuesta_incorrecta3))
    
    return preguntas

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación de Quiz")
        self.root.geometry("500x400")
        self.root.config(bg="#f0f4f8")  # Color de fondo suave
        
        # Variables del quiz
        self.preguntas = self.obtener_preguntas()
        self.pregunta_actual = 0
        self.correctas = 0
        
        # Estilo de la fuente
        self.fuente_pregunta = ("Helvetica", 14, "bold")
        self.fuente_respuesta = ("Helvetica", 12)
        
        # Elementos de la interfaz gráfica
        self.lbl_pregunta = tk.Label(self.root, text="", wraplength=400, font=self.fuente_pregunta, bg="#f0f4f8")
        self.lbl_pregunta.pack(pady=20)
        
        self.opciones = []
        self.respuesta = tk.StringVar()
        
        # Crear botones de opciones con borde y diseño agradable
        for i in range(4):
            r = tk.Radiobutton(self.root, text="", variable=self.respuesta, value="", font=self.fuente_respuesta, bg="#e9eff4", 
                               activebackground="#cde4f7", width=40, anchor="w", relief="ridge", padx=10, pady=5)
            r.pack(anchor=tk.W, pady=5, padx=20)
            self.opciones.append(r)
        
        self.btn_siguiente = tk.Button(self.root, text="Siguiente", command=self.verificar_respuesta, font=("Helvetica", 12, "bold"), 
                                       bg="#4CAF50", fg="white", relief="raised", padx=20, pady=5)
        self.btn_siguiente.pack(pady=20)
        
        self.mostrar_pregunta()
    
    def obtener_preguntas(self):
        return obtener_preguntas_desde_notion()
    
    def mostrar_pregunta(self):
        if self.pregunta_actual < len(self.preguntas):
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
