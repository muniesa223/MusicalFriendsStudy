'''
Created on 17 ene. 2019

@author: Diego
'''
class User(object):
    
    def __init__(self, name,artists,position):
        self.name = name
        self.artists = artists
        self.position=position   
        
    def getArtist(self,pos):
        return self.artists[pos]
    
    def searchArtist(self,nameArtist):
        find=False
        for usr in self.artists:
            if(usr==nameArtist):
                find=True
        return find
    
    def getNameUser(self):
        return  self.name
    
    def getPossition(self):
        return  self.possition
  
   
            