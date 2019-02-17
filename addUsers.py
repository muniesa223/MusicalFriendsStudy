# -*- coding: utf-8 -*-
"""
@descripci�n:
Este script realiza una busqueda por todos los usuarios cogiendo
los 10 artistas m�s escuchados por el usuario y haciendo una paridad
entre esos 10.

@autores: 

Diego Sanchez Muniesa

"""

import json
import requests
import os.path
from pack.Artist import Artist 

# ruta de usuarios que utilizaremos para la b�squeda
pathUsers = "10000usuarios.json"
# ruta destino donde crearemos el csv para 
pathAristas = "aristas.csv"
# API necesaria para realiza las consultas REST
apiKey = "57f51a2a7d19b952917a19f9ee970938"

count  = 0

class addUsers(object):
    
    def __init__(self):
        #ARTISTS LIST
        self.finalData = []
        

# Inicializa el archivo de aristas destino
    def initFile(self,path,typeFile):
        if (typeFile is "aristas"):
            line = "Source,Target\n"
        else:
            line = "Label\n"
        if (os.path.isfile(path)):        
            with open(path,'r+') as file:
                first_line = file.readline()
                if (line not in first_line):
                    file.write(line)
                file.close()
        else:
            with open(path,'w') as file:
                file.write(line)
                file.close()
            

    # devuelve un Json con los usuarios
    def readJsonFile(self,path):
        with open(path,'r') as json_data:
            data = json.load(json_data)
        return data


    # devuelve la url necesaria para hacer la consulta de los 
    def GetUrlTopArtist(self,name,limit=0,page=0):
        wbTopArtist = "http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user={}&api_key={}&format=json"
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
        url = wbTopArtist.format(name,apiKey) + limit + page
        return url


    def GetArtistList(self,data,maxim):
        listArtist = data["topartists"]["artist"]
        returnList = []
        file = open("temp.txt",'w')
        count = maxim
        for art in listArtist:
            if (count > 0):
                try:
                    file.write(art["name"])
                    returnList.append(art["name"])
                    count -= 1
                except:
                    print("fallo al insertar")
            else:
                break
        file.close()
        return returnList
        

    # realiza la paridad de los artistas escogidos
    def GetCombinationByList(self,listArtist):
        combo = []
        total = len(listArtist)
        for it1 in range(0,total):
            for it2 in range(it1,total):
                if(listArtist[it1] not in listArtist[it2]):
                    linea = listArtist[it1] + ',' + listArtist[it2] 
                    combo.append(linea)
        return combo
    

    # obtiene los 10 artistas m�s escuchados por el usuario
    def GetTopArtists(self,name):
    
        fileOut = open(pathAristas,'a')
        url = self.GetUrlTopArtist(name)
        response = requests.get(url).text
        data = json.loads(response)
        listArtis =  self.GetArtistList(data,10)
    
        return listArtis
    
    #MICODIGO
    
    
    
    
    
    ## combinationList = GetCombinationByList(listArtis)
    ## num = 0
    ## while (num < len(combinationList)):
    #    line = combinationList[num] + '\n'
    #     fileOut.write(line)
    #     num += 1
    # fileOut.close()
    #si es un 0 esque no esta y hay que añadir uno nuevo
    def isOnList(self,nameArtist):
    
        aux=0
        for i in self.finalData:
            re=i.name
            if(len(self.finalData)!=0):
                if(self.compare(re,nameArtist)==True):
                    aux = i.getPossition()
                    break
        return aux
        
    def compare(self,name1,name2):
   

        set1 = set(name1.split(' '))
        set2 = set(name2.split(' '))
        return set1 == set2
                            

# PROGRAMA PRINCIPAL
    def main(self):
        self.initFile(pathAristas,"aristas")
        auxCounter=0
        counter=0
        jsonUsers = self.readJsonFile(pathUsers)
        numUsers = len(jsonUsers)
        print(numUsers)
        #print("N�mero de usuarios:",len(jsonUsers))
        #FOR EVERY USER:
        for name in jsonUsers:
            print(name)
            print("-----------------------------")
            #GET THEIR 1O TOP ARTISTS
            list=self.GetTopArtists(name)
            
            #ADD THE USER TO THE ARTISTS LIST
            for  i  in list:
                print(i)
            
                pos=self.isOnList(i) 
                if(pos!=0):
                    self.finalData[pos].addUser(name)
                else:
                    artist=Artist(i,counter)
                    artist.addUser(name)
                    self.finalData.append(artist)
                    counter=counter+1
                    
                auxCounter=auxCounter+1
                
        print("EMPIEZOOOOOOOOOOOOOOOOO")    
        print(len(self.finalData))        
    
        for name2 in self.finalData:
            
            if(name2.count>3):
                print(name2.getNameArtist())
                print(name2.count)
    
        os.remove("temp.txt")  


    