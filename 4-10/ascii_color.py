#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
This is a tool used to convert a image to ASCII form!
'''
import os
import argparse
from contextlib import closing
from string import Template
from PIL import Image, ImageEnhance

# Correspondence defining.
key = 'MNHQ$OC?7>!:-;. '

# Param parser defining.
parser = argparse.ArgumentParser(description='Translate a image to ASCII form.')
parser.add_argument('filename', help='Declare the file you want to translate.')
parser.add_argument('newfile', nargs='?', default='new.html', help='Declare the new file name.')
parser.add_argument('-c', '--color', action='store_false', dest='color',
                    help='Choose the color mode, the output file may be large.')
parser.add_argument('-s', '-scale', type=int, metavar='NUM', default=300, dest='scale',
                    help='Give a integer to declare the size of the output file.')

#Template defining.
dot = '<span style="color: rgb({}, {}, {})">{}</span>'
temp = Template('''
<!doctype html>
<html>
    <head>
        <title>test</title>
        <meta charset="utf-8"/>
        <style>
         pre {
             font-size: 10px;
             line-height: 67%;
         }
        </style>
    </head>
    <body>
        <pre>
$str
        </pre>
    </body>
</html>
''')


def translate(filename, newfile, scale):
    '''To translate a black-white file.'''
    with closing(Image.open(filename)) as im:
        im.thumbnail((scale, scale))
        im = ImageEnhance.Sharpness(im).enhance(2)
        im = im.convert('L')
    width, height = im.size
    file_str = ''
    for x in range(height):
        for y in range(width):
            file_str += key[int(im.getpixel((y, x))*0.05859375)]
        file_str += '\n'
    with open(newfile, 'w') as f:
        f.write(temp.substitute(str=file_str))


def translate_color(filename, newfile, scale):
    '''To translate a colored file.'''
    with closing(Image.open(filename)) as im:
        im.thumbnail((scale, scale))
        im = ImageEnhance.Color(im).enhance(2)
        im = ImageEnhance.Sharpness(im).enhance(2)
    width, height = im.size
    file_str = ''
    for x in range(height):
        for y in range(width):
            r, g, b, *other = im.getpixel((y, x))
            L = int((r*0.299+g*0.587+b*0.114)*0.05859)
            file_str += dot.format(r, g, b, key[L])
        file_str += '\n'
    with open(newfile, 'w') as f:
        f.write(temp.substitute(str=file_str))


# Drive the program.
if __name__ == '__main__':
    args = vars(parser.parse_args())

    if not args['color']:
        translate_color(args['filename'], args['newfile'], args['scale'])
    else:
        translate(args['filename'], args['newfile'], args['scale'])

    os.system('open -a Safari {}'.format(args['newfile']))