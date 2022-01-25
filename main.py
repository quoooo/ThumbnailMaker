from PIL import Image, ImageDraw, ImageFont, ImageFilter
from enum import Enum
import urllib.request


class Order(Enum):
    TOP = 1
    MID = 2
    BOT = 3


class TxtData:
    def __init__(self, text, max_txt_size, order, max_size_fraction,
                 shadow_distance=-1, multiline=False, rectangle=None, location=(0, 0), image=None):
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

        # hard coded for now
        self.padding_top = 88
        self.padding_bot = 88
        self.padding_sides = 88
        # TODO text alignment
        # TODO search font in folder, else use basic font
        self.this_font = "PoetsenOne-Regular.ttf"
        # self.this_font = "ariblk.ttf"
        self.fill_colour = (247, 200, 37)  # yellow
        self.stroke_colour = (125, 39, 125)  # purple

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
        h = d.textbbox((0, 0), font=fnt, text=self.text)[3] - d.textbbox((0, 0), font=fnt, text=self.text)[1]
        ascender = d.textbbox((0, 0), font=fnt, text=self.text)[1]

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
            d.multiline_text((self.padding_sides + self.shadow_distance, total_top_padding + self.shadow_distance),
                             self.text, font=fnt, fill=(0, 0, 0, 75))
            txt_img = txt_img.filter(ImageFilter.GaussianBlur(6))

        # draw the text
        d = ImageDraw.Draw(txt_img)
        d.multiline_text((self.padding_sides, total_top_padding), self.text, font=fnt, fill=self.fill_colour,
                         stroke_width=5, stroke_fill=self.stroke_colour)

        self.rectangle = d.textbbox((self.padding_sides, total_top_padding), font=fnt, text=self.text)

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
            if w > round(canvas_width * self.max_size_fraction / 12) - self.padding_sides:
                break
            selected_size = new_size

        return selected_size

    def multiliner(self, canvas_width):
        total_width = ImageFont.truetype(self.this_font, self.max_txt_size).getbbox(self.text)[2]
        max_width = round(canvas_width * self.max_size_fraction / 12) - self.padding_sides

        if self.multiline and '\n' not in self.text and total_width > max_width:
            wordlist = self.text.split()
            centerer = 0, 0
            for x in range(len(wordlist)):
                str1 = ' '.join(wordlist[:x + 1])
                str2 = ' '.join(wordlist[x + 1:])
                segment_width = ImageFont.truetype(self.this_font, self.max_txt_size).getbbox(str1)[2]
                if segment_width > max_width:
                    current = min(self.text_sizer(str1, canvas_width), self.text_sizer(str2, canvas_width))
                    past = min(self.text_sizer(centerer[0], canvas_width), self.text_sizer(centerer[1], canvas_width))
                    if current > past:
                        centerer = str1, str2
                    break
                else:
                    centerer = str1, str2

            self.text = f"{centerer[0]}\n{centerer[1]}"


def overlay_all(txt_imgs, overlay_img, bg_img, bg_location, out=None):
    out = Image.new("RGB", (1280,720), 0)
    out.paste(bg_img.copy().resize((1280, 720)), bg_location)

    out.paste(overlay_img, (0, 0), overlay_img)

    for image in txt_imgs:
        out.paste(image.image, image.location, image.image)

    return out


# def preview()

def main():
    # create text data
    txt_top_img = TxtData("Pupperazzi", 125, Order.TOP, 7, 10, True)
    # txt_top_img = TxtData("A B C Alphabet!!!!!", 125, Order.TOP, 7, 10, True)
    txt_mid_img = TxtData("Any% Speedrun", 50, Order.MID, 5, 10, True)
    txt_bot_img = TxtData("3:30", 125, Order.BOT, 5, 10)

    try:
        overlay_img = Image.open('bkgrnd.png')
    except OSError:
        print("== ERROR ==\nimage not found\n")
        raise

    txt_top_img.text_shaper(overlay_img)
    txt_bot_img.text_shaper(overlay_img)

    rectangles = (txt_top_img.rectangle, txt_bot_img.rectangle)

    txt_mid_img.text_shaper(overlay_img, rectangles)

    images = [txt_top_img, txt_mid_img, txt_bot_img]

    # create final output image
    # out = Image.new("RGB", (1280, 720), 0)

    # load bg image, if no image exists create black image
    # TODO grab image some other way
    img_file = 'Untitled.png'
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

    # out = Image.new("RGB", (1280, 720), 0)
    out = overlay_all(images, overlay_img, game_img, (250, 0))
    out.show()
    out.save(fp='./Images/output.png')


if __name__ == '__main__':
    main()
