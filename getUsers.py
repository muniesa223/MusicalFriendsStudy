'''
Created on 25 ene. 2019

@author: Diego
'''

import json
import requests
import os.path


# número de usuarios requeridos
required = 100
# constante con número mínimo de amigos
minFriends = 30
# constante con número mínimo de scrobblings
minScrobling = 300
# contador de usuarios añadidos
count = 0
# ruta destino donde se alojarán los nombre de los usuarios
path = "10000usuarios.json"
# constante para añadir al archivo destino anterior pasada esas iteraciones
writeLimit = 300
# API key necesario para realizar la consulta
apiKey = "57f51a2a7d19b952917a19f9ee970938"
# url para obtener los amigos del usuario
urlgetFriendList = "http://ws.audioscrobbler.com/2.0/?method=user.getfriends&user={}&api_key={}&format=json"
# url para obtener la información del usuario
urlgetInfoUser = "http://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={}&api_key={}&format=json"

usuarios = []
usados = []



def InsertToFile():
    with open(path,"w",encoding="utf8", errors='ignore') as jsonFile:
        json.dump(usuarios,jsonFile,ensure_ascii=False)
    print("añadidos ",writeLimit," usuarios al fichero")


def ReadJsonFile(count):
    if(os.path.isfile(path)):
        with open(path,encoding="utf8", errors='ignore') as json_data:
            data = json.load(json_data)
            count += len(data)
    else:
        data = None
    return data


# inicializa el usuario dependiendo si ya existe 10000usuarios.json
# si no existe coge LAST.HQ, sino el ultimo usuario añadido
def Inicialize(count):
    data = ReadJsonFile(count)
    listName = []
    if (data == None):
        listName.append("LAST.HQ")
        count += 1
    else:
        listName = data
    return listName


# forma el string con la url para coger los amigos del usuario
def GetUrlUserFriends(name,limit=0,page=0):
    if (limit > 0):
        val = str(limit)
        limit = "&limit=" + val
    else:
        limit = ""
    if (page > 1):
        val = str(page)
        page = "&page=" + val
    else:
        page = ""
    url = urlgetFriendList.format(name,apiKey) + limit + page
    return url

# chequea si este usuario tiene más de 50 amigos
def Has50Friends(url):
    response = requests.get(url).text
    data = json.loads(response)
    if ("friends" not in data):
        print("no tiene amigos")
        return False
    friends = data["friends"]["@attr"]["total"]
    if (int(friends) < minFriends):
        print("tiene menos de 50 amigos")
        return False
    print("tiene 50 o más amigos")
    return True

# chequea si el usuario tiene amigos
def HasFriends(url):
    response = requests.get(url).text
    data = json.loads(response)
    if ("friends" not in data):
        print("no tiene amigos")
        return False
    return True

# cheque el usuario tiene un mínimo de scrobblings
def HasScrobblings(name):
    url = urlgetInfoUser.format(name,apiKey)
    response = requests.get(url).text
    data = json.loads(response)
    if ("user" not in data):
        print("información válida")
        return False
    playCount = int(data["user"]["playcount"])
    if (playCount < minScrobling):
        print("tiene menos de ",minScrobling," scrobling")
        return False
    print("tiene más de ",minScrobling," scrobling")
    return True

# obtiene los amigos del usuario y los añade a la lista
# cumpliendo siempre los valores antes descritos
def GetFriends(url, name, count):
    response = requests.get(url).text
    data = json.loads(response)
    totalPages = int(data["friends"]["@attr"]["totalPages"])
    for pag in range(1,totalPages+1):
        if (pag > 1):
            urlPage = GetUrlUserFriends(name,500,pag)
            response = requests.get(urlPage).text
            data = json.loads(response)
        amigos = data["friends"]["user"]
        #recorre lista de amigos de la pagina actual
        for i, amigo in enumerate(amigos):
            nameF = amigo["name"]
            print(i, nameF)
            if (HasScrobblings(nameF) and nameF not in usuarios):
                print("añadido")
                usuarios.append(nameF)
                count += 1
                print("total:",count)
                if (count % writeLimit == 0):
                    InsertToFile()
            if (count == required):
                break
        if (count == required):
            break
    usados.append(name)



# PROGRAMA PRINCIPAL
usuarios = Inicialize(count)   #Crea el fichero si aun no existe delvuelve la lista con elusuario HQ

url = GetUrlUserFriends(usuarios[0],500)
GetFriends(url,usuarios[0],count)
print("tamaño de usados:",len(usados))
if (len(usuarios) < required):
    for i,name in enumerate(usuarios):
        print("ultimo bucle",i,name)
        url = GetUrlUserFriends(name,500)
        if (name not in usados and HasFriends(url)):
            GetFriends(url,name,count)
            usados.append(name)
InsertToFile()
