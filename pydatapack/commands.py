from .richtext import tellRichText
from .internals import *
from .constants import *

def pos(x,y,z,mode='relative'):
    working = []
    for part in [x,y,z]:
        if mode == 'relative':
            working.append('~')
        if part != 0:
            working.append(str(part))
        working.append(' ')
    return ''.join(working)[:-1]

def tellraw(text,target='@s'):
    return f'tellraw {target} {TextSegment(text).render()}'

def setblock(block,position='~ ~ ~',mode='replace'):
    return f'setblock {position} {block} {mode}'

def gamerule(name,value=None):
    # if no value provided
    if value == None:
        value = GAMERULE_DEFUALTS.get(name)

    # if invalid value provided
    elif not isinstance(value,type(GAMERULE_DEFUALTS.get(name))):
        return tellRichText(f'&cInvalid value for gamerule "{name}" x= {value}')
    
    return f'gamerule {name} {str(value).lower()}'


# ! incomplete
def sb_operation(op):
    op.split()

'''
    def relative(x,y,z):
        x = str(x) if x != 0 else ''
        y = str(y) if y != 0 else ''
        z = str(z) if z != 0 else ''
        return f'~{x} ~{y} ~{z}'

    def exact(x,y,z):
        return f'{x} {y} {z}'
'''


