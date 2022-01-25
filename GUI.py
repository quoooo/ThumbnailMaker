import PySimpleGUI as sg
import main

SYMBOL_UP = '▲'
SYMBOL_DOWN = '▼'


def collapse(layout, key):
    return sg.pin(sg.Column(layout, key=key))


sg.theme('DarkAmber')  # Add a touch of color
# All the stuff inside your window.

col = [[sg.B('Preview', s=10)],
       [sg.B('Settings', s=10)],
       [sg.Save(s=10)]]

layout = [[sg.Text('Overlay Text', s=20)        , sg.Text('Shit goes here')],
          [sg.InputText(k='-TOPTEXT-', s=(20, 0), tooltip='Top text in image')],
          [sg.InputText(k='-MIDTEXT-', s=(20, 0), tooltip='Middle text in image')],
          [sg.InputText(k='-BOTTEXT-', s=(20, 0), tooltip='Bottom text in image')],
          [sg.Image(s=(320, 180), background_color='black'), sg.Push(), sg.vbottom(sg.Column(col))]]

# Create the Window
window = sg.Window('Window Title', layout, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):  # if user closes window
        break
    elif event == 'Edit Me':
        sg.execute_editor(__file__)
    elif event == 'Version':
        sg.popup_scrolled(sg.get_versions())
    elif event == 'Preview':
        print(values['-TOPTEXT-'])

window.close()
