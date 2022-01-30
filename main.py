from PIL import Image, ImageDraw, ImageFont, ImageFilter
from enum import Enum


class Order(Enum):
    TOP = 1
    MID = 2
    BOT = 3


class Align(Enum):
    LEFT = 'Left'
    CENTER = 'Center'
    RIGHT = 'Right'


class TxtData:
    def __init__(self, text, max_txt_size, order, max_size_fraction, font,
                 shadow_distance=-1, multiline=False, fill_colour=(247, 200, 37),
                 stroke_colour=(125, 39, 125), stroke_size=5, alignment=Align.LEFT, padding=(0, 0, 0, 0),
                 location=(0, 0), rectangle=None, image=None):
        # TODO load default data from .json
        self.text = text
        self.max_txt_size = max_txt_size
        self.order = order
        self.max_size_fraction = max_size_fraction
        self.shadow_distance = shadow_distance
        self.multiline = multiline
        self.rectangle = rectangle
        self.location = location
        self.image = image
        self.this_font = font
        self.fill_colour = fill_colour  # yellow
        self.stroke_colour = stroke_colour  # purple
        self.stroke_size = stroke_size
        self.alignment = alignment
        self.padding_left, self.padding_top, self.padding_right, self.padding_bot = padding

    def text_shaper(self, canvas_size, rectangles=None):
        # if it is a multiline text, there are no new line chars, and the width of max text size > max width allowed
        if self.multiline and (' ' in self.text or '\n' in self.text):
            self.multiliner(canvas_size.size[0])

        # loop through text sizes until the max width is exceeded
        selected_size = self.text_sizer(self.text, canvas_size.size[0])

        txt_img = Image.new("RGBA", canvas_size.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(txt_img)
        fnt = ImageFont.truetype(self.this_font, selected_size)

        # get the height and the size of the ascender - https://en.wikipedia.org/wiki/Ascender_(typography)
        # needed for correctly spacing things later
        left, up, right, down = d.textbbox((0, 0), font=fnt, text=self.text)
        h = down - up
        w = right - left
        ascender = up

        # get X coordinate
        total_left_padding = 0
        if self.alignment == Align.LEFT.value:
            total_left_padding = self.padding_left
        elif self.alignment == Align.RIGHT.value:
            total_left_padding = canvas_size.size[0] - self.padding_right - w
        elif self.alignment == Align.CENTER.value:
            total_left_padding = int(canvas_size.size[0]/2) - self.padding_right + self.padding_left - int(w/2)

        # get Y coordinate
        total_top_padding = 0
        if self.order == Order.TOP:
            total_top_padding = self.padding_top - ascender
        elif self.order == Order.MID:
            if rectangles is not None:
                '''
                bottom of top rectangle
                distance between bottom of top and top of bottom, over 2
                half the height
                ascender for positionning 
                all this should place middle box perfectly between top and bottom
                '''
                total_top_padding = rectangles[0][3] \
                                    + (round((rectangles[1][1] - rectangles[0][3]) / 2)) \
                                    - round(h / 2) \
                                    - ascender
            else:
                total_top_padding = round(canvas_size.size[1] / 2) - round(h / 2) - round(ascender / 2)
        elif self.order == Order.BOT:
            total_top_padding = canvas_size.size[1] - self.padding_bot - h - ascender

        if self.shadow_distance >= 0:
            # draw the shadow
            d.multiline_text((total_left_padding + self.shadow_distance, total_top_padding + self.shadow_distance),
                             self.text, font=fnt, fill=(0, 0, 0, 75))
            txt_img = txt_img.filter(ImageFilter.GaussianBlur(6))

        # draw the text
        d = ImageDraw.Draw(txt_img)
        d.multiline_text((total_left_padding, total_top_padding), self.text, font=fnt, fill=self.fill_colour,
                         stroke_width=self.stroke_size, stroke_fill=self.stroke_colour)

        self.rectangle = d.textbbox((total_left_padding, total_top_padding), font=fnt, text=self.text)

        # d.rectangle(self.rectangle)

        self.image = txt_img

    def text_sizer(self, text, canvas_width):
        selected_size = 1
        w, h = 0, 0
        for new_size in range(1, self.max_txt_size):
            font = ImageFont.truetype(self.this_font, new_size)
            for line in text.split('\n'):
                # left, top, right, bottom = font.getbbox(line)
                temp_w = font.getbbox(line)[2]
                if temp_w > w:
                    w = temp_w
            if (w > round(canvas_width * self.max_size_fraction / 12) - self.padding_left) \
                    and self.alignment == Align.LEFT.value:
                break
            elif (w > round(canvas_width * self.max_size_fraction / 12) - self.padding_right) \
                    and self.alignment == Align.RIGHT.value:
                break
            elif (w > round(canvas_width * self.max_size_fraction / 12) - self.padding_right - self.padding_left) \
                    and self.alignment == Align.CENTER.value:
                break
            selected_size = new_size

        # print(selected_size, text)
        return selected_size

    def multiliner(self, canvas_width):
        total_width = ImageFont.truetype(self.this_font, self.max_txt_size).getbbox(self.text)[2]

        if self.alignment == Align.LEFT.value:
            max_width = round(canvas_width * self.max_size_fraction / 12) - self.padding_left
        elif self.alignment == Align.RIGHT.value:
            max_width = round(canvas_width * self.max_size_fraction / 12) - self.padding_right
        else:
            max_width = round(canvas_width * self.max_size_fraction / 12) - self.padding_left - self.padding_right

        if self.multiline and '\n' not in self.text and total_width > max_width:
            wordlist = self.text.split()
            centerer = 0, 0
            max_size = 1
            for x in range(len(wordlist)):
                str1 = ' '.join(wordlist[:x + 1])
                str2 = ' '.join(wordlist[x + 1:])

                local = min(self.text_sizer(str1, canvas_width), self.text_sizer(str2, canvas_width))
                if local > max_size:
                    centerer = str1, str2
                    max_size = max(max_size, local)
                else:
                    break

            self.text = f"{centerer[0]}\n{centerer[1]}"


def overlay_all(txt_imgs, overlay_img, bg_img, bg_location, out=None):
    if out is None:
        out = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))

    if bg_img is None:
        out.paste(overlay_img)
    else:
        bg_w = resizer(bg_img)
        bg_img = bg_img.resize((bg_w, 720))
        out.paste(bg_img.copy(), bg_location)
        out.alpha_composite(overlay_img)

    for img in txt_imgs:
        out.alpha_composite(img.image)

    return out


def get_overlay_img(filename='bkgrnd.png'):
    try:
        img = Image.open(filename)
        return img
    except OSError:
        print("== ERROR ==\nimage not found\n")
        raise


# resize image to proper height while maintaining aspect ratio
def resizer(img):
    ratio = 720 / img.size[1]
    return int(ratio * img.size[0])


def main():
    # create text data
    txt_top_img = TxtData("The Legend of Zelda: The Minish Cap", 125, Order.TOP, 7, 10, True)
    # txt_top_img = TxtData("A B C Alphabet!!!!!", 125, Order.TOP, 7, 10, True)
    txt_mid_img = TxtData("hola", 50, Order.MID, 5, 10, True)
    txt_bot_img = TxtData("0:00:00", 125, Order.BOT, 5, 10)

    overlay_img = get_overlay_img()

    # create text images
    txt_top_img.text_shaper(overlay_img)
    txt_bot_img.text_shaper(overlay_img)
    rectangles = (txt_top_img.rectangle, txt_bot_img.rectangle)
    txt_mid_img.text_shaper(overlay_img, rectangles)
    images = [txt_top_img, txt_mid_img, txt_bot_img]

    # load bg image, if no image exists create black image
    # TODO grab image some other way
    img_file = 'test.png'
    # x = urllib.request.urlretrieve("https://www.smashbros.com/assets_v2/img/fighter/ness/main5.png", 'char_left.png')
    # x = urllib.request.urlretrieve("https://www.smashbros.com/assets_v2/img/fighter/wolf/main.png", 'char_right.png')
    try:
        game_img = Image.open(img_file)
    except OSError:
        print("== ERROR ==\nimage not found\n")
        game_img = Image.new("RGB", (1280, 720), 0)

    # TODO loop until location of images are final
    finalized = False
    while not finalized:
        thumbnail = overlay_all(images, overlay_img, game_img, (200, 0))
        thumbnail.thumbnail((320, 180))
        # thumbnail.show()
        finalized = True

    out = overlay_all(images, overlay_img, game_img, (250, 0))
    # out.show()
    # out.save(fp='./Images/output.png')


if __name__ == '__main__':
    main()
