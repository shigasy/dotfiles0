#!/usr/bin/python

'''
open_color.py -- Prints all open color items in Alfred XML format.
    written by Jongwook Choi (@wookayin)
'''

# https://raw.githubusercontent.com/yeun/open-color/v1.4.0/open-color.json
OPEN_COLORS_VERSION = '1.4.0'
OPEN_COLORS = \
{
  "white": "#ffffff",
  "black": "#000000",
  "gray": [
    "#f8f9fa",
    "#f1f3f5",
    "#e9ecef",
    "#dee2e6",
    "#ced4da",
    "#adb5bd",
    "#868e96",
    "#495057",
    "#343a40",
    "#212529"
  ],
  "red": [
    "#fff5f5",
    "#ffe3e3",
    "#ffc9c9",
    "#ffa8a8",
    "#ff8787",
    "#ff6b6b",
    "#fa5252",
    "#f03e3e",
    "#e03131",
    "#c92a2a"
  ],
  "pink": [
    "#fff0f6",
    "#ffdeeb",
    "#fcc2d7",
    "#faa2c1",
    "#f783ac",
    "#f06595",
    "#e64980",
    "#d6336c",
    "#c2255c",
    "#a61e4d"
  ],
  "grape": [
    "#f8f0fc",
    "#f3d9fa",
    "#eebefa",
    "#e599f7",
    "#da77f2",
    "#cc5de8",
    "#be4bdb",
    "#ae3ec9",
    "#9c36b5",
    "#862e9c"
  ],
  "violet": [
    "#f3f0ff",
    "#e5dbff",
    "#d0bfff",
    "#b197fc",
    "#9775fa",
    "#845ef7",
    "#7950f2",
    "#7048e8",
    "#6741d9",
    "#5f3dc4"
  ],
  "indigo": [
    "#edf2ff",
    "#dbe4ff",
    "#bac8ff",
    "#91a7ff",
    "#748ffc",
    "#5c7cfa",
    "#4c6ef5",
    "#4263eb",
    "#3b5bdb",
    "#364fc7"
  ],
  "blue": [
    "#e8f7ff",
    "#ccedff",
    "#a3daff",
    "#72c3fc",
    "#4dadf7",
    "#329af0",
    "#228ae6",
    "#1c7cd6",
    "#1b6ec2",
    "#1862ab"
  ],
  "cyan": [
    "#e3fafc",
    "#c5f6fa",
    "#99e9f2",
    "#66d9e8",
    "#3bc9db",
    "#22b8cf",
    "#15aabf",
    "#1098ad",
    "#0c8599",
    "#0b7285"
  ],
  "teal": [
    "#e6fcf5",
    "#c3fae8",
    "#96f2d7",
    "#63e6be",
    "#38d9a9",
    "#20c997",
    "#12b886",
    "#0ca678",
    "#099268",
    "#087f5b"
  ],
  "green": [
    "#ebfbee",
    "#d3f9d8",
    "#b2f2bb",
    "#8ce99a",
    "#69db7c",
    "#51cf66",
    "#40c057",
    "#37b24d",
    "#2f9e44",
    "#2b8a3e"
  ],
  "lime": [
    "#f4fce3",
    "#e9fac8",
    "#d8f5a2",
    "#c0eb75",
    "#a9e34b",
    "#94d82d",
    "#82c91e",
    "#74b816",
    "#66a80f",
    "#5c940d"
  ],
  "yellow": [
    "#fff9db",
    "#fff3bf",
    "#ffec99",
    "#ffe066",
    "#ffd43b",
    "#fcc419",
    "#fab005",
    "#f59f00",
    "#f08c00",
    "#e67700"
  ],
  "orange": [
    "#fff4e6",
    "#ffe8cc",
    "#ffd8a8",
    "#ffc078",
    "#ffa94d",
    "#ff922b",
    "#fd7e14",
    "#f76707",
    "#e8590c",
    "#d9480f"
  ]
}
###############################################################################

COLOR_CATEGORIES = (
    'gray', 'red', 'pink', 'grape', 'violet', 'indigo',
    'blue', 'cyan', 'teal', 'green', 'lime', 'yellow', 'orange'
)


from collections import OrderedDict
items = OrderedDict()

for color in COLOR_CATEGORIES:
    for number, hexcode in enumerate(OPEN_COLORS[color]):
        items['%s-%d' % (color, number)] = hexcode

XML_HEADER = ['<?xml version="1.0"?>', '<items>']
XML_FOOTER = ['</items>']

def print_category():
    lines = []
    for i, c in enumerate(COLOR_CATEGORIES):
        lines.append(
            '''
            <item uid="oc-{i}-{c}" autocomplete="{c}" type="file" valid="no">
                <title>{c}</title>
                <icon>icons/{c}-6.png</icon>
            </item>
            '''.format(i=i, c=c)
        )
    print('\n'.join(XML_HEADER + lines + XML_FOOTER))


def print_items(query):
    lines = []
    for key, hexcode in items.items():
        if not query in key:
            continue
        lines.append(
            '''
            <item uid="{key}" autocomplete="{key}" arg="{hexcode}" type="file">
                <title>{key}</title>
                <subtitle>{hexcode}</subtitle>
                <icon>icons/{key}.png</icon>
            </item>
            '''.format(key=key, hexcode=hexcode)
        )

    if not lines:
        lines.append(
            '''
            <item uid="no-result" type="file" valid="no">
                <title>No Results Found</title>
            </item>
            '''
        )

    print('\n'.join(XML_HEADER + lines + XML_FOOTER))


def hex2rgb(v):
    v = v.lstrip('#')
    L = len(v)
    return tuple(int(v[i:i+L/3], 16) for i in range(0, L, L/3))

def generate_icons():
    # requires Pillow package to run with '--generate-icons' options
    import os, os.path
    from PIL import Image
    if not os.path.exists('./icons'):
        os.mkdir('./icons')

    for key, hexcode in items.iteritems():
        print ('Generating %10s : %s ...' % (key, hexcode))
        pixel_rgb = hex2rgb(hexcode)
        im = Image.new('RGB', (64, 64))
        im.putdata([pixel_rgb] * (64*64))
        im.save('./icons/%s.png' % key)

def main():
    import sys
    arg = sys.argv[1] if len(sys.argv) > 1 else ''

    if arg == '--generate-icons':
        generate_icons()
    elif arg == '':
        print_category()
    else:
        print_items(arg)

if __name__ == '__main__':
    main()