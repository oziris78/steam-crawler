
################## IMPORTS ##################

from bs4 import BeautifulSoup
import requests, webbrowser, time, tkinter, os, sys
from tkinter import ttk


################## VARIABLES ##################


allLinks = []
linksToOpen = []
browserType = ""
browserDir = ""
waitingTime = 1.25


isFreeExecuted = False
isDiscountedExecuted = False

isFreeOpened = False
isDiscountedOpened = False

urlForFree = 'https://store.steampowered.com/search/?sort_by=Price_ASC&supportedlang=english&category1=998&os=win&specials=1'
    


################## CLASSES ##################

class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title('Steam Crawler Plus Plus - SCPP v0.2')
        self.geometry('370x150')
        checkBtn = ttk.Button(self, text='CHECK DISCOUNT', command = self.searchGamesWithDiscount)
        checkBtn.pack(expand=True)
        checkFreeBtn = ttk.Button(self, text='CHECK FREE GAMES', command = self.searchFreeGames)
        checkFreeBtn.pack(expand=True)
        
    def tryToTerminate(self):
        if (isFreeOpened and isFreeExecuted and not isDiscountedExecuted) or (isDiscountedOpened and isDiscountedExecuted and not isFreeExecuted) or (isFreeOpened and isFreeExecuted and isDiscountedOpened and isDiscountedExecuted):
            print('test')
            self.destroy()
            sys.exit(0)

    def searchFreeGames(self):
        global isFreeExecuted
        getConfigs()
        btn = ttk.Button(self,text='Open Free Games If They Exist', command = self.openFree)
        btn.pack(expand=True)
        isFreeExecuted = True
        
    def openFree(self):
        global isFreeOpened
        setupBrowser()
        openIfTheresAnyFreeGame()
        isFreeOpened = True
        self.tryToTerminate()
            
    def searchGamesWithDiscount(self):
        global isDiscountedExecuted
        getAllLinks()
        getConfigs()
        getGamesOnSale()
        btn = ttk.Button(self,text='Open Games With Discount If They Exists', command = self.btnClick)
        btn.pack(expand=True)
        isDiscountedExecuted = True

    def btnClick(self):
        global isDiscountedOpened
        setupBrowser()
        openLinks()
        isDiscountedOpened = True
        self.tryToTerminate()
      
      
      
################## FUNCTIONS ##################


            
        
def getAllLinks():
    with open(os.getcwd() + '/res/steamLinks.txt', 'a+') as myFile:
        myFile.seek(0)
        global allLinks
        allLinks = myFile.read().split('\n')
        while allLinks.count('') != 0:  allLinks.remove('')
        while allLinks.count(' ') != 0: allLinks.remove(' ')      

def getConfigs():
    with open(os.getcwd() + '/res/config.txt', 'a+') as myFile:
        myFile.seek(0)
        tempList = myFile.read().split('\n')
        global browserType, browserDir, waitingTime
        browserType = str(tempList[0])
        browserDir = str(tempList[1])
        waitingTime = float(tempList[2])
    
def getGamesOnSale():
    global linksToOpen
    for i in range(0, len(allLinks)):
        soup = BeautifulSoup(requests.get(str(allLinks[i])).text, features="html.parser")
        salePercentage = soup.find_all("div", {"class": "discount_pct"})
        if len(salePercentage) > 0:
            onSalePrice = soup.find_all("div", {"class": "discount_final_price"})
            onSalePrice = onSalePrice[0]
            onSalePrice = str(onSalePrice)
            onSalePrice = onSalePrice[34:-6]
            salePercentage = salePercentage[0]
            salePercentage = str(salePercentage)
            salePercentage = salePercentage[26:30]
            linksToOpen.append(allLinks[i])


def setupBrowser():
    webbrowser.register(str(browserType), None, webbrowser.BackgroundBrowser(str(browserDir)))
    
    
def openLinks():
    if len(linksToOpen) != 0:
        for i in linksToOpen:
            webbrowser.get(browserType).open(i)
            time.sleep(waitingTime)
    else:
        sys.exit(0)
        
        
def openIfTheresAnyFreeGame():
    soupForFree = BeautifulSoup( requests.get(urlForFree).text, 'html.parser')
    spans = [str(a.select('div.search_discount span')) for a in soupForFree.select('div#search_resultsRows a')]
    for span in spans:
        if span.find('100%') != -1:
            webbrowser.get(browserType).open(urlForFree)
            break
        
        
################## MAIN ##################
        
if __name__ == '__main__':
    app = App()
    app.mainloop()

