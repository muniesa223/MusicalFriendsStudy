'''
Created on 17 ene. 2019

@author: Diego
'''
from _overlapped import NULL

import json
import os.path
import csv

path = "results.json"
results = {}

class jaccardSim(object):
    
    def __init__(self, list):
        self.list = list
        self.similarityList=[]
        
    def compare(self,name1,name2):
   
        set1 = set(name1.split(' '))
        set2 = set(name2.split(' '))
        return set1 == set2
                            
    def doUnionList(self,list1,list2):
        unionList=[]
        
        for fill in list1:
            unionList.append(fill)
            
        for name in list2:
            founded=False
            for name2 in list1:
               
                if(self.compare(name,name2)==True):
                    founded=True
                    break
            if(founded==False):
                unionList.append(name)
                
        return unionList
    
    def doIntersectionList(self,list1,list2):
        intersecList=[]
      
        for name in list2:
            for name2 in list1:
                if(self.compare(name,name2)==True):
                    intersecList.append(name2)
                    break
        return intersecList
                
            
    def main(self):
        user=NULL
        count=0
        graphUser=[]
    
        
        
        for friend in self.list:
            if(count==0):
                user=friend
                count=count+1
            else:
                unionList=self.doUnionList(user.artists,friend.artists)
                intersectionList=self.doIntersectionList(user.artists,friend.artists)
                countUnion=len(unionList)
                countIntersec=len(intersectionList)
                res=float(countIntersec / countUnion)
                if(res>float(0)):
                    print("SIMILARITY WITH: ")
                    print(friend.name)
                    self.similarityList.append(res)
                    graphUser.append(friend.name)
                
        print(len(self.similarityList))
        print(len(graphUser))
                
        results = dict(zip(graphUser, self.similarityList))
        csv_columns = ['name', 'simmilarity']


        
        csv = open('similarUsers.csv', "w") 
          
        columnTitleRow = "name, simmilarity\n"
        csv.write(columnTitleRow)

        for key in results.keys():
            name = key
            number = results[key]
            row = name + "," + str(number) + "\n"
            csv.write(row)