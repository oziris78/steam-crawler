
from my_enums import WindowType, HandlingResult

import PySimpleGUI as sg
import copy


sg.theme("DarkAmber")
layout = [
    [sg.VPush()],
    [
		sg.Text('CHECK DISCOUNT', font="Calibri 18", key='-DISCOUNT-', enable_events=True)
    ],
    [
		sg.Text('CHECK FREE GAMES', font="Calibri 18", key='-FREE-', enable_events=True)
    ],
    [
		sg.Text('GO BACK', font="Calibri 18", key='-BACK-', enable_events=True)
    ],
    [sg.VPush()]
]


def handle_events(event, values):
    global layout

    if event == "-BACK-":
        return HandlingResult.GO_BACK
    
    if event == "-DISCOUNT-":
        layout[1] = [
            sg.Text("Open Discounts", font="Calibri 16", key='-OPEN-DISCOUNT-', 
                    enable_events=True, text_color="white")
        ]
        return HandlingResult.REFLESH

    if event == "-FREE-":
        layout[2] = [
            sg.Text("Open Free Games", font="Calibri 16", key='-OPEN-FREE-', 
                    enable_events=True, text_color="white")
        ]
        return HandlingResult.REFLESH

    return HandlingResult.STAY


def get_window():
    return sg.Window("Steam Crawler++", copy.deepcopy(layout), element_justification="center", size=(500, 150), metadata=WindowType.SCPP)


if __name__ == '__main__':
    pass