

# my imports
import telekpyhub
from my_enums import WindowType, HandlingResult

# imports
import PySimpleGUI as sg
import copy
import json
import time
import sys
import requests
import webbrowser
from bs4 import BeautifulSoup

# import os with custom path

import os
os.chdir(telekpyhub.EXECUTABLE_PATH)

# import os
# os.chdir(os.path.dirname(__file__))  # make sure that os.getcwd() shows this file's folder
# from pathlib import Path
# os.chdir(str(Path(os.getcwd()).parents[0])) # go back once into the project's main folder


##################  VARIABLES  ##################


sg.theme("DarkAmber")
layout = [
    [sg.VPush()],
    [
		sg.Text('CHECK DISCOUNT', font="Calibri 18", key='-EXECUTE-DISCOUNT-', enable_events=True)
    ],
    [
		sg.Text('CHECK FREE GAMES', font="Calibri 18", key='-EXECUTE-FREE-', enable_events=True)
    ],
    [
		sg.Text('GO BACK', font="Calibri 18", key='-BACK-', enable_events=True)
    ],
    [sg.VPush()]
]


all_links = []
links_to_open = []
browser_type = ""
browser_dir = ""
waiting_time = float()

is_free_executed = False
is_discount_executed = False

is_free_opened = False
is_discount_opened = False

url_for_free = 'https://store.steampowered.com/search/?sort_by=Price_ASC&supportedlang=english&category1=998&os=win&specials=1'



##################  INIT AND CONFIG FUNCTIONS  ##################


# reads steam_links.txt file into the variables
def get_all_links():
    with open(os.getcwd() + '/res/scpp_links.json', 'r') as myFile:
        _json = json.load(myFile)
        global all_links
        all_links = _json["all_links"]



# reads config.txt file into the variables
def get_configs():
    with open(os.getcwd() + '/res/scpp_config.json', 'r') as myFile:
        _json = json.load(myFile)
        global browser_type, browser_dir, waiting_time
        browser_type = str(_json["browser_type"])
        browser_dir = str(_json["browser_dir"])
        waiting_time = float(_json["waiting_time"])




def setup_browser():
    webbrowser.register(browser_type, None, webbrowser.BackgroundBrowser(browser_dir))



##################  WEB SCRAPING FUNCTIONS  ##################


def get_games_on_sale():
    global links_to_open
    for i in range(0, len(all_links)):
        soup = BeautifulSoup(requests.get(str(all_links[i])).text, features="html.parser")
        salePercentage = soup.find_all("div", {"class": "discount_pct"})
        if len(salePercentage) > 0:
            onSalePrice = soup.find_all("div", {"class": "discount_final_price"})
            onSalePrice = onSalePrice[0]
            onSalePrice = str(onSalePrice)
            onSalePrice = onSalePrice[34:-6]
            salePercentage = salePercentage[0]
            salePercentage = str(salePercentage)
            salePercentage = salePercentage[26:30]
            links_to_open.append(all_links[i])



def open_links():
    if len(links_to_open) != 0:
        for i in links_to_open:
            webbrowser.get(browser_type).open(i)
            time.sleep(waiting_time)
    else:
        sys.exit(0)
        
        

def open_if_theres_any_free_game():
    soupForFree = BeautifulSoup( requests.get(url_for_free).text, 'html.parser')
    spans = [str(a.select('div.search_discount span')) for a in soupForFree.select('div#search_resultsRows a')]
    for span in spans:
        if span.find('100%') != -1:
            webbrowser.get(browser_type).open(url_for_free)
            break



##################  BUTTON HANDLERS  ##################



def handle_execute_free():
    global is_free_executed
    is_free_executed = True
    get_configs()
    global layout
    layout[2] = [
        sg.Text("Open Free Games", font="Calibri 16", key='-OPEN-FREE-', enable_events=True, text_color="white")
    ]



def handle_open_free():
    global is_free_opened
    is_free_opened = True
    setup_browser()
    open_if_theres_any_free_game()
    try_to_close_app()
    layout[2] = [
        sg.Text("Open Free Games", font="Calibri 16", key='-OPEN-FREE-', enable_events=True, text_color="red")
    ]



def handle_execute_discount():
    global is_discount_executed
    is_discount_executed = True
    get_all_links()
    get_configs()
    get_games_on_sale()
    global layout
    layout[1] = [
        sg.Text("Open Discounts", font="Calibri 16", key='-OPEN-DISCOUNT-',  enable_events=True, text_color="white")
    ]
    


def handle_open_discount():
    global is_discount_opened
    is_discount_opened = True
    setup_browser()
    open_links()
    try_to_close_app()
    global layout
    layout[1] = [
        sg.Text("Open Discounts", font="Calibri 16", key='-OPEN-DISCOUNT-',  enable_events=True, text_color="red")
    ]
    


##################  GUI CODE  ##################



def handle_events(event, values):
    if event == "-BACK-":
        return HandlingResult.GO_BACK
    
    if event == "-EXECUTE-DISCOUNT-":
        handle_execute_discount()
        return HandlingResult.REFLESH

    if event == "-EXECUTE-FREE-":
        handle_execute_free()
        return HandlingResult.REFLESH
    
    # exec olanlar
    if event == "-OPEN-FREE-" and not is_free_opened:
        handle_open_free()
        return HandlingResult.REFLESH
    
    if event == "-OPEN-DISCOUNT-" and not is_discount_opened:
        handle_open_discount()
        return HandlingResult.REFLESH

    return HandlingResult.STAY



def get_window():
    return sg.Window("Steam Crawler++", copy.deepcopy(layout), element_justification="center", size=(500, 150), metadata=WindowType.SCPP)



def try_to_close_app():
    # b1 = is_free_opened and is_free_executed and not is_discount_executed
    # b2 = is_discount_opened and is_discount_executed and not is_free_executed
    b3 = is_free_opened and is_free_executed and is_discount_opened and is_discount_executed
    # if b1 or b2 or b3:
    if b3:
        sys.exit(0)



##################  MAIN  ##################


if __name__ == '__main__':
    pass

