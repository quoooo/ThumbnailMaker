from copy import deepcopy
from re import compile
import io
import os
import PySimpleGUI as sg
from PySimpleGUI import ThisRow

from ThumbnailMaker import *


def get_fonts():
    all_fonts = (os.listdir(os.path.join(os.environ['WINDIR'], 'fonts')))
    local_fonts = os.listdir("./")
    font_list = []
    for font in all_fonts:
        if font.endswith(".ttf") or font.endswith(".ttc"):
            font_list.append(font)

    for font in local_fonts:
        if font.endswith(".ttf") or font.endswith(".ttc"):
            font_list.append(font)

    font_list.sort(key=str.lower)
    return font_list


def collapse(layout, key):
    return sg.pin(sg.Column(layout, key=key))


def filenameify(strings):
    regex = compile('[^a-zA-Z0-9]')
    output_string = ""
    for s in strings:
        if len(s) > 0:
            output_string += regex.sub('', s).lower() + "_"

    if output_string == "":
        output_string = "output_"

    return output_string[:len(output_string) - 1]


def save_all_settings(values, filename=None):
    for v in settings.read():
        settings[v] = values[v.upper()]
    settings.save(filename)


def load_all_settings(filename='./default.json'):
    loaded = sg.UserSettings(filename).load()

    for v in loaded:
        window[v.upper()].update(loaded[v])
    for x in range(1, 4):
        window[f'-COL TEXT{str(x)}-'].update(button_color=loaded[f'-col text set{str(x)}-'])
        window[f'-COL STROKE{str(x)}-'].update(button_color=loaded[f'-col stroke set{str(x)}-'])

    loaded = {k.upper(): v for k, v in loaded.items()}
    save_all_settings(loaded)


def create_settings_json():
    settings_list = {
        "-text1-": "Hello World",
        "-hide1-": True,
        "-multi1-": True,
        "-size1-": 125,
        "-shadow1-": True,
        "-width1-": 7,
        "-col text set1-": "#f7c825",
        "-align1-": "Left",
        "-col stroke set1-": "#7d277d",
        "-stroke size1-": 5,
        "-text2-": "",
        "-hide2-": True,
        "-multi2-": True,
        "-size2-": 60,
        "-shadow2-": True,
        "-width2-": 5,
        "-col text set2-": "#f7c825",
        "-align2-": "Left",
        "-col stroke set2-": "#7d277d",
        "-stroke size2-": 5,
        "-text3-": "",
        "-hide3-": True,
        "-multi3-": False,
        "-size3-": 125,
        "-shadow3-": True,
        "-width3-": 5,
        "-col text set3-": "#f7c825",
        "-align3-": "Left",
        "-col stroke set3-": "#7d277d",
        "-stroke size3-": 5,
        "-bg image-": "",
        "-fg image-": "",
        "-pad l-": 87,
        "-pad r-": 87,
        "-pad u-": 87,
        "-pad d-": 87,
        "-font choice-": "segmdl2.ttf",
        "-slider-box-": 0,
        "-slider-slide-": 0.0
    }
    for s in settings_list:
        settings.set(s, settings_list[s])
    sg.UserSettings.save(settings)


settings = sg.UserSettings(filename='settings.json', path='.')
if not settings.exists():
    create_settings_json()

SYMBOL_UP = '▲'
SYMBOL_DOWN = '▼'

fg_filename = settings['-fg image-']
try:
    overlay_img = get_overlay_img(fg_filename)
except:
    sg.popup_error("Forground image not found")
    overlay_img = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))

overlay_tn = deepcopy(overlay_img)
overlay_tn = overlay_tn.resize((320, 180))
bio = io.BytesIO()
overlay_tn.save(bio, format="PNG")
fonts = get_fonts()

sg.theme('DarkAmber')  # Add a touch of color
# All the stuff inside your window.

# -------------------- BOTTOM OF GUI ---------------------
button_col = [[sg.B('Test', s=10)],
              [sg.B('Preview', s=10)],
              [sg.B('Preview (Full)', s=10)],
              [sg.Save(s=10)]]

image_col = [[sg.Graph((320, 180), (0, 180), (320, 0), k='-GRAPH-')],
             [sg.Spin([i for i in range(-1281, 1281)], k='-SLIDER-BOX-', enable_events=True, s=4,
                      initial_value=settings['-slider-box-']), sg.Push(),
              sg.Slider(range=(-1280, 1280), orientation='h', size=(29, 20), disable_number_display=True,
                        k='-SLIDER-SLIDE-', enable_events=True, default_value=settings['-slider-slide-'])]]

# ----------------------- SETTINGS -----------------------
# smash settings
# smash_settings = [[sg.T('smash')]]

# more settings section
# settings_lay = [[sg.CB('smush mode', k='-OPEN SMASH SETTINGS-', enable_events=True)],
#                 [collapse(smash_settings, '-SMASH SETTINGS-')],

settings_lay = [[sg.ColorChooserButton('All Text Color', k=f'-COL TEXT ALL-', s=12, target=(ThisRow, 1)),
                 sg.I('', s=(7, 0), enable_events=True, k=f'-COL TEXT SET ALL-', disabled=True, text_color='black'),
                 sg.T('All text align:', s=12),
                 sg.Combo(['Left', 'Center', 'Right'], s=6, k=f'-ALIGN ALL-', readonly=True, tooltip='Text alignment', enable_events=True),

                 sg.T('Padding:', s=7),
                 sg.T('L', s=1),
                 sg.Spin([i for i in range(1, 999)], s=3, tooltip='Left padding', initial_value=settings['-pad l-'],
                         k='-PAD L-'),
                 sg.T('R', s=1),
                 sg.Spin([i for i in range(1, 999)], s=3, tooltip='Right padding', initial_value=settings['-pad r-'],
                         k='-PAD R-'),
                 sg.T('U', s=1),
                 sg.Spin([i for i in range(1, 999)], s=3, tooltip='Top padding', initial_value=settings['-pad u-'],
                         k='-PAD U-'),
                 sg.T('D', s=1),
                 sg.Spin([i for i in range(1, 999)], s=3, tooltip='Bottom padding', initial_value=settings['-pad d-'],
                         k='-PAD D-')],

                [sg.ColorChooserButton('All Stroke Color', k=f'-COL STROKE ALL-', s=12, target=(ThisRow, 1)),
                 sg.I('', s=(7, 0), enable_events=True, k=f'-COL STROKE SET ALL-', disabled=True, text_color='black'),
                 sg.T('All stroke size:', s=12), sg.Spin([i for i in range(0, 50)], s=6, k='-STROKE SIZE ALL-', enable_events=True),
                 sg.T('Font:', s=7, pad=((7, 0), (0, 0))),
                 sg.Combo(fonts, default_value=settings['-font choice-'], readonly=True, pad=((32, 0), (0, 0)),
                          k='-FONT CHOICE-'),
                 sg.Push()],

                [sg.I(settings[f'-fg image-'], k='-FG IMAGE-', visible=False, enable_events=True),
                 sg.FileBrowse('Edit foreground image', s=17),
                 sg.Push(),
                 sg.I('', visible=False, k='-LOAD FILE-', enable_events=True),
                 sg.FileBrowse('Load settings from file', s=17, initial_folder='.',
                               file_types=(('json', '*.json'), ('All Files', '*.*'))),
                 sg.I('', visible=False, k='-SAVE FILE-', enable_events=True),
                 sg.SaveAs('Save settings to file', s=17, initial_folder='.', default_extension='.json',
                           file_types=(('json', '*.json'), ('All Files', '*.*')))]]

# ---------------------- TOP OF GUI ----------------------
text_layout = []
for l in range(1, 4):
    text_layout += [[sg.Column(
        [[sg.InputText(settings[f'-text{str(l)}-'], k=f'-TEXT{str(l)}-', s=20, tooltip=f'Text {str(l)} in image')],
         [sg.CB('More settings', k=f'-HIDE{str(l)}-', enable_events=True, default=settings[f'-hide{str(l)}-'])]]),
        sg.Column([[sg.CB('Multiline', k=f'-MULTI{str(l)}-', s=6, default=settings[f'-multi{str(l)}-']),
                    sg.T('Font size: ', s=8),
                    sg.Spin([i for i in range(1, 500)], s=3, tooltip='Max text size',
                            initial_value=settings[f'-size{str(l)}-'], k=f'-SIZE{str(l)}-')],

                   [sg.CB('Shadow', k=f'-SHADOW{str(l)}-', s=6, default=settings[f'-shadow{str(l)}-']),
                    sg.T('Max width: ', s=8), sg.Spin([i for i in range(1, 13)], s=3,
                                                      tooltip='Max width of image\nBased on fraction of X/12',
                                                      initial_value=settings[f'-width{str(l)}-'],
                                                      k=f'-WIDTH{str(l)}-')
                    ]]),


        sg.Column([
            [sg.ColorChooserButton('Text Color', k=f'-COL TEXT{str(l)}-', s=9, target=(ThisRow, 1),
                                   button_color=settings[f'-col text set{str(l)}-']),
             sg.I(settings[f'-col text set{str(l)}-'], s=(7, 0), enable_events=True,
                  k=f'-COL TEXT SET{str(l)}-', disabled=True, text_color='black'),
             sg.T('Text alignment: ', s=12),
             sg.Combo(['Left', 'Center', 'Right'], default_value=settings[f'-align{str(l)}-'], s=(6, 0),
                      k=f'-ALIGN{str(l)}-', readonly=True, tooltip='Text alignment')],

            [sg.ColorChooserButton('Stroke Color', k=f'-COL STROKE{str(l)}-', s=9, target=(ThisRow, 1),
                                   button_color=settings[f'-col stroke set{str(l)}-']),
             sg.Input(settings[f'-col stroke set{str(l)}-'], s=(7, 0), enable_events=True,
                      k=f'-COL STROKE SET{str(l)}-', disabled=True, text_color='black'),
             sg.T('Stroke size: ', s=12),
             sg.Spin([i for i in range(0, 50)], s=6, k=f'-STROKE SIZE{str(l)}-',
                     initial_value=settings[f'-stroke size{str(l)}-'])
             ]], k=f'-COL{str(l)}-')]]

# ------------------------- FINAL ------------------------
layout = [[sg.T('Overlay Text', s=20), sg.Text('Hover over settings to learn more')],
          text_layout,
          [sg.T('')],
          [sg.FileBrowse('Browse background image', target=(ThisRow, 1)),
           sg.I(settings[f'-bg image-'], k='-BG IMAGE-', expand_x=True,
                        tooltip='Location of background image file', enable_events=True)],
          [sg.T(f'{SYMBOL_UP} Global Settings', enable_events=True, k='-OPEN SETTINGS-')],
          [collapse(settings_lay, '-SETTINGS-')],
          [sg.Column(image_col), sg.Push(), sg.vbottom(sg.Column(button_col))]]

# Create the Window
window = sg.Window('Thumbnail Maker', layout, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT, finalize=True)

settings_open = True
# settings_open = False
window['-SETTINGS-'].update(visible=settings_open)
for x in range(1, 4):
    window[f'-COL{x}-'].update(visible=window[f'-HIDE{str(x)}-'].get())

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
        print(window['-COL TEXT1-'].ButtonColor)

    elif event.startswith('-COL '):
        if event == '-COL TEXT SET1-':
            if values[event] == "None":
                window[event].update(window['-COL TEXT1-'].ButtonColor[1])
            else:
                window['-COL TEXT1-'].update(button_color=values['-COL TEXT SET1-'])
        elif event == '-COL TEXT SET2-':
            if values[event] == "None":
                window[event].update(window['-COL TEXT1-'].ButtonColor[1])
            else:
                window['-COL TEXT2-'].update(button_color=values['-COL TEXT SET2-'])
        elif event == '-COL TEXT SET3-':
            if values[event] == "None":
                window[event].update(window['-COL TEXT1-'].ButtonColor[1])
            else:
                window['-COL TEXT3-'].update(button_color=values['-COL TEXT SET3-'])
        elif event == '-COL TEXT SET ALL-':
            if values[event] == "None":
                window[event].update(window['-COL TEXT ALL-'].ButtonColor[1])
            else:
                window['-COL TEXT SET1-'].update(window['-COL TEXT ALL-'].ButtonColor[1])
                window['-COL TEXT SET2-'].update(window['-COL TEXT ALL-'].ButtonColor[1])
                window['-COL TEXT SET3-'].update(window['-COL TEXT ALL-'].ButtonColor[1])
                window['-COL TEXT1-'].update(button_color=values['-COL TEXT SET ALL-'])
                window['-COL TEXT2-'].update(button_color=values['-COL TEXT SET ALL-'])
                window['-COL TEXT3-'].update(button_color=values['-COL TEXT SET ALL-'])
                window['-COL TEXT ALL-'].update(button_color=values['-COL TEXT SET ALL-'])

        elif event == '-COL STROKE SET1-':
            if values[event] == "None":
                window[event].update(window['-COL TEXT1-'].ButtonColor[1])
            else:
                window['-COL STROKE1-'].update(button_color=values['-COL STROKE SET1-'])
        elif event == '-COL STROKE SET2-':
            if values[event] == "None":
                window[event].update(window['-COL TEXT1-'].ButtonColor[1])
            else:
                window['-COL STROKE2-'].update(button_color=values['-COL STROKE SET2-'])
        elif event == '-COL STROKE SET3-':
            if values[event] == "None":
                window[event].update(window['-COL TEXT1-'].ButtonColor[1])
            else:
                window['-COL STROKE3-'].update(button_color=values['-COL STROKE SET3-'])
        elif event == '-COL STROKE SET ALL-':
            if values[event] == "None":
                window[event].update(window['-COL STROKE ALL-'].ButtonColor[1])
            else:
                window['-COL STROKE SET1-'].update(window['-COL STROKE ALL-'].ButtonColor[1])
                window['-COL STROKE SET2-'].update(window['-COL STROKE ALL-'].ButtonColor[1])
                window['-COL STROKE SET3-'].update(window['-COL STROKE ALL-'].ButtonColor[1])
                window['-COL STROKE1-'].update(button_color=values['-COL STROKE SET ALL-'])
                window['-COL STROKE2-'].update(button_color=values['-COL STROKE SET ALL-'])
                window['-COL STROKE3-'].update(button_color=values['-COL STROKE SET ALL-'])
                window['-COL STROKE ALL-'].update(button_color=values['-COL STROKE SET ALL-'])

    elif event.startswith('-HIDE'):
        for x in range(1, 4):
            window[f'-COL{x}-'].update(visible=(values[f'-HIDE{x}-']))

    elif event == '-SLIDER-SLIDE-':
        window['-SLIDER-BOX-'].update(int(values['-SLIDER-SLIDE-']))
        if bg_id is not -1:
            graph.relocate_figure(bg_id, int(values['-SLIDER-SLIDE-']/4), 0)

    elif event == '-SLIDER-BOX-':
        window['-SLIDER-SLIDE-'].update(values['-SLIDER-BOX-'])
        if bg_id is not -1:
            graph.relocate_figure(bg_id, int(values['-SLIDER-BOX-']/4), 0)

    elif event == 'Preview' or event == 'Preview (Full)' or event == 'Save':
        txt_top_img = TxtData(text=values['-TEXT1-'].replace('\\n', '\n'),
                              max_txt_size=values['-SIZE1-'],
                              order=Order.TOP,
                              max_size_fraction=values['-WIDTH1-'],
                              font=values['-FONT CHOICE-'],
                              shadow_distance=10 if values['-SHADOW1-'] else -1,
                              multiline=values['-MULTI1-'],
                              fill_colour=window['-COL TEXT1-'].ButtonColor[1],
                              stroke_colour=window['-COL STROKE1-'].ButtonColor[1],
                              stroke_size=values['-STROKE SIZE1-'],
                              alignment=values['-ALIGN1-'],
                              padding=(values['-PAD L-'], values['-PAD U-'], values['-PAD R-'], values['-PAD D-']))

        txt_mid_img = TxtData(text=values['-TEXT2-'].replace('\\n', '\n'),
                              max_txt_size=values['-SIZE2-'],
                              order=Order.MID,
                              max_size_fraction=values['-WIDTH2-'],
                              font=values['-FONT CHOICE-'],
                              shadow_distance=10 if values['-SHADOW2-'] else -1,
                              multiline=values['-MULTI2-'],
                              fill_colour=window['-COL TEXT2-'].ButtonColor[1],
                              stroke_colour=window['-COL STROKE2-'].ButtonColor[1],
                              stroke_size=values['-STROKE SIZE2-'],
                              alignment=values['-ALIGN2-'],
                              padding=(values['-PAD L-'], values['-PAD U-'], values['-PAD R-'], values['-PAD D-']))

        txt_bot_img = TxtData(text=values['-TEXT3-'].replace('\\n', '\n'),
                              max_txt_size=values['-SIZE3-'],
                              order=Order.BOT,
                              max_size_fraction=values['-WIDTH3-'],
                              font=values['-FONT CHOICE-'],
                              shadow_distance=10 if values['-SHADOW3-'] else -1,
                              multiline=values['-MULTI3-'],
                              fill_colour=window['-COL TEXT3-'].ButtonColor[1],
                              stroke_colour=window['-COL STROKE3-'].ButtonColor[1],
                              stroke_size=values['-STROKE SIZE3-'],
                              alignment=values['-ALIGN3-'],
                              padding=(values['-PAD L-'], values['-PAD U-'], values['-PAD R-'], values['-PAD D-']))

        overlay_tn = deepcopy(overlay_img)
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

        if event == 'Preview':
            game_img.thumbnail((320, 180))
            overlay_tn = overlay_all(images, overlay_tn, None, (0, 0))
            overlay_tn = overlay_tn.resize((320, 180))
            bio = io.BytesIO()
            bio2 = io.BytesIO()
            overlay_tn.save(bio, format="PNG")
            game_img.save(bio2, format="PNG")

            graph.Erase()
            bg_id = graph.DrawImage(data=bio2.getvalue(), location=(int(values['-SLIDER-BOX-']/4), 0))
            graph.DrawImage(data=bio.getvalue(), location=(0, 0))

        elif event == 'Save':
            overlay_tn = overlay_all(images, overlay_tn, game_img, (values['-SLIDER-BOX-'], 0))

            fn = filenameify((values['-TEXT1-'], values['-TEXT2-'], values['-TEXT3-']))

            overlay_tn.save(f'./Images/{fn}.png')
            sg.popup("Image saved!", auto_close=True, auto_close_duration=3)

        elif event == 'Preview (Full)':
            overlay_tn = overlay_all(images, overlay_tn, game_img, (values['-SLIDER-BOX-'], 0))
            overlay_tn.show()

        save_all_settings(values)

        for img in images:
            img.image.close()
        overlay_tn.close()
        game_img.close()

    elif event == '-ALIGN ALL-':
        window['-ALIGN1-'].update(values[event])
        window['-ALIGN2-'].update(values[event])
        window['-ALIGN3-'].update(values[event])

    elif event == '-STROKE SIZE ALL-':
        window['-STROKE SIZE1-'].update(values[event])
        window['-STROKE SIZE2-'].update(values[event])
        window['-STROKE SIZE3-'].update(values[event])

    elif event == '-BG IMAGE-':
        window['-BG IMAGE-'].update(window['-BG IMAGE-'].get().replace(os.path.abspath(os.path.curdir).replace('\\', '/'), '.'))
        try:
            img_file = values['-BG IMAGE-']
            game_img = Image.open(img_file)
            game_img.thumbnail((320, 180))

            bio2 = io.BytesIO()
            game_img.save(bio2, format="PNG")

            graph.Erase()
            bg_id = graph.DrawImage(data=bio2.getvalue(), location=(int(values['-SLIDER-BOX-'] / 4), 0))
            graph.DrawImage(data=bio.getvalue(), location=(0, 0))
        except:
            pass

    elif event == '-FG IMAGE-':
        try:
            img_file = values['-FG IMAGE-']
            overlay_img = Image.open(img_file)
            overlay_tn = deepcopy(overlay_img)
            window['Preview'].click()
        except:
            pass

    elif event == '-OPEN SETTINGS-':
        settings_open = not settings_open
        window['-OPEN SETTINGS-'].update(
            f'{SYMBOL_DOWN} Global Settings' if settings_open else f'{SYMBOL_UP} Global Settings')
        window['-SETTINGS-'].update(visible=settings_open)

    elif event == '-SAVE FILE-':
        if window[event].get() is not '':
            save_all_settings(values, window[event].get())

    elif event == '-LOAD FILE-':
        if window[event].get() is not '':
            load_all_settings(window[event].get())

    elif event == 'Edit Me':
        sg.execute_editor(__file__)
    elif event == 'Version':
        sg.popup_scrolled(sg.get_versions())

window.close()
