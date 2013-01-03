'''
flipbook.bot
=-=-=-=-=-=-

page grid generator, with crop marks

copyleft 2008 ricardo lafuente
licensed under the GPLv3
'''
import yaml
from random import randint

# -=- LETTERSOUP INIT -=-
  
sentence = ('computers are', 'better friends than', 'most experts')

yamlfile = open('fivepieces/variables.yaml')
variables = yaml.load(yamlfile)
yamlfile = open('fivepieces/widths.yaml')
widths = yaml.load(yamlfile)
yamlfile = open('fivepieces/blueprint.yaml')
_blueprint = yaml.load(yamlfile)
setvars(variables)

execfile('fivepieces/parts.py',globals(),locals())


def render_string(string):
    '''Renders each letter of the input string.'''
    for letter in string:
        render_letter(letter)
    
def render_letter(letter, blueprint=_blueprint):
    '''Takes a character and a letter->parts dict, building the 
    appropriate glyph and displaying it.
    
    (see blueprint.yaml for an example of proper syntax)
    '''
    global _glyph_width, gap
    
    # hack for accomodating the space character
    if letter in specialchars:
        letter = specialchars[letter]
    if letter == 'space':
        translate(_glyph_width * widths[letter] + spacing, 0)
        return True
    _glyph_width = float(widths[letter] * em_width)
    gap = _glyph_width/2 - bar

    for part in blueprint[letter]:
        if letter == 'slash':
            print 'aha!'
        # run the function with the same name as the dict key
        # using the value of the key as kwargs   
        partname = part.keys()[0]
        kwargs = part.values()[0]
        # append the part function to the global namespace
        globals()[partname](**kwargs)
    translate(_glyph_width + spacing, 0)

def get_optimal_width(string, emwidth, targetwidth):
    '''Returns the coefficient between a fixed width value and the
    width of the string using emwidth as its letterwidth.
    
    Works for creating several strings with the same overall width.'''
    original_width = 0.
    for char in string:
        if char in specialchars:
            char = specialchars[char]
        original_width += emwidth * widths[char] + spacing
        
    coef = targetwidth / original_width
    return coef
    
# -=- DIMENSIONS -=-

# A4 page size
page_width = 29.700*cm
page_height = 21.100*cm

# our specific dimensions
rect_width = 8*cm
rect_height = 5*cm
margin = 2*cm

# cropmark specification
crop_distance = 0.2*cm
crop_length = 0.5*cm

# calculate how many rectangles will fit on the page
columns = int((page_width - margin*2) / rect_width)
rows = int((page_height - margin*2) / rect_height)

size(page_width, page_height)
background(1,1,1)

translate(margin, margin)

# -=- CROP MARKS -=-

stroke(0.5, 0.5, 0.5)
for row in range(0, rows + 1):

    # left  
    x1 = 0 - crop_distance - crop_length
    y1 = row * rect_height
    x2 = 0 - crop_distance
    y2 = row * rect_height
    line(x1,y1,x2,y2)
    
    # right
    x1 = columns * rect_width + crop_distance + crop_length
    y1 = row * rect_height
    x2 = columns * rect_width + crop_distance
    y2 = row * rect_height
    line(x1,y1,x2,y2)

for column in range(0, columns + 1):    
    # top
    x1 = column * rect_width
    y1 = 0 - crop_distance - crop_length
    x2 = column * rect_width
    y2 = 0 - crop_distance
    line(x1,y1,x2,y2)
    
    # bottom
    x1 = column * rect_width
    y1 = rows * rect_height + crop_distance + crop_length
    x2 = column * rect_width
    y2 = rows * rect_height + crop_distance
    line(x1,y1,x2,y2)

nostroke()

def drawcontents(value):
    global em_width, cap_height, spacing, bar, stem
    global bar_height, jut, slab
    translate(40, 20)  
    save()
    scale(.2,.2)
    # bar = slab
    background(1,1,1)
    c = color(.3,.3,.3)
    fill(c)
    WID =700.
    strokewidth(0.2)
    stroke(.8,.8,.8)
        
    for line in sentence:
        em_width = value*1.5
        save()
        render_string(line)
        restore()
        translate(0,cap_height+leading)
        
    restore()  

page = 9
pages = 9

cell = 1
cells = columns * rows

# iterate through all cells
for row in range(0,rows):
    # no shift for first row
    if row != 0:
        translate(0, rect_height)
        
    for column in range(0,columns):
        save()
        if column != 0:
            translate(column * rect_width, 0)
                    
        beginclip(0, 0, rect_width, rect_height)
        # drawing in each rectangle goes here
        
        value = cell * pages + page
        drawcontents(value)
        endclip()
        
        # back to original position
        restore()
        
        print str(cell) + "(row: " + str(row) + "; col: " + str(column) + ") - "  + str(value)
        cell += 1
