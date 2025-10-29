import jwt


#La key se define en una variable de entorno, nunca se debe de pasar como parametro porque es una vulnerabilidad, por lo que causa conflictos, ya cuando se hace el despliegue se crea una nueva variable de entorno dentro de la raíz del proyecto
"""
El Json web token (JWT) esta estructurado en 3 partes:
HEADER: Que contiene el algoritmo HS246 y el tipo de token
PAYLOAD: Contiene la información del token, usuario, contraseña, tipo de usuario, etc
SIGNATURE esta se crea a partir del HEADER y el PAYLOAD, que es básicamente un llave privada para poder decodificar el PAYLOAD y poder leer la información, por obvias razones no se envía a producción porque puede causar vulnerabilidades
"""
def createToken(data: dict):
  token: str = jwt.encode(payload=data, key = 'misecret', algorithm='HS256')
  return token

def validateToken(token: str) -> dict:
  data: dict = jwt.decode(token, key='misecret', algorithms=['HS256'])
  return data