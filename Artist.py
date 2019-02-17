'''
Created on 17 ene. 2019

@author: Diego
'''
class Artist(object):
    
    def __init__(self, name,possition):
        self.name = name
        self.users = []
        self.possition=possition
        self.count=0
        
    def addUser(self,nameUser):
        self.users.append(nameUser)
        self.count=self.count+1
    def searchUser(self,nameUser):
        find=False
        for usr in self.users:
            if(usr==nameUser):
                find=True
        return find
    def getNameArtist(self):
        return  self.name
    def getPossition(self):
        return  self.possition
    def getNumUsers(self):
        return self.count
   
            