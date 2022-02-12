# ThumbnailMaker

Create video thumbnails in seconds!

## Description

This project gives a simple solution to creating video thumbnails, with added emphasis on consistent designs. It can generate multiple thumbnails in a short amount of time, with little intervention from the user, save for writing the text. 

## Getting Started

### Dependencies

* [Pillow](https://pypi.org/project/Pillow/)
* [PySimpleGui](https://pypi.org/project/PySimpleGUI/)

### Installing

Download both files and run the cleaverly named 'GUI.py' file.

### Executing program

#### Text and settings
With the program open, text can be placed in the respective boxes, with relavant settings to their right. 

The Multiline setting will put the text on 2 lines if the max size of the text is too large for the defined area. If the text will fit the area without needing to be split in 2 lines, the Multiline setting will effectively do nothing. You can force 2 or more lines by using '\n' in the text box, if needed.

The Shadow setting toggles a simple text shadow.

Font size is the maximum possible size the font will be displayed at. Text may be smaller if it's maximum size does not fit in the confines of it's max width.

Max width is the total width of the image, minus the padding, over a fraction of 12. For example, a max width of 6 would be half the image, 9 would be three quarters, and 12 would be the full image (again, minus the padding).

Text and stroke color set the relevant colors. Click the buttons to open the color picker.

Text alignment sets the text to align to the left, right or center.

#### Images and other global settings
A foreground image can be set to either completely or partially fill the image behind the text. 

If an image only partially fills the screen or is semi transparent, a second image can be set as a background to fill the void. The background image can be moved left/right with the slider at the bottom of the window.

Padding sets the no-go zone for text. Max width and text alignment both rely on these to place the text properly.

Fonts can probably be done a bit more elegantly, but alas. You can add fonts to the program by dropping .ttf or .ttc files into the directory of the program.

#### Buttons
The Preview button will show the image in the bottom right canvas. The slider beneath can move the background image left or right to the user's preference. 
The Preview (Full) button will open the image in your PC's default image application. Note that this image can't be copied or saved as is. 
The Save button will save the image in the Images folder in the program's directory.


## Help

Bugs or common issues will go here eventually.

## Authors

Just me so far...

## Version History
* 1.0
    * Initial Release
