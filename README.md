# pgd-analisis-evidencias
App en flask para analisis de evidencias de FURAG con Gemini

Ejemplo de request:
POST https://pgd-analisis-evidencias.onrender.com/analitica/evidencias:
```
{
    "pregunta_ge":"Los proyectos de transformación digital aprobados en el comité de gestión y desempeño institucional están sustentados en los resultados de la arquitectura?",
    "evidencia": "https://www.contraloriabga.gov.co/index.php?option=com_phocadownload&view=category&id=110&Itemid=551",
    "entidad": "Contraloria municipal de Bucaramanga"
}
```

Ejemplo de response:
```
[
    "LINK_NO_RELACION_ENTIDAD",
    "LINK_NO_RELACION_FURAG"
]
```

Posibles alertas:

- NO_ALERTAS: No se detectó ninguna señal de alerta en la evidencia analizada
- NO_LINK: La evidencia analizada no constituye un link o URL para acceder un repositorio o sitio web con evidencias o documentos.
- TEXTO_GENERICO: La evidencias analizada, ademas de ser texto plano, no guarda ninguna relacion con la pregunta de gestion extendida para la cual debe dar soportes
- LINK_MALO: La evidencia analizada constituye un link, pero el mismo no responde con estado 200 OK por estar mal formado, apuntar a una red local, necesitar autenticacion, etc.
- LINK_NO_RELACION_ENTIDAD:  El link analizado direcciona a una pagina web que posiblemente no guarda ninguna relacion con la entidad para la cual se esta haciendo el analisis de evidencias
- LINK_NO_RELACION_FURAG: El link analizado direcciona a una pagina web que posiblemente no contiene la palabra "FURAG"
- LINK_NO_ARCHIVOS: El link analizado direcciona a una pagina web que posiblemente no contiene ninguna lista de archivos, links, u otros elementos que puedan servir como evidencias para la pregunta de gestion extendida referenciada
