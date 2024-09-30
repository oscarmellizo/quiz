from notion_client import Client

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

# Ejemplo de uso
preguntas = obtener_preguntas_desde_notion()
print(preguntas)
