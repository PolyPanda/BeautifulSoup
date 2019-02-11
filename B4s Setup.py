# lab8 
# Yuxi Yu & Hua Xia
import urllib.request as ur
import requests
from bs4 import BeautifulSoup 
import re
import time
from bs4.diagnose import diagnose
import json
import sqlite3

class SetUp():
    '''read data from website, and save it into 4 data list'''
    def __init__(self):
        try:
            olympicData = {}
            self.countrySportDict = {}
            keys = []
            self.totalPerson = []
            self.countryWithSports = []      
            
            page = requests.get('https://www.olympic.org/pyeongchang-2018/results/en/general/nocs-list.htm')
            soup = BeautifulSoup(page.content, 'lxml')
            country = soup.find('div', class_='CountriesList')
            self.countryNames = [text.get_text() for text in soup.select("div.CountriesListItem a.center-block strong")] #get all the country name  
            g_data = soup.find_all("a", {"class": "center-block"})
            for link in g_data:
                keys.append(link.text)
            keys = map(lambda s: s.strip(), keys)
            links= ["https://www.olympic.org/pyeongchang-2018/results"+ str(link.get('href'))[5:] 
                       for link in soup.select("div.CountriesListItem a.center-block")]
            olympicData = list(zip(keys, links))      #get country match with their links

            
            for i in olympicData:
                page = requests.get(i[1])
                soup = BeautifulSoup(page.content, "lxml")
                for data in soup.select('tr.MedalStd1 td'): 
                    total = data.get_text().strip() 
                self.totalPerson.append(total)  #get total list 
                
                tableTag = soup.find("table", class_="ResTableFull")
                aTag = tableTag.find_all('a')
                self.sportsList = []
                for j in aTag:
                    x = j.get_text()
                    if not x.startswith('\n'):
                        self.sportsList.append(x)            

                self.countrySportDict[i[0]] = self.sportsList
            
        except requests.exceptions.HTTPError as error:
            print (error)
            sys.exit()
        except requests.exceptions.RequestException as e:
            print (e)
            sys.exit("Unable to access requested URL")
        except requests.exceptions.Timeout:
            sys.exit("Unable to access requested URL")
        except requests.exceptions.TooManyRedirects:
            sys.exit("Unable to access requested URL")           
        
        
    def createJSONFile(self):
        '''save the country's first letter match with the list and write as json file'''
        countryList = self.countryNames
        countryList = "','".join(map(str,countryList))
        myDic={}
        for letter in countryList.split("','"):
            if(letter[0] not in myDic.keys()):
                myDic[letter[0]]=[]
                myDic[letter[0]].append(letter)
            else:
                if(letter not in myDic[letter[0]]):
                    myDic[letter[0]].append(letter)
                    
        with open('lab8json.json', 'w') as fh:
            json.dump(myDic, fh, indent=3)

    def creatDataBase(self, conn, cur):
        '''create database and two tables, store data into database'''
        cur.execute("DROP TABLE IF EXISTS countryDB")
        cur.execute('''CREATE TABLE countryDB(
                       sid INTEGER NOT NULL PRIMARY KEY,
                       country TEXT,
                       total INTEGER,
                       sport1 INTEGER,
                       sport2 INTEGER,
                       sport3 INTEGER,
                       sport4 INTEGER,
                       sport5 INTEGER,
                       sport6 INTEGER,
                       sport7 INTEGER,
                       sport8 INTEGER,
                       sport9 INTEGER,
                       sport10 INTEGER,
                       sport11 INTEGER,
                       sport12 INTEGER,
                       sport13 INTEGER,
                       sport14 INTEGER,
                       sport15 INTEGER)''')
        
        for x in self.countryNames:
            cur.execute("INSERT INTO countryDB (country) VALUES (?)", (x,))   
            
        i = 1
        for y in self.totalPerson:
            cur.execute("UPDATE countryDB SET total = ? WHERE sid = ?", (y,i)) 
            i += 1
                    
        
        cur.execute("DROP TABLE IF EXISTS SportsDB")
        cur.execute('''CREATE TABLE SportsDB(
                                   sid INTEGER NOT NULL PRIMARY KEY,
                                   sports TEXT)''')
        
        fullsportslist = self.countrySportDict["United States of America"]

        for y in fullsportslist:
            cur.execute("INSERT INTO SportsDB (sports) VALUES (?)", (y,))
    
        for x in self.countryNames: 
            self.sportsList = self.countrySportDict[x]
            for y in self.sportsList:
                cur.execute('''SELECT sid FROM SportsDB WHERE sports = ?''', (y,))
                sportsID = cur.fetchone()[0]
                cur.execute('''UPDATE countryDB SET sport{} = 1 WHERE country = ?'''.format(sportsID),(x,))
        conn.commit()
        conn.close()        
        


def main():
    setupObj = SetUp()
    conn = sqlite3.connect('lab8.db')
    cur = conn.cursor()
    setupObj.creatDataBase(conn, cur)
    setupObj.createJSONFile()

    
main()
