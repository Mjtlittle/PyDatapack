from .commands import *

# item frames
def item_frame_connected_block(item,command,item_rotation=-1,on_block=''):
    parts = [f'execute as @e[type=item_frame, nbt={{Item:{{id:"{item}"}}']

    if item_rotation != -1:
        parts.append(f', ItemRotation: {item_rotation}b')
    
    
    parts.append(f'}}] at @s positioned ^ ^ ^-1 ')

    if on_block != '':
        parts.append(f'if block ~ ~ ~ {on_block} ')
    
    parts.append('run '+command)
    
    return ''.join(parts)

def item_frame_remove_item(reset_rotation=True):
    parts = ['execute as @e[type=item_frame] run data merge entity @s {Item:{id:"minecraft:air",Count:1b}']
    if reset_rotation:
        parts.append(', ItemRotation: 0b')
    parts.append('}')
    return ''.join(parts)

# ! custom kill message
def custom_kill(richtext,target='@s'):
    parts = []
    parts.append(gamerule('showDeathMessages',False))
    parts.append('kill @s')
    parts.append(gamerule('showDeathMessages'))
    parts.append(tellRichText(richtext))
    return '\n'.join(parts)

# leather armor give
def leather_armor_color_value(r,g,b):
    return (r << 16) + (g << 8) + b

    # return f'give {target} minecraft:leather_helmet{{display:{{color:{value}}}}} {amount}'
