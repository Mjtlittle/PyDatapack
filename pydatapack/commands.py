from .richtext import tellRichText
from .internals import *
from .constants import *

def pos(x, y, z, mode='relative'):
    working = []
    for part in [x,y,z]:
        if mode == 'relative':
            working.append('~')
        if part != 0:
            working.append(str(part))
        working.append(' ')
    return ''.join(working)[:-1]

def tellraw(text, selector='@s'):
    return f'tellraw {selector} {TextSegment(text).render()}'

def setblock(block, position='~ ~ ~', mode='replace'):
    return f'setblock {position} {block} {mode}'

def gamerule(name, value=None):
    # if no value provided
    if value == None:
        value = GAMERULE_DEFUALTS.get(name)

    # if invalid value provided
    elif not isinstance(value,type(GAMERULE_DEFUALTS.get(name))):
        return tellRichText(f'&cInvalid value for gamerule "{name}" x= {value}')
    
    return f'gamerule {name} {str(value).lower()}'

def tag_add(tag, selector='@s'):
    return f'tag {selector} add {tag}'

def tag_remove(tag, selector='@s'):
    return f'tag {selector} remove {tag}'
