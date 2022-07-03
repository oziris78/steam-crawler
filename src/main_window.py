

# my imports
import scpp
from my_enums import HandlingResult, WindowType

# imports
import PySimpleGUI as sg
import copy

# import os with custom path
import os
EXECUTABLE_PATH = os.getcwd()



##################  VARIABLES  ##################


sg.theme("DarkAmber")

layout = [
	[
		sg.Text("Main Window", key="-t-", font="Calibri 25", text_color="white")
	],
	[sg.VPush()],
	[
		sg.Text('Steam Crawler', font="Calibri 20", key='-SCPP-', enable_events=True)
	],
	[ sg.VPush() ]
]


window = None



##################  WINDOW FUNCTIONS  ##################


def get_main_window():
	global window
	window = sg.Window("Main Window", copy.deepcopy(layout), element_justification="center", 
							size=(350, 350), metadata=WindowType.MAIN_WINDOW)



def reopen_main_window():
	global window
	window.close()
	get_main_window()
    	


def reopen_scpp_window():
	global window
	window.close()
	window = scpp.get_window()



##################  MAIN  ##################



def main():
	global window
	window = scpp.get_window()
	while True:
		event, values = window.read()

		if event == sg.WIN_CLOSED:
			break
		
		if window.metadata == WindowType.MAIN_WINDOW:
			if event == "-SCPP-":
				reopen_scpp_window()
		
		if window.metadata == WindowType.SCPP:
			result = scpp.handle_events(event, values)
			
			if result == HandlingResult.GO_BACK:
				reopen_main_window()
			elif result == HandlingResult.REFLESH:
				reopen_scpp_window()

	window.close()



if __name__ == '__main__':
	main()


