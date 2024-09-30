from notion_client import Client

# Conecta con la API de Notion
notion = Client(auth="secret_aAgPKQ7tbH0fga5g0vdetysFNidsjtiA6exKR2Mhk6v")  # Reemplaza con tu token

# ID de la base de datos de Notion donde están las preguntas
database_id = '1110878281c680dbaaeadffafd0215eb'

# Consultar la base de datos
response = notion.databases.query(database_id=database_id)

# Mostrar resultados
for result in response['results']:
    print(result)
