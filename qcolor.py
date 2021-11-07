#!/usr/bin/python

import argparse
import os
import inquirer
import json
from colorthief import ColorThief
from sty import fg, bg, ef, rs
from sty import Style, RgbFg
from sys import stderr, stdout
path_json = '/home/your_user/.config/qtile/settings/colors.json'

class SetColorError(Exception):
    pass

class logger:
   
    def set_verbosity(self, verbosity):
        self.verbose = verbosity

    def log(self,message, file=stdout):
        if self.verbose:
            print(message, file=file)

    def error(self, message,file=stderr):
        print(f'Error: {message}',file=file)

logger = logger()


def read_json():
    if os.path.exists(path_json):
        try:
            file = open(path_json)
            data = json.loads(file.read())
            return data
        except:
            return logger.error("File not set with format correct \n\n {'object':'object'}")
    else:
        return logger.error("File not found, Make sure the file exists!")

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def createFileColor(color,opacity):
    color = color
    is_rgb_start = False
    is_rgb_end = False
    fg.color_show = False

    opacity = opacity
    
    if int(opacity) > 100:
        opacity = 100
    if int(opacity) < 0:
        opacity = 0

    # Convert decimal percentage to hexadecimal value

    decimal_opacity = round(int(opacity)*255/100)
    
    opacity = str(hex(int(decimal_opacity)))[-2:].upper()
    
    #open file json
    try:
        with open(path_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        data = {}

    logger.log(data)
    if isinstance(color, dict):
        data['bar'] = color['bar'] + opacity
        color_back = hex_to_rgb(str(color['bar']))
        pass
    else:
        color_string = ''.join(str(color))
        is_rgb_start = color_string.startswith('(')
        is_rgb_end = color_string.endswith(')')
        if is_rgb_start and is_rgb_end:
            fg.color_show = Style(RgbFg(color[0],color[1],color[2]))
            data['bar'] = '#%02x%02x%02x' % color + opacity 
        else:
            data['bar'] = '#%02x%02x%02x' % color + opacity
            color_back = hex_to_rgb(str('#%02x%02x%02x' % color + opacity))
    
    #Save in JSON

    with open(path_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        if is_rgb_start and is_rgb_end and fg.color_show:
            return logger.log(f'Change color to: %s' % (fg.color_show + (data['bar'])))
        else:
            fg.color_show = Style(RgbFg(color_back[0],color_back[1],color_back[2]))
            return logger.log(f'Change color to: %s' % (fg.color_show + (data['bar'])))

#Choose colors from the pallete reference to image
def showColors(colors,opacity):
    questions = [
    inquirer.List('bar',
                  message="Choose the color for the bar",
                  choices=colors,
              ),
    ]
    answers = inquirer.prompt(questions)
    selected = answers
    createFileColor(selected,opacity)

#Validate HexCode color
def verify_hex(color):
    if len(color) == 6:
        try:
            int(color, 16)
            return color
        except ValueError:
            raise SetColorError("Invalid Hex code")
    else:
        raise SetColorError("Invalid Hex code")


#Set color from text

def textColor(text_color):
    
    color = verify_hex(text_color)
    
    with open(path_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    data['text'] = '#'+color
    
    with open(path_json, 'w') as outfile:
        json.dump(data, outfile)


def getImage(src,pallete,opacity):

    if os.path.exists(src):
        logger.log("Analyzing image, please wait...")
        image = ColorThief(src)
        if pallete:
            pallete_colors = image.get_palette(quality=4,color_count=int(pallete))
            colors = []
            for color in pallete_colors:
                hex_color = '#%02x%02x%02x' % color
                fg.color_show = Style(RgbFg(color[0],color[1],color[2]))
                colors.append((fg.color_show + hex_color, hex_color))
            return showColors(colors,opacity)
        else:
            dominant_color = image.get_color(quality=4)
        return createFileColor(dominant_color,opacity)
    else:
        return logger.error("Image not found!")

def cli():

    parser = argparse.ArgumentParser(description="Change the color from bar Qtile")

    parser.add_argument("-s","--source", help="Image path", default="", required=False)

    parser.add_argument("-p","--pallete", default="", help="Place a number and you will get the color palette of the image", required=False)

    parser.add_argument("-c","--color", help="Set color for bar in format HexCode. 'ffffff'", default="", required=False)

    parser.add_argument("-t","--text", help="Set color text for bar in format HexCode. 'ffffff'", default="", required=False)

    parser.add_argument("-o","--opacity", help="Set the opacity of the color 0 ~ 100", default="100", required=False)

    parser.add_argument("-r","--read", action='store_true', default=False, help="Read file json", required=False)

    parser.add_argument("-v","--verbose", action='store_true', default=False, help="Get verbosity", required=False)

    args = parser.parse_args()

    return args

def main():
    args = cli()
    logger.set_verbosity(args.verbose)
    
    if args.text and args.color == "" and args.source == "":
        return textColor(args.text)

    if args.text:
        textColor(args.text)

    if args.source and args.color:
        return logger.error("You can't set the image path and color at the same time!")
    try:
        if args.read:
            return read_json()
        if args.color:
            color = verify_hex(args.color)
            if color:
                return createFileColor(hex_to_rgb(str("#"+color)), args.opacity)
            else:
                return logger.error("Invalid HexCode color")
        if args.pallete:
            try:
                int(args.pallete)
            except:
                return logger.error("The pallet number is invalid")
        getImage(args.source, args.pallete, args.opacity)
    except SetColorError as e:
        logger.error(e)
        exit(1)


if __name__ == "__main__":
    main()
