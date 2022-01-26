import copy
import io
import re
import PySimpleGUI as sg
from main import *

SYMBOL_UP = '▲'
SYMBOL_DOWN = '▼'


def collapse(layout, key):
    return sg.pin(sg.Column(layout, key=key))


def filenameify(strings):
    regex = re.compile('[^a-zA-Z0-9]')
    output_string = ""
    for s in strings:
        if len(s) > 0:
            output_string += regex.sub('', s).lower() + "_"

    if output_string == "":
        output_string = "output_"

    return output_string[:len(output_string) - 1]


overlay_img = get_overlay_img()
overlay_tn = copy.deepcopy(overlay_img)
overlay_tn = overlay_tn.resize((320, 180))
bio = io.BytesIO()
overlay_tn.save(bio, format="PNG")

sg.theme('DarkAmber')  # Add a touch of color
# All the stuff inside your window.

button_col = [[sg.B('Test', s=10, visible=False)],
              [sg.B('Preview', s=10)],
              [sg.Save(s=10)]]

image_col = [[sg.Graph((320, 180), (0, 180), (320, 0), k='-GRAPH-')],
             [sg.Spin([i for i in range(-321, 321)], k='-SLIDER-BOX', enable_events=True, s=3, initial_value=0), sg.Push(),
              sg.Slider(range=(-320, 320), orientation='h', size=(30, 20), disable_number_display=True,  k='-SLIDER-SLIDE', enable_events=True, default_value=0)]]

# smash settings
smash_settings = [[sg.T('dfgsdfg')]]

# more settings section
settings = [[sg.CB('smush mode', k='-OPEN SMASH SETTINGS-', enable_events=True)],
            [collapse(smash_settings, '-SMASH SETTINGS-')],
            [sg.T('settings go here')]]

layout = [[sg.T('Overlay Text', s=20), sg.Text('Settings will go here')],
          [sg.InputText(k='-TOPTEXT-', s=(20, 0), tooltip='Top text in image')],
          [sg.InputText(k='-MIDTEXT-', s=(20, 0), tooltip='Middle text in image')],
          [sg.InputText(k='-BOTTEXT-', s=(20, 0), tooltip='Bottom text in image')],
          [sg.T('Background image:', s=(17, 0)), sg.InputText(k='-BG IMAGE-', s=35, tooltip='Location of background image file'), sg.FileBrowse(k='-BROWSE-', enable_events=True)],
          [sg.T(SYMBOL_UP, enable_events=True, k='-OPEN SETTINGS-'), sg.T('More Settings')],
          [collapse(settings, '-SETTINGS-')],
          [sg.Column(image_col), sg.Push(), sg.vbottom(sg.Column(button_col))]]


# Create the Window
window = sg.Window('Thumbnail Maker', layout, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT, finalize=True)

settings_open = False
window['-SETTINGS-'].update(visible=settings_open)
window['-SMASH SETTINGS-'].update(visible=False)

graph = window['-GRAPH-']
graph.DrawImage(data=bio.getvalue(), location=(0, 0))
bg_id = -1

# --------------------------------------------------------
# ------------------------ EVENTS ------------------------
# --------------------------------------------------------

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):  # if user closes window
        break

    elif event == 'Test':
        pass

    elif event == '-SLIDER-SLIDE':
        window['-SLIDER-BOX'].update(int(values['-SLIDER-SLIDE']))
        if bg_id is not -1:
            graph.relocate_figure(bg_id, values['-SLIDER-SLIDE'], 0)

    elif event == '-SLIDER-BOX':
        window['-SLIDER-SLIDE'].update(values['-SLIDER-BOX'])
        if bg_id is not -1:
            graph.relocate_figure(bg_id, values['-SLIDER-BOX'], 0)

    elif event == 'Preview':
        txt_top_img = TxtData(values['-TOPTEXT-'], 125, Order.TOP, 7, 10, True)
        txt_mid_img = TxtData(values['-MIDTEXT-'], 50, Order.MID, 5, 10, True)
        txt_bot_img = TxtData(values['-BOTTEXT-'], 125, Order.BOT, 5, 10)

        overlay_tn = copy.deepcopy(overlay_img)
        txt_top_img.text_shaper(overlay_img)
        txt_bot_img.text_shaper(overlay_img)
        rectangles = (txt_top_img.rectangle, txt_bot_img.rectangle)
        txt_mid_img.text_shaper(overlay_img, rectangles)
        images = [txt_top_img, txt_mid_img, txt_bot_img]

        try:
            img_file = values['-BG IMAGE-']
            game_img = Image.open(img_file)
        except OSError:
            sg.popup_error('Background image not found', auto_close_duration=3, auto_close=True)
            game_img = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
        except AttributeError:
            sg.popup_error('Background image not found', auto_close_duration=3, auto_close=True)
            game_img = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
        game_img.thumbnail((320, 180))

        overlay_tn = overlay_all(images, overlay_tn, None, (0, 0))
        overlay_tn = overlay_tn.resize((320, 180))
        bio = io.BytesIO()
        bio2 = io.BytesIO()
        overlay_tn.save(bio, format="PNG")
        game_img.save(bio2, format="PNG")

        graph.Erase()
        bg_id = graph.DrawImage(data=bio2.getvalue(), location=(values['-SLIDER-BOX'], 0))
        graph.DrawImage(data=bio.getvalue(), location=(0, 0))

        overlay_tn.close()
        game_img.close()

    elif event == 'Save':
        txt_top_img = TxtData(values['-TOPTEXT-'], 125, Order.TOP, 7, 10, True)
        txt_mid_img = TxtData(values['-MIDTEXT-'], 50, Order.MID, 5, 10, True)
        txt_bot_img = TxtData(values['-BOTTEXT-'], 125, Order.BOT, 5, 10)

        overlay_tn = copy.deepcopy(overlay_img)
        txt_top_img.text_shaper(overlay_img)
        txt_bot_img.text_shaper(overlay_img)
        rectangles = (txt_top_img.rectangle, txt_bot_img.rectangle)
        txt_mid_img.text_shaper(overlay_img, rectangles)
        images = [txt_top_img, txt_mid_img, txt_bot_img]

        try:
            img_file = values['-BG IMAGE-']
            game_img = Image.open(img_file)
        except OSError:
            sg.popup_error('Background image not found', auto_close_duration=3, auto_close=True)
            game_img = Image.new("RGBA", (1280, 720), 0)
        except AttributeError:
            sg.popup_error('Background image not found', auto_close_duration=3, auto_close=True)
            game_img = Image.new("RGBA", (1280, 720), 0)

        overlay_tn = overlay_all(images, overlay_tn, game_img, (values['-SLIDER-BOX'] * 4, 0))

        fn = filenameify((values['-TOPTEXT-'], values['-MIDTEXT-'], values['-BOTTEXT-']))

        overlay_tn.save(f'./Images/{fn}.png')
        sg.popup("Image saved!", auto_close=True, auto_close_duration=3)

        for img in images:
            img.image.close()
        overlay_tn.close()
        game_img.close()

    elif event == '-OPEN SETTINGS-':
        settings_open = not settings_open
        window['-OPEN SETTINGS-'].update(SYMBOL_DOWN if settings_open else SYMBOL_UP)
        window['-SETTINGS-'].update(visible=settings_open)

    elif event == 'Edit Me':
        sg.execute_editor(__file__)
    elif event == 'Version':
        sg.popup_scrolled(sg.get_versions())
    elif event == '-OPEN SMASH SETTINGS-':
        window['-SMASH SETTINGS-'].update(visible=values['-OPEN SMASH SETTINGS-'])

window.close()
