# lab8 
# Yuxi Yu & Hua Xia
import urllib.request as ur
import requests
from bs4 import BeautifulSoup 
import re
import sys
import json
import sqlite3



class userInterface():
    
    '''
        Default Constructor
        '''
    def __init__(self):
        self.JSONFileName = "olympics.json"
        with open(self.JSONFileName, 'r') as fh:
            self.firstLetterDict = json.load(fh)
        self.conn = sqlite3.connect('lab8.db')
        self.cur = self.conn.cursor() 
        self.cur.execute('SELECT sports FROM SportsDB ')
        self.sportList = []
        for record in self.cur.fetchall():
            self.sportList.append(record[0])
        while True:
            self.displaylistOfCountry()
            self.displaySportCountry()
            self.displayNumAthletesCountry()
            

    '''
    First Promote the user to display 
    selection of country athletes
    '''              
    def displaylistOfCountry(self):
        Letter = ''
        while Letter == '':
            first_letter = input('First letter of country name: ')
            if first_letter == "0":
                sys.exit()
            if(first_letter.isalpha()):
                first_letter = first_letter.upper()
                if (len(first_letter)!=1 or (first_letter in 'ZXYWVQ') ):
                    print("No country name matching the letter")
                else:
                    Letter = first_letter
            else:
                print("Invalid entry. Re-enter the first letter of country name:")      
        print("Countries: ") 
        self.countryListResults = self.firstLetterDict[first_letter]
        counter = 0
        for country in self.countryListResults:
            if country[0] == first_letter:
                print(str(counter+1)+": "+country)
                counter+=1            
        countryString = ''
        while countryString == '':
            try:
                choice = int(input("Enter a number: "))
                if(choice < 1 or choice > len(self.countryListResults) ):
                    print("Invalid number input")
                else:
                    countryString = self.countryListResults[choice-1]
                    print(countryString)
                    self.cur.execute('SELECT total FROM countryDB WHERE country = ?', (countryString,))
                    self.total = self.cur.fetchone()[0]
                    print(self.total, "athletes for", countryString)
            except ValueError:
                print("Please enter an integer")   

    '''
    Display contries with sport catagloy
    Also select the data from database 
    '''      
    def displaySportCountry(self):
        print("Sports: ")
        sportsName = ", ".join(self.sportList)
        print(sportsName)
        sport = ''
        while sport == '':
            sportInput = input("Enter sport name: ")
            sportInput = sportInput.title()
            if sportInput not in self.sportList:
                print("Sport entered is invalid!")
            else:
                sport = sportInput
        self.cur.execute('SELECT sid FROM SportsDB WHERE sports = ?', (sport,))
        self.sportNum = self.cur.fetchone()[0]
        #self.getCountryBySport()
        self.countryBySport = []
        sql = "SELECT country FROM countryDB WHERE {} = 1".format("sport"+str(self.sportNum))
        self.cur.execute(sql)
        for record in self.cur.fetchall():
            self.countryBySport.append(record[0])         
        self.countryBySport = []
        sql = "SELECT country FROM countryDB WHERE {} = 1".format("sport"+str(self.sportNum))
        self.cur.execute(sql)
        for record in self.cur.fetchall():
            self.countryBySport.append(record[0])        
        print("Countries participating in", sport)
        for elem in self.countryBySport:
            print(elem)
    '''
    Display the max and min in the data row
    '''
    def displayNumAthletesCountry(self):
        min = -1
        max = -1
        while min < 0 or max < 0:
            try:
                userValues = input("Enter min, max number of athletes: ")
                values = userValues.split(',')
                min = int(values[0])
                max = int(values[1])
                if(min < 0 or min > max):
                    print("Invalid min and max")
            except ValueError:
                print("Please enter an integer")   
            except Exception as e:
                print(str(e))
        # get the record of the min and max
        self.countryWithNumAthletes = []
        self.cur.execute('SELECT country FROM countryDB WHERE total BETWEEN ? and ?', (min, max,)) 
        for record in self.cur.fetchall():
            self.countryWithNumAthletes.append(record[0])
        # print the end 
        print("Countries with", min, "to", max, "athletes")
        for elem in self.countryWithNumAthletes:
            print(elem)
            
        
def main():
    userInterface()
                     
main()
