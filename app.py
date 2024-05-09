from flask import Flask, jsonify, request
import requests
import urlextract as extractor
import google.generativeai as genai
import os

app = Flask(__name__)

# Create a conversation client
genai.configure(api_key=os.environ["GOOGLE_AI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

#Extractor de URLs
urlextractor = extractor.URLExtract()

#Alertas a retornar
alertas = []

# Primero, determinar si la evidencia es un texto plano o un link para saber como evaluarlo
# si es un link, revisar primero que el link retorne 200
#   Luego de comprobar que link retorne 200, evaluar:
#       Pagina web debe estar relacionada con la entidad o con furag
#       Pagina web debe contenter una lista de archivos, links o elementos
# Si es un texto plano, generar alerta de que evidencia es un texto plano
#   Ademas, evaluar que texto tenga que ver con la pregunta
@app.route('/analitica/evidencias', methods=['POST'])
def analisis_evidencia():

    alertas.clear()

    request_data = request.get_json()
    pregunta_ge = request_data['pregunta_ge']
    evidencia = request_data['evidencia']
    entidad = request_data['entidad']

    #Cuando evidencia no contiene links:
    if not urlextractor.find_urls(evidencia):
        analizar_texto_plano(pregunta_ge, evidencia)
        
    #Cuando evidencia contiene links
    else:
        analizar_link(entidad, evidencia)
    
    if len(alertas) == 0:
        alertas.append("NO_ALERTAS")

    return jsonify(alertas), 200

def analizar_texto_plano(pregunta, evidencia):
    print('No se detecto link, analizando texto plano')
    alertas.append("NO_LINK")
    response = model.generate_content(f'Responder en español si la respuesta tiene relacion con la pregunta, usar unicamente el contexto dado por la pregunta y la respuesta, no buscar informacion en la web. responder unicamente \"si\" o \"no\": pregunta: {pregunta} respuesta: {evidencia}')
    if response.text.lower() == 'no':
        alertas.append("TEXTO_GENERICO")

def analizar_link(entidad, evidencia):
    #Revisando que link sea accesible
    print('Link detectado, analizando')
    r = requests.get(urlextractor.find_urls(evidencia)[0])
    if r.status_code != 200:
        alertas.append("LINK_MALO")
    else:
        #Cuando el link es accesible, revissar si el contenido tiene que ver con la entidad
        response = model.generate_content(f'Acceder a la pagina web del siguiente link, y responder si el contenido de la pagina web tiene relacion con {entidad}, solamente responder si o no: link:{evidencia}')
        print(response.text)
        if response.text.lower() == 'no':
                alertas.append("LINK_NO_RELACION_ENTIDAD")
        #Cuando el link es accesible, revissar si el contenido tiene contiene la palabra FURAG
        response = model.generate_content(f'Acceder a la pagina web del siguiente link, y responder si el contenido de la pagina web mostrada incluye la palabra "\"FURAG"\", solamente responder si o no: link:{evidencia}')
        print(response.text)
        if response.text.lower() == 'no':
            alertas.append("LINK_NO_RELACION_FURAG")
        #Cuando el link es accesible, revisar si el contenido lista archivos, links, o elementos
        response = model.generate_content(f'Acceder a la pagina web del siguiente link, y responder si contiene una lista de archivos, links, u otro tipo de elementos, solamente responder si o no: {evidencia}')
        print(response.text)
        if response.text.lower() == 'no':
            alertas.append("LINK_NO_ARCHIVOS")

if __name__ == '__main__':
    app.run(debug=True)