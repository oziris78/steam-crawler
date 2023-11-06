# Copyright 2023 Oğuzhan Topaloğlu 
#  
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
#  
#     http://www.apache.org/licenses/LICENSE-2.0 
#  
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License. 



# my imports
import main_window
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
os.chdir(main_window.EXECUTABLE_PATH)


##################  VARIABLES  ##################


sg.theme("DarkAmber")
layout = [
    [
        sg.VPush()
    ],
    [
		sg.Text('CHECK DISCOUNT', font="Calibri 20", key='-EXECUTE-DISCOUNT-', enable_events=True)
    ],
    [
		sg.Text('CHECK FREE GAMES', font="Calibri 20", key='-EXECUTE-FREE-', enable_events=True)
    ],
    [
		sg.Text('-----------------------------------' * 2, text_color="gray")
    ],
    [
		sg.Text('OPEN ALL LINKS', font="Calibri 15", key='-OPEN-ALL-LINKS-', enable_events=True)
    ],
    [
		sg.Text('OPEN RES FOLDER', font="Calibri 15", key='-OPEN-RES-', enable_events=True)
    ],
    # [
	# 	sg.Text('GO BACK', font="Calibri 15", key='-BACK-', enable_events=True)
    # ],
    [
        sg.VPush()
    ]
]


all_links = []
links_to_open = []
browser_type = ""
browser_dir = ""
waiting_time = -1.0
browser_obj = None

is_free_executed = False
is_discount_executed = False

is_free_opened = False
is_discount_opened = False

url_for_free = 'https://store.steampowered.com/search/?sort_by=Price_ASC&supportedlang=english&category1=998&os=win&specials=1'



##################  INIT AND CONFIG FUNCTIONS  ##################


# reads steam_links.txt file into the variables
def get_all_links():
    global all_links
    if len(all_links) != 0:
        return
    
    with open(os.getcwd() + '/res/scpp_links.json', 'r') as myFile:
        _json = json.load(myFile)
        all_links = _json["all_links"]



# reads config.txt file into the variables
def get_configs():
    global browser_type, browser_dir, waiting_time

    # if all of them are already set then return
    if browser_type != "" and browser_dir != "" and waiting_time != -1.0:
        return
    
    with open(os.getcwd() + '/res/scpp_config.json', 'r') as myFile:
        _json = json.load(myFile)
        browser_type = str(_json["browser_type"])
        browser_dir = str(_json["browser_dir"])
        waiting_time = float(_json["waiting_time"])




def setup_browser():
    global browser_obj
    if browser_obj != None:
        return

    webbrowser.register(browser_type, None, webbrowser.BackgroundBrowser(browser_dir))
    browser_obj = webbrowser.get(browser_type)



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


def open_all_steamdb_links():
    if len(links_to_open) > 0:
        for link in links_to_open:
            # link is something like https://store.steampowered.com/app/1621690/Core_Keeper/
            link = str(link).replace("https://store.steampowered.com/app/", "")
            link = link[:link.index("/")]
            link = "https://steamdb.info/app/" + link + "/"
            # now link is something like https://steamdb.info/app/1621690/
            browser_obj.open(link)
            time.sleep(waiting_time)
        


def open_if_theres_any_free_game():
    soupForFree = BeautifulSoup( requests.get(url_for_free).text, 'html.parser')
    spans = [str(a.select('div.search_discount span')) for a in soupForFree.select('div#search_resultsRows a')]
    for span in spans:
        if span.find('100%') != -1:
            browser_obj.open(url_for_free)
            break



def open_all_links():
    for link in all_links:
        # link is something like https://store.steampowered.com/app/1621690/Core_Keeper/
        link = str(link).replace("https://store.steampowered.com/app/", "")
        link = link[:link.index("/")]
        link = "https://steamdb.info/app/" + link + "/"
        # now link is something like https://steamdb.info/app/1621690/
        browser_obj.open(link)
        time.sleep(waiting_time)
        

    

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
    open_all_steamdb_links()
    try_to_close_app()
    global layout
    layout[1] = [
        sg.Text("Open Discounts", font="Calibri 16", key='-OPEN-DISCOUNT-',  enable_events=True, text_color="red")
    ]
    


def handle_open_res():
    os.startfile(str(os.getcwd() + "/res"))
    sys.exit(0)



def handle_open_all_links():
    get_all_links()
    get_configs()
    setup_browser()
    open_all_links()
    sys.exit(0)
    


##################  GUI CODE  ##################




def handle_events(event, values):
    # if event == "-BACK-":
        # return HandlingResult.GO_BACK

    if event == "-OPEN-RES-":
        handle_open_res()
        # no return needed, sys.exit(0) will run

    if event == "-OPEN-ALL-LINKS-":
        handle_open_all_links()
        # no return needed, sys.exit(0) will run
    
    if event == "-EXECUTE-DISCOUNT-":
        handle_execute_discount()
        return HandlingResult.REFLESH

    if event == "-EXECUTE-FREE-":
        handle_execute_free()
        return HandlingResult.REFLESH

    if event == "-OPEN-FREE-" and not is_free_opened:
        handle_open_free()
        return HandlingResult.REFLESH
    
    if event == "-OPEN-DISCOUNT-" and not is_discount_opened:
        handle_open_discount()
        return HandlingResult.REFLESH

    return HandlingResult.STAY



def get_window():
    return sg.Window("Steam Crawler", copy.deepcopy(layout), element_justification="center", size=(500, 250), metadata=WindowType.SCPP)



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

